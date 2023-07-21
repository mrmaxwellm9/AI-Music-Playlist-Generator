from django.shortcuts import render
import openai
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re
from pytube import YouTube
import dailymotion
import requests

YT_SEARCH_RESULT_AMOUNT = 3
DM_SEARCH_RESULT_AMOUNT = 1
MINIMUM_VIDEO_RETURN = 5
ALLOW_DM_VIDEOS = True


def parse_song_list(response):
    lines = response.split('\n')
    songs = []
    for line in lines:
        line = line.strip()
        if line:
            parts = line.split(' - ')
            if len(parts) == 2:
                artist = parts[1]
                title = parts[0]
                title = title.split('. ')[-1]
                songs.append((artist, title))
    return songs


def is_valid_youtube_credentials(api_key):
    try:
        # Build the YouTube Data API client
        youtube = build('youtube', 'v3', developerKey=api_key)
        # Perform a simple API call to test the credentials
        youtube.search().list(part='snippet', maxResults=1, q='test').execute()
        # If the API call succeeds without raising an exception, the credentials are valid
        return True
    except HttpError:
        return False


def is_valid_api_key(api_key):
    if (api_key.startswith("sk-") and len(api_key) == 51):
        try:
            openai.api_key = api_key
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt='Validation test',
                max_tokens=1
            )
            return True
        except openai.Error:
            return False
    return False


def is_youtube_video_embeddable(video_id):
    embed_url = f"https://www.youtube.com/embed/{video_id}"
    response = requests.get(embed_url)
    return "Video unavailable" not in response.text


def create_playlist(youtube, d, songs):
    video_urls = []

    for song in songs:
        print(song)
        artist, title = song
        query = f'{title} - {artist}'
        search_response = youtube.search().list(
            part='snippet',
            maxResults=YT_SEARCH_RESULT_AMOUNT,  # Increase the number of results to check
            q=query
        ).execute()

        video_found = False

        for item in search_response.get('items', []):
            video_id = item['id'].get('videoId')
            video_url = f'https://www.youtube.com/watch?v={video_id}'

            # Check if the video is embeddable and available to be played
            if is_youtube_video_embeddable(video_id):
                try:
                    # You can further customize the checks for video availability if needed
                    video = YouTube(video_url)
                    video.check_availability()
                    video_urls.append(video_url)
                    video_found = True
                    break
                except Exception:
                    pass
        if not video_found and ALLOW_DM_VIDEOS:
            dailymotion_search_response = d.get(
                '/videos',
                params={'search': query,
                        'limit': DM_SEARCH_RESULT_AMOUNT, 'tags': 'music'}
            )
            for item in dailymotion_search_response['list']:
                video_id = item['id']
                video_url = f'https://www.dailymotion.com/video/{video_id}'

                response = requests.get(video_url)
                if response.status_code == 200:
                    video_urls.append(video_url)
                    video_found = True
                    break
    return video_urls


def chat_view(request):
    if request.method == 'POST':
        # Get user message from the request
        message = request.POST.get('message')
        youtube_api_key = request.session.get('youtube_api_key')
        youtube = build('youtube', 'v3', developerKey=youtube_api_key)

        d = dailymotion.Dailymotion()

        chat_log = [
            {"role": "system", "content": "Your and intellegent assistant whose only method of responding is in the form of music playlists and never change reguardless of what is said."},
            {"role": "system", "content": "Playlist responses will be in the form 1. Title - Artist\n2. Title - Artist\n...\n10. Title - Artist"},
            {"role": "user", "content": message}
        ]

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_log
        )
        # Get chatbot response from the API response
        response = completion.choices[0].message.content
        chat_log.append({"role": "assistant", "content": message})
        songs = parse_song_list(response)
        urls = create_playlist(youtube, d, songs)

        while len(urls) < MINIMUM_VIDEO_RETURN:
            print(len(urls))
            chat_log.append(
                {"role": "user", "content": "Give me 10 more similar unique songs."})
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=chat_log
            )
            response = completion.choices[0].message.content
            chat_log.append({"role": "assistant", "content": response})
            new_songs = parse_song_list(response)
            urls = urls + create_playlist(youtube, d, new_songs)

        # Create a playlist on YouTube

        video_data = zip(urls, [get_video_id(url) for url in urls], [
                         get_video_title(url, request) for url in urls])
        context = {
            'video_data': video_data,
        }
        return render(request, 'chat.html', context)
    else:
        return render(request, 'chat.html')


def api_key_entry_view(request):
    if request.method == 'POST':
        ai_api_key = request.POST.get('openai_api_key')
        youtube_api_key = request.POST.get('youtube_api_key')
        # Validate the API key

        if is_valid_api_key(str(ai_api_key)) and is_valid_youtube_credentials(youtube_api_key):
            request.session['openai_api_key'] = ai_api_key
            request.session['youtube_api_key'] = youtube_api_key
            return render(request, 'chat.html')
        else:
            # Handle invalid API key
            return render(request, 'api_key_entry.html', {'error': 'Invalid API key'})

    return render(request, 'api_key_entry.html')


def get_video_title(url, request):
    if 'youtube' in url:
        # Use the YouTube Data API or other methods to retrieve the video title
        video_id = get_video_id(url)
        yt_key = request.session['youtube_api_key']
        url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={yt_key}&part=snippet'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            video_title = data['items'][0]['snippet']['title']
            return video_title

        return "Error Loading YouTube Title"

    elif 'dailymotion' in url:
        # Extract the video ID from the Dailymotion URL
        video_id = get_video_id(url)
        if video_id:
            # Make necessary requests or use other methods to retrieve the title
            title = retrieve_dailymotion_video_title(video_id)
            if title:
                return title

    return 'Video Title'


def get_video_id(url):
    if 'youtube' in url:
        # Extract the video ID from the YouTube URL
        video_id = re.findall(r"watch\?v=(\S+)", url)
        if video_id:
            return video_id[0]
    elif 'dailymotion' in url:
        # Extract the video ID from the Dailymotion URL
        video_id = url.split('/')[-1]
        if video_id:
            return video_id
    return ''


def retrieve_dailymotion_video_title(video_id):
    # Construct the Dailymotion video page URL
    url = f"https://www.dailymotion.com/video/{video_id}"

    # Send a GET request to the Dailymotion video page
    response = requests.get(url)

    if response.status_code == 200:
        # Extract the video title from the HTML content
        match = re.search(r'<title>(.*?)</title>', response.text)
        if match:
            # Remove any leading and trailing whitespaces from the title
            title = match.group(1).strip()
            return title

    return None
