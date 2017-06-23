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

        beginning_artist, ending_artist = self.retrieve_artists()
        results = self.perform_artist_search(beginning_artist, ending_artist)
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
        beginning_artist = input("Name of artist to begin search: ").upper()
        ending_artist = input("Name of artist to end search: ").upper()
        return beginning_artist, ending_artist

    def perform_artist_search(self, beginning_artist, ending_artist):
        # TODO replace this dictionary with a defaultdict
        artist_graph = {beginning_artist: set([])}
        queue = [(beginning_artist, [])]
        result = []

        result = self.subsearch(artist_graph, [], queue, None, beginning_artist, ending_artist)
        if len(result) > 0:
            return result

        while queue:
            (vertex, path) = queue.pop(0)
            not_yet_visited = artist_graph[vertex] - set(path)
            for current_track in not_yet_visited:
                main_artist = current_track.featured_artist
                result = self.subsearch(artist_graph, path, queue, current_track, main_artist, ending_artist)
                if len(result) > 0:
                    return result

        return result

    def subsearch(self, artist_graph, path, queue, current_track, main_artist, ending_artist):
        results = self.__sp.search(q=main_artist, limit=50)
        sorted(results['tracks']['items'], key=lambda track: (track['popularity']))
        for track in results['tracks']['items']:
            if len(track['artists']) > 1:
                for artist in track['artists']:
                    featured_artist = str(artist['name']).upper()
                    related_track = TrackInfo(track['name'], main_artist, featured_artist)

                    if featured_artist == ending_artist:
                        if current_track is not None:
                            return path + [current_track, related_track]
                        else:
                            return path + [related_track]

                    if self.can_add_artist_to_graph(artist_graph, featured_artist, main_artist):
                        if main_artist in artist_graph:
                            artist_graph[main_artist].add(related_track)
                        else:
                            artist_graph[main_artist] = {related_track}
                        queue.append((related_track, path + [related_track]))

        return []

    def can_add_artist_to_graph(self, featured_artists, featured_artist, beginning_artist):
        return featured_artist not in featured_artists and featured_artist != beginning_artist

degrees_of_separation = DegreesOfSeparation()
degrees_of_separation.main()
