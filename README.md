# AI-Music-Playlist-Generator

## Dependencies

The dependencies for the project can be found in the [requirements.txt](https://github.com/mrmaxwellm9/AI-Music-Playlist-Generator/blob/master/requirements.txt) file and can be installed using pip install -r requirements.txt

## Keys

#### Django

To run the server you will need to [generate a Django secret key](https://www.educative.io/answers/how-to-generate-a-django-secretkey). Once you have generated the key, open the [settings.py](https://github.com/mrmaxwellm9/AI-Music-Playlist-Generator/blob/master/AiPlaylistMaker/settings.py) file and edit the try-except block at the top of the file. You can either hard code the key by adding the line "SECRET_KEY = YOUR_KEY" and remove the try-except block at the top of the settings file; paste your key in a text file and change the path in this line of the try-except block "with open('etc/secret_key.txt') as f:" to reference your text file, or you can set the key to an environment variable named DJANGO_SECRET_KEY.

#### YouTube

When you launch the server and route to the site, you will be asked to enter a YouTube API key, to [obtain a YouTube API key](https://developers.google.com/youtube/v3/getting-started) which allows a free daily quota of use. 

#### OpenAI

When you launch the server and route to the site, you will be asked to enter an OpenAI API key, to obtain an OpenAI API key you will need to visit [OpenAI's website](https://platform.openai.com/), create an account, and then in your user settings navigate to [API keys](https://platform.openai.com/account/api-keys). Note that usage of OpenAI API calls will always come with a charge however the charge is small fractions of a penny per call. To learn more about the pricing you can visit [OpenAI's GPT pricing page](https://openai.com/pricing). Note that this project uses GPT-3.5 Turbo, however you can change this by editing the views.py file if you would like to use a different version.

## Usage

To run the server type "python manage.py runserver" in the same directory as the manage.py file. This should start the server and give you a url the server is running on. Open a web browser and direct to that url. ![alt text](https://raw.githubusercontent.com/mrmaxwellm9/images/main/AI_Enter_Keys.png?token=GHSAT0AAAAAACEFFZBTTJMTY7ZWY54RYF5EZF5NV3A "Enter_API_Keys_Screen") 
A screen that looks like the above image should display and after entering the valid API keys and clicking submit you should be redirected to the ChatGPT chat screen that looks like the image below
![alt text](https://raw.githubusercontent.com/mrmaxwellm9/images/main/AI_Type_A_Message.png?token=GHSAT0AAAAAACEFFZBTPNL5JZQS4DUWNVN6ZF5NV4Q "GPT_Chat_Screen") 
Where it says "Type your message..." enter a message for the AI to read and interpret into a playlist of music. 

###  Playlist Interface

When entering the prompt "Rock and Roll" the following screen is provided. 
![alt text](https://raw.githubusercontent.com/mrmaxwellm9/images/main/AI_Video_Display.png?token=GHSAT0AAAAAACEFFZBTLAZ3YOR44CSUHNEEZF5NWGA "Rock_And_Roll_Playlist")
To play a specific video you can click the desired video from the list of videos on the left. To play the video use the video's native player controls. To control the volume, YouTube offers an adequate volume bar in its native player, but if a Dailymotion video plays a custom volume bar will be added to the player controls below the video player.

Other player control options include shuffle, autoplay, previous, and next. The next button plays the next video in the playlist, or a random video if shuffle is toggled on. The previous button always plays the previously played video regardless of shuffle. Autoplay makes it so that upon video completion the next button is automatically pressed.


## Additional Features and Program Information

### Custom Searching

### Inner Workings
