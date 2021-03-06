# mixFlaskApp
A Flask App to help people trying to make mixes by matchings 
songs based on tempo and key 

![Description](https://github.com/gargavi/mixFlaskApp/blob/master/static/images/description.JPG) 



## How to run? 

1. First make sure you have python and pip on your computer 
2. Git clone this repo and then move into the directory 
3. Create a virtual environment and activate it (not necessary but good for practice) 
4. DO: "pip install -r requirements.txt" 
5. Go to developer.spotify.com and make an account and a new app. This will get you a 
CLIENTID and a CLIENTSECRET which you should put in the get_prefs() function in application.py (towards the bottom) 
6. In the developer account you also have to add  "127.0.0.1:8080/home" as a redirect link 
7. Go back to your terminal and run "python application.py" 
8. If a browser doesn't open up with the app go to 127.0.0.1:8080 and your app should be there. 

## How to use? 

There is a helpful html link on the main page that will tell you how to do just that. 

## Future Updates? 

1. I will be adding an additional page that will let users add to their "database" 
2. I will add a way to save the matched song to a playlist to allow a person to list to the songs 
3. I will add a way to match songs based on other attributes (danceability, rhythm and more) 

**Took base inspiration from sheagcraig's actually_random project for authentication** 
