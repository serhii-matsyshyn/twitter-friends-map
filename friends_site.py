""" Flask site for twitter-friends-map """

# pylint: disable = import-error,broad-except

import os
from logging import DEBUG, getLogger

from flask import Flask, render_template, request

from friends_api import FriendsApi
from friends_map import FriendsMap

getLogger().setLevel(DEBUG)

SECRET_TWITTER_API_BEARER_TOKEN = os.getenv("SECRET_TWITTER_API_BEARER_TOKEN")
friends_api = FriendsApi(SECRET_TWITTER_API_BEARER_TOKEN)

app = Flask(__name__)


@app.route("/")
def index():
    """
    Main page.
    """
    return render_template("index.html")


@app.route("/create-map", methods=["POST"])
def create_map():
    """
    Create map with twitter friends locations
    """
    username = request.form.get("username")
    if not username:
        return render_template("error.html")

    if '@' not in username:
        username = '@' + username

    try:
        friends_locations = friends_api.get_friends_coordinates(username)
        if len(friends_locations) == 0:
            raise Exception('No friends found or incorrect account name. Try again.')

        friends_map = FriendsMap()
        created_friends_map = friends_map.create_map(friends_locations)
    except Exception as err:
        return render_template("error.html", data=str(err))

    return created_friends_map


if __name__ == '__main__':
    app.run()
