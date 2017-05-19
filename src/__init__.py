import spotipy
from src.TrackInfo import TrackInfo


class DegreesOfSeparation:

    def __init__(self):
        self.__sp = spotipy.Spotify()

    def main(self):
        beginning_artist, ending_artist = "Chance the Rapper", "Kendrick Lamar"  #retrieve_artists()
        result = self.perform_artist_search(str(beginning_artist).upper(), str(ending_artist).upper())
        print(result)

    def retrieve_artists(self):
        beginning_artist = input("Name of artist to begin search: ").lower()
        ending_artist = input("Name of artist to end search: ").lower()
        return beginning_artist, ending_artist

    def perform_artist_search(self, beginning_artist, ending_artist):
        featured_artists = {beginning_artist: set([])}
        temp_featured_artists = []

        results = self.__sp.search(q=beginning_artist, limit=50)
        for track in results['tracks']['items']:
            for artist in track['artists']:
                featured_artist = str(artist['name']).upper()

                if featured_artist == ending_artist:
                    return [beginning_artist, ending_artist]

                if self.can_add_artist_to_graph(featured_artist, featured_artists, temp_featured_artists, beginning_artist):
                    related_track = TrackInfo(track['name'], beginning_artist, featured_artist)
                    temp_featured_artists.append(featured_artist)
                    featured_artists[beginning_artist].add(related_track)

        return self.artist_subsearch(featured_artists, beginning_artist, ending_artist)

    def artist_subsearch(self, artist_graph, starting_artist, ending_artist):
        queue = [(starting_artist, [starting_artist])]
        # iterate through queue and pick up the first elements
        while queue:
            (vertex, path) = queue.pop(0)
            # find next unique artist in associated artists graph
            not_yet_visited = artist_graph[vertex] - set(path)

            for current_artist in not_yet_visited:
                featured_artists = self.search_for_featured_artists(artist_graph, current_artist, ending_artist, path)
                artist_graph[current_artist] = featured_artists

                if featured_artists is not None and ending_artist in featured_artists:
                    return featured_artists
                elif current_artist == ending_artist:
                    return path + [current_artist]
                else:
                    queue.append((current_artist, path + [current_artist]))

    def search_for_featured_artists(self, artist_graph, initial_artist, ending_artist, path):
        track_artists = artist_graph.get(initial_artist, set([]))

        results = self.__sp.search(q=initial_artist, limit=50)
        sorted(results['tracks']['items'], key=lambda track: (track['popularity']))

        for track in results['tracks']['items']:
            if len(track['artists']) > 1:
                for artist in track['artists']:
                    featured_artist = artist['name']

                    if str(featured_artist).lower() == str(ending_artist).lower():
                        return path + [initial_artist, featured_artist]

                    if featured_artist not in track_artists:
                        track_artists.add(featured_artist)

    def can_add_artist_to_graph(self, featured_artist, featured_artists, temp_featured_artists, beginning_artist):
        return featured_artist not in featured_artists and featured_artist not in temp_featured_artists and featured_artist != beginning_artist


degrees_of_separation = DegreesOfSeparation()
degrees_of_separation.main()
