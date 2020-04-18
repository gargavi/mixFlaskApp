
from __future__ import print_function
import pandas as pd
from flask import Flask, redirect, request, render_template, session, url_for, flash, get_flashed_messages
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, BooleanField, StringField, validators, SelectField, IntegerField
from wtforms.validators import NoneOf, Required
import spotipy 
import sys 

application = Flask(__name__)
application.secret_key = "something_else"
bootstrap = Bootstrap(application)


CLIENT_SIDE_URL = "avigarg.pythonanywhere.com"
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8080
REDIRECT_URI = "{}:{}/home".format(CLIENT_SIDE_URL, PORT)
#REDIRECT_URI = CLIENT_SIDE_URL + "/home"
SCOPE = ("playlist-modify-public playlist-modify-private "
         "playlist-read-collaborative playlist-read-private user-library-read user-library-modify")

# Forms to be used 

class Matches(FlaskForm):
    spotifyid = StringField(label = "Spotify Id:", validators =[validators.required()])
    exact = BooleanField("Exact Key Match?")
    double = BooleanField("Double Tempo?")
    half = BooleanField("Half Tempo?")
    normal = BooleanField("Normal Tepo?")
    tightness = IntegerField("Tightness:", validators = [validators.required(), validators.NumberRange(1, 10)])
    popularity = BooleanField(label = "Sort by Popularity? ")
    numbers = IntegerField("# of Songs?", validators = [validators.required(), validators.NumberRange(1, 100)])
    submit = SubmitField("Submit:")

# This is the function that fixes the key of songs
def fix_keys(songdataframe):
    song_df = songdataframe.copy()
    song_df["key_ish"] = song_df["key"].map({0: "C", 1: "D-", 2: "D", 3: "E-", 4: "E", 5: "F", 6: "F+", 7: "G", 8: "A-", 9: "A", 10: "B-", 11: "B"}) + song_df["mode"].map({0: "mi", 1: "ma"})
    song_df["true_key"] = song_df["key_ish"].map({"Cmi": "5A",
                                                  "Cma": "8B", 
                                                  "D-mi": "12A", 
                                                  "D-ma": "3B", 
                                                  "Dmi": "7A", 
                                                  "Dma": "10B", 
                                                  "E-mi": "2A", 
                                                  "E-ma": "5B", 
                                                  "Emi": "9A", 
                                                  "Ema": "12B", 
                                                  "Fmi": "4A", 
                                                  "Fma": "7B", 
                                                  "F+mi": "11A", 
                                                  "F+ma": "2B", 
                                                  "Gmi": "6A", 
                                                  "Gma": "9B", 
                                                  "A-mi": "1A", 
                                                  "A-ma": "4B", 
                                                  "Ami": "8A", 
                                                  "Ama": "11B", 
                                                  "B-mi": "3A",
                                                  "B-ma": "6B", 
                                                  "Bmi": "10A", 
                                                  "Bma": "1B"
                                                 })
    return song_df.drop(["key_ish"], axis = 1)

#This add songs to either a file or a dataframe 
def add_songs_to_output(sp, album = None, playlist = None, song = None, filename = None, dataframe = pd.DataFrame()):
    """
    Point of this is to be able to add songs to the output, either if it is a dataframe or a filelocation 
    Uses spotify API to do so 
    """
    def inornah(list, a):
        if a in list:
            return 1
        else:
            return 0
    if playlist == None and song == None and album == None:
        raise Exception("Need to enter a song to add")
    if song != None: 
        songs = [{"track":sp.track(song)}]
    elif playlist != None:
        songs = []
        b = sp.playlist(playlist)["tracks"]
        while b["next"]:
            songs.extend(b["items"])
            b = sp.next(b)
        songs.extend(b["items"])
    elif album != None: 
        songs = []
        b = sp.album(album)["tracks"]
        while b["next"]:
            songs.extend(b["items"])
            b = sp.next(b)
        songs.extend(b["items"])
        #return songs
    if filename != None:
        dataframe = pd.read_csv(filename, encoding = "cp1252")
    if filename == None:
        listsongs = [[
        "id",
        "name",
        "popularity",
        "artist_name", 
        "explicit",
        "key", 
        "timesig", 
        "danceability",
        "energy",
        "loudness",
        "mode",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "genres"
    ]]
        for song in songs:
            try: 
                iid = song["track"]["id"]
            except:
                iid = song["id"]
            if (dataframe.empty) or (iid not in dataframe["id"].values):
                new_list = []
                try:
                    new_list.append(song["track"]["id"])
                    new_list.append(song["track"]["name"])
                    temp = sp.track(song["track"]["id"])
                except:
                    new_list.append(song["id"])
                    new_list.append(song["name"])
                    temp = sp.track(song["id"])
                try: 
                    new_list.append(temp["popularity"])
                    new_list.append(temp["artists"][0]["name"])
                    new_list.append(temp["explicit"])
                    audio_features = sp.audio_features(new_list[0])[0]
                    new_list.append(audio_features["key"])
                    new_list.append(audio_features["time_signature"])
                    new_list.append(audio_features["danceability"])
                    new_list.append(audio_features["energy"])
                    new_list.append(audio_features["loudness"])
                    new_list.append(audio_features["mode"])
                    new_list.append(audio_features["speechiness"])
                    new_list.append(audio_features["acousticness"])
                    new_list.append(audio_features["instrumentalness"])
                    new_list.append(audio_features["liveness"])
                    new_list.append(audio_features["valence"])
                    new_list.append(audio_features["tempo"])
                    new_list.append(sp.artist(temp["artists"][0]["uri"])["genres"])
                    listsongs.append(new_list)
                except:
                    print(new_list)
        song_df = pd.DataFrame(data = listsongs[1:], columns = listsongs[0])
        all_genres = []
        for item in song_df["genres"]:
            for value in item:
                if value not in all_genres:
                    all_genres.append(value)
        for a in all_genres:
            song_df[a] = [inornah(x, a) for x in song_df["genres"]]
        song_df = fix_keys(song_df)
    song_df = song_df.sort_values("popularity", ascending = False).groupby(["name", "artist_name"]).first()
    df = dataframe.append(song_df, sort = False)
    df = df.sort_values("popularity", ascending = False).groupby(["name", "artist_name"]).first()
    return df
# This is the chunky function that deals with the data 
def close_match(song, songs, matching = 0, closeness = 1, exact_key = False, half_temp = False, double_temp = False, normal_temp = True, popularity_sort = False):
    index = song.index[0]
    reduced = pd.DataFrame(columns = song_db.columns)
    if half_temp:
        base = song["tempo"][index]/2
        reduced = pd.concat([reduced, songs[(songs["tempo"] > base - 1*3*closeness) & (songs["tempo"] < base + 1*3*closeness)]])
    if double_temp:
        base = song["tempo"][index]*2
        reduced = pd.concat([reduced, songs[(songs["tempo"] > base - 1*3*closeness) & (songs["tempo"] < base + 1*3*closeness)]])
    if normal_temp: 
        base = song["tempo"][index]
        reduced = pd.concat([reduced, songs[(songs["tempo"] > base - 1*3*closeness) & (songs["tempo"] < base + 1*3*closeness)]])
    if exact_key:
        print(song, file = sys.stderr)
        reduced = reduced[reduced["true_key"] == song["true_key"][index]]
    else:    
        reduced = reduced[((reduced["true_key"].str[: -1].astype("int64") == (int(song["true_key"][index][:-1]) + 1) % 12 ) & 
                         (reduced["true_key"].str[-1] == song["true_key"][index][-1]))
                        | ((reduced["true_key"].str[: -1].astype("int64") == (int(song["true_key"][index][:-1]) - 1 ) % 12) &
                           (reduced["true_key"].str[-1] == song["true_key"][index][-1]))
                       | (reduced["true_key"].str[: -1].astype("int64") == int(song["true_key"][index][:-1])) 
                       ]
    matched = []
    for _, row in reduced.iterrows(): 
        count = 0
        for key, item in {"speechiness":1, "acousticness": 1, "instrumentalness":1, "danceability": 1, "energy": 1, "loudness": 10, "liveness" : 1, "valence": 1}.items(): 
            if (song[key][index] > row[key] - .1*closeness*item) and (song[key][index] < row[key] + .1*closeness*item): 
                count += 1
        if count >= matching: 
            matched.append(row["id"])
    reduced = reduced[["name", "artist_name", "id", "popularity", "tempo", "true_key"]]
    if popularity_sort == True: 
        return reduced.sort_values("popularity", ascending = False )
    return reduced


#song_db = pd.read_csv("output.csv")
stored_info = {}
song_db = pd.DataFrame()
@application.route("/")
def index(): 
    return "Hello World"


def index1():
    stored_info["token"] = None
    sp_oauth = get_oauth()
    return redirect(sp_oauth.get_authorize_url())

@application.route("/home", methods =["GET", "POST"])
def home():
    if request.args.get("code"):
        get_spotify(request.args["code"])
        stored_info["token"] = get_oauth().get_cached_token()
    try:
        os.remove(".tokens")
    except:
        a = 1
    form = Matches()
    if form.is_submitted():
        print('Hello world!', file=sys.stderr)
        target_song = None
        if song_db[song_db["id"] == form.spotifyid.data].shape[0] != 0: 
            target_song = song_db[song_db["id"] == form.spotifyid.data]
        else: 
            target_song = add_songs_to_output(sp = get_spotify(), song = form.spotifyid.data)
            try: 
                target_song = add_songs_to_output(sp = get_spotify(), song = form.spotifyid.data)
            except Exception as e: 
                print(e, file=sys.stderr)
                return render_template("home.html", form = form, values = [], target_song = None)
        matching_df = close_match(
            target_song, song_db, closeness = form.tightness.data, exact_key = form.exact.data, 
            half_temp = form.half.data, double_temp = form.double.data, normal_temp = form.normal.data, 
            popularity_sort = form.popularity.data)
        matching_df = matching_df[:form.numbers.data]
        all_rows = []
        for _, row in matching_df.iterrows():
            to_add = [row["name"], row.artist_name, row.popularity, row.tempo, row.true_key]
            all_rows.append(to_add)
        index = target_song.index[0]
        diction = target_song.to_dict()
        target_song = [index[0], index[1], diction["popularity"][index], diction["tempo"][index], diction["true_key"][index]]
        return render_template("home.html", form = form, values = all_rows, target_song = target_song)
    return render_template("home.html", form = form, values = [], target_song = "None")


def get_oauth():
    """Return a Spotipy Oauth2 object."""
    prefs = get_prefs()
    return spotipy.oauth2.SpotifyOAuth(
        prefs["ClientID"], prefs["ClientSecret"], REDIRECT_URI, scope=SCOPE,
        cache_path=".tokens")


def get_spotify(auth_token=None):
    """Return an authenticated Spotify object."""
    oauth = get_oauth()
    token_info = stored_info["token"]
    if not token_info and auth_token:
        token_info = oauth.get_access_token(auth_token)
    return spotipy.Spotify(token_info["access_token"])


def get_prefs():
    """Get application prefs plist and set secret key.
    Args:
        path: String path to a plist file.
    """
    prefs = {'ClientID' : '9a89b1b3f68a46d085cdc372adef5fdd',
             'ClientSecret': 'b6ea71732a224938b6a48fa51581b7d6'}
    return prefs


#this just runs the function
if __name__ == "__main__":
#   #application.run(debug = True, host = "0.0.0.0")
    application.run(debug=True, port=PORT)

