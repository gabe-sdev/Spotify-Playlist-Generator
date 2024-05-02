import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
#Using the spotipy python module to execute the code
import spotipy
#inside the spotipy module it pulls in other modules and all of their content into the code
#I am calling the .oauth2 module and importing the SpotifyOAuth class into the code so that
#I do not have to type in 'spotipy.oauth2.SpotifyOAuth (which is the class name inside the module)
#into my code each time and simply type in SpotifyOAuth to use it in my code.
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

#Spotify ID's
load_dotenv()
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

date = input("Which year fo you want to travel to? Type the date in this format YYYY-MM-DD: ")

get_response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
# print(get_response.text)
web_page_content = get_response.text

soup = BeautifulSoup(web_page_content, "html.parser")
# print(soup.title)
print(f"Billboards Top 100 songs from {date} web scraping...\n")
#Searching the webpage for the h3 attribute nested within 'a li ul li h a' class selector named 'title'
top_songs_list = soup.select("li ul li h3")
# print(top_songs_list)
#Grabbing the text from each h3 tag and appending it to a new song_names list with list comprehension
song_names = [tag.getText().strip() for tag in top_songs_list]
print(f"Success!! List of Top 100 Song:\n{song_names}\n")


##Spotify API Code##

#The scope variable is assigned a Spotify Web API scope based off the available list of scopes.
#Ref Spotify WebAPI Doc; Manage your private playlists.
scope = "playlist-modify-private"

#Setting up the 'sp' object for the code and calling the '.Spotify()' class from the spotipy client module
#and, I am specifying the 'auth_manager' parameter to the 'SpotifyOAuth()' class from the spotipy oauth2 module
#with an optional parameter of "scope=". I am taking the scope variable defined above and passing it to this parameter.
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, show_dialog=True))

#'me()' method is a spotipy built-in method that returns a json dictionary detailed profile information
#about the current user. Setting the "user_id" variable to my 'id' key.
user_id = sp.me()['id']
print(f"My User ID->{user_id}...\n")

new_playlist_text = f"Top 100 List from {date}"
print(f"Creating {new_playlist_text}...\n")

print(f"Creating New Playlist...\n")
#'user_playlist_create()' is a spotipy built-in method that creates a playlist for a user and returns a json dictionary.
#I am creating a "new_playlist" variable based on the "date" input variable entered at the beginning of the code exec.
data_return = sp.user_playlist_create(user=user_id, name=new_playlist_text, public=False)
# pprint(data_return)
new_playlist_id = data_return["id"]
print(f"New Playlist ID->{new_playlist_id}\n")

#Search song from 'song_names' list using .'search()' Spotipy method and appending the 'uri' key values of each song
#from the json dictionary provided via the api to a new list named 'song_search_list'
print(f"Searching for the songs on Spotify....\n")
song_search_list = []
for name in song_names:
    result = sp.search(q=name, limit=1)
    song_search_list.append(result["tracks"]["items"][0]["uri"])
print(f"Success, all songs have been found...\n")
#Add the 'uri' tracks to the new_playlist using the 'playlist_add_items' method with the playlist_id parameter
#set to the 'new_playlist_id' created above and the item parameter set the 'song_search_list' created above
sp.playlist_add_items(playlist_id=new_playlist_id, items=song_search_list)
print(f"New {new_playlist_text} is ready!\n")
