import numpy as np
import pandas as pd
from tqdm import tqdm
from flask import Flask, render_template, request, Markup
import string

class Spotify_Recommendation():
    def __init__(self, dataset):
        self.dataset = dataset
    def recommend(self, songs, amount=1):
        distance = []
        song = self.dataset[(self.dataset['name'].str.lower() == songs.lower())].head(1).values[0]
        rec = self.dataset[self.dataset['name'].str.lower() != songs.lower()]
        for songs in tqdm(rec.values):
            d = 0
            for col in np.arange(len(rec.columns)):
                if not col in [1, 6, 12, 14, 18]:
                    d = d + np.absolute(float(song[col]) - float(songs[col]))
            distance.append(d)
        rec['distance'] = distance
        rec = rec.sort_values('distance')
        columns = ['artists', 'name']
        return rec[columns][:amount]


app = Flask(__name__)
df = pd.read_csv('spotify clusters.csv')
recommendations = Spotify_Recommendation(df)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    song = request.form['song']
    number = int(request.form['recnumber'])

    output = ""
    title = "Songs Similar To " + string.capwords(song) + ":"
    i = 1
    recs = recommendations.recommend(song, number)
    for artists, songs in recs.values:
        output += Markup(str(i) + ". " + songs + " by " + artists[1:-1].replace("'", "").replace('"', "") + "<br>")
        i+= 1

    return render_template('home.html', song_user_likes=title, song_recs=output)


if __name__ == '__main__':
    app.run(debug=True)
