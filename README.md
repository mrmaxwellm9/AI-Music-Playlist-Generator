# AI-Music-Playlist-Generator

## Setup

### Dependencies

The dependencies for the project can be found in the [requirements.txt](https://github.com/mrmaxwellm9/AI-Music-Playlist-Generator/blob/master/requirements.txt) file and can be installed using pip install -r requirements.txt

### Keys

#### Django

To run the server you will need to [generate a Django secret key](https://www.educative.io/answers/how-to-generate-a-django-secretkey). Once you have generated the key, open the [settings.py](https://github.com/mrmaxwellm9/AI-Music-Playlist-Generator/blob/master/AiPlaylistMaker/settings.py) file and edit the try-except block at the top of the file. You can either hard code the key by adding the line "SECRET_KEY = YOUR_KEY" and remove the try-except block at the top of the settings file; paste your key in a text file and change the path in this line of the try-except block "with open('etc/secret_key.txt') as f:" to reference your text file, or you can set the key to an environment variable named DJANGO_SECRET_KEY.

#### YouTube

When you launch the server and route to the site, you will be asked to enter a YouTube API key, to [obtain a YouTube API key](https://developers.google.com/youtube/v3/getting-started) which allows a free daily quota of use. 

#### OpenAI

When you launch the server and route to the site, you will be asked to enter an OpenAI API key, to obtain an OpenAI API key you will need to visit [OpenAI's website](https://platform.openai.com/), create an account, and then in your user settings navigate to [API keys](https://platform.openai.com/account/api-keys). Note that usage of OpenAI API calls will always come with a charge however the charge is small fractions of a penny per call. To learn more about the pricing you can visit [OpenAI's GPT pricing page](https://openai.com/pricing). Note that this project uses GPT-3.5 Turbo, however you can change this by editing the views.py file if you would like to use a different version.

## Usage

## Additional Features and Program Information

### Custom Searching

### Inner Workings
