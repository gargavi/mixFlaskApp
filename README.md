# mixFlaskApp
A Flask App to help people trying to make mixes by matchings 
songs based on tempo and key 

![Description] (https://github.com/gargavi/mixFlaskApp/blob/master/static/images/readme1.JPG) 



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
