""" Works with map with the use of folium method """

import os
from logging import info

import folium


class FriendsMap:
    """ Creates map with friends based on provided data """

    def __init__(self, save_to: str = 'map.html'):
        self.save_to = save_to
        self.map = folium.Map()

    def save_map(self):
        """ Save map to html file"""
        # create map directory if not exists
        if ((len(os.path.dirname(self.save_to)) > 1) and
                (not os.path.exists(os.path.dirname(self.save_to)))):
            os.makedirs(os.path.dirname(self.save_to))
        self.map.save(self.save_to)

        info(f"Saved map to {self.save_to}")

    def create_map(self, friends):
        """ Create map based on provided pd.DataFrame """
        fg_friend_markers = folium.FeatureGroup(name="Twitter Friends")

        for friend in friends:
            friend_latitude, friend_longitude = friend['latitude'], friend['longitude']
            fg_friend_markers.add_child(
                folium.Marker(location=[friend_latitude, friend_longitude],
                              popup=f"{friend['name']}",
                              icon=folium.Icon(icon="user", prefix='fa'))
            )

        self.map.add_child(fg_friend_markers)

        info("Created map")

        return self.map
