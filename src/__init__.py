import spotipy
import yaml
from spotipy.oauth2 import SpotifyClientCredentials
from collections import defaultdict

from src.TrackInfo import TrackInfo


class DegreesOfSeparation:

    def __init__(self):
        self.__sp = None
        self._config = {}
        self._access_token = ""

    def main(self):
        try:
            self.load_config()
            self.initialize_spotipy()
        except Exception as error:
            print(error)

        beginning_artist, ending_artist = "Chance the Rapper", "Kendrick Lamar"  #retrieve_artists()
        results = self.perform_artist_search(str(beginning_artist).upper(), str(ending_artist).upper())
        for track in results:
            print(str(track))

    def initialize_spotipy(self):
        client_credentials_manager = SpotifyClientCredentials(self._config.get("client_id"),
                                                              self._config.get("client_secret"))
        self.__sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def load_config(self):
        with open("config/config.yaml", 'r') as stream:
            try:
                self._config = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def retrieve_artists(self):
        beginning_artist = input("Name of artist to begin search: ").lower()
        ending_artist = input("Name of artist to end search: ").lower()
        return beginning_artist, ending_artist

    def perform_artist_search(self, beginning_artist, ending_artist):
        # TODO replace this dictionary with a defaultdict
        artist_graph = {beginning_artist: set([])}

        queue = [(beginning_artist, [])]

        while queue:
            (vertex, path) = queue.pop(0)

            if vertex == beginning_artist:
                results = self.__sp.search(q=beginning_artist, limit=50)
                sorted(results['tracks']['items'], key=lambda track: (track['popularity']))
                for track in results['tracks']['items']:
                    for artist in track['artists']:
                        featured_artist = str(artist['name']).upper()

                        if featured_artist == ending_artist:
                            return [beginning_artist, ending_artist]

                        if self.can_add_artist_to_graph(featured_artist, artist_graph, beginning_artist):
                            related_track = TrackInfo(track['name'], beginning_artist, featured_artist)
                            artist_graph[beginning_artist].add(related_track)
                            queue.append((featured_artist, path + [related_track]))

            # find next unique artist in associated artists graph
            not_yet_visited = artist_graph[vertex] - set(path)

            for current_track in not_yet_visited:
                current_artist = current_track.featured_artist
                results = self.__sp.search(q=current_artist, limit=50)
                sorted(results['tracks']['items'], key=lambda track: (track['popularity']))
                for track in results['tracks']['items']:
                    if len(track['artists']) > 1:
                        for artist in track['artists']:
                            featured_artist = str(artist['name']).upper()
                            related_track = TrackInfo(track['name'], current_artist, featured_artist)

                            if featured_artist == ending_artist:
                                return path + [current_track, related_track]

                            if self.can_add_artist_to_graph(featured_artist, artist_graph, current_artist):
                                if current_artist in artist_graph:
                                    artist_graph[current_artist].add(related_track)
                                else:
                                    artist_graph[current_artist] = {related_track}
                                queue.append((current_track, path + [current_track]))

        return []

    def can_add_artist_to_graph(self, featured_artist, featured_artists, beginning_artist):
        return featured_artist not in featured_artists and featured_artist != beginning_artist

degrees_of_separation = DegreesOfSeparation()
degrees_of_separation.main()
