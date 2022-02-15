""" Module to get Friends Locations with the use of Twitter API
and then convert their locations to coordinates
"""

# pylint: disable = import-error  # To disable import-error warning

import os
import warnings
from logging import debug
import requests

from locations_coordinates import LocationsCoordinates

warnings.filterwarnings('ignore', message='Unverified HTTPS request')


class FriendsApi:
    """ Get Friends Locations with the use of Twitter API
    and then convert their locations to coordinates"""

    def __init__(self, bearer_token):
        self.headers = {'Authorization': f'Bearer {bearer_token}'}
        self.locations_coordinates = LocationsCoordinates()

    def get_friends(self, username: str, count: int = 20):
        """ Make request to Twitter API to get user friends"""
        params = {'screen_name': username,
                  'count': count}

        response = requests.get('https://api.twitter.com/1.1/friends/list.json',
                                headers=self.headers,
                                params=params, verify=False)
        r_j = response.json()

        if r_j.get('errors'):
            raise Exception(f'Twitter API errors: {r_j.get("errors")}')

        if r_j.get('error') is not None:
            raise Exception(f'Twitter API error: {r_j.get("error")}')

        debug(response.text)

        return response.json()

    def get_friends_coordinates(self, username: str):
        """ Get those user friends in Twitter that have location coordinates """
        friends = self.get_friends(username)
        friends_coordinates = []
        for friend in friends['users']:
            latitude, longitude = self.locations_coordinates.get_place_location_approx(
                friend['location']
            )
            debug(f"Friend: {friend['name']}, {latitude=}, {longitude=}")

            if latitude and longitude:
                friend_coordinates = {"name": friend['name'],
                                      "location": friend['location'],
                                      "latitude": latitude,
                                      "longitude": longitude}

                friends_coordinates.append(friend_coordinates)

        return friends_coordinates


if __name__ == '__main__':
    SECRET_TWITTER_API_BEARER_TOKEN = os.getenv("SECRET_TWITTER_API_BEARER_TOKEN")
    friends_api = FriendsApi(SECRET_TWITTER_API_BEARER_TOKEN)
    friends_locations = friends_api.get_friends_coordinates('@elonmusk')
    print(friends_locations)
