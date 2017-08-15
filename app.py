import os
from flask import Flask, request, render_template, jsonify
from twitter import TwitterClient
from movie import MovieClient

app = Flask(__name__)
twitter_api = TwitterClient('@Sirajology')
movie_api = MovieClient('war for the planet of the apes')


def strtobool(v):
    return v.lower() in ["yes", "true", "t", "1"]


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/tweets')
def tweets():
    retweets_only = request.args.get('retweets_only')
    twitter_api.set_retweet_checking(strtobool(retweets_only.lower()))
    with_sentiment = request.args.get('with_sentiment')
    twitter_api.set_with_sentiment(strtobool(with_sentiment.lower()))
    query = request.args.get('query')
    twitter_api.set_query(query)

    tweets = twitter_api.get_tweets()
    return jsonify({'data': tweets, 'count': len(tweets)})

@app.route('/movie')
def movie():
    query = request.args.get('query')
    movie_api.set_query(query)

    details = movie_api.get_movie()
    return jsonify({'data': details})


port = int(os.environ.get('PORT', 5000))
app.run(host="0.0.0.0", port=port, debug=True)
