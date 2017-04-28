import spotipy


class DegreesOfSeparation:

    def __init__(self):
        self.__sp = spotipy.Spotify()

    def main(self):
        beginning_artist, ending_artist = "chance the rapper", "kendrick lamar"  #retrieve_artists()
        initial_artist_graph = self.get_initial_artist_graph(beginning_artist, ending_artist)
        result = self.breadth_first_search(initial_artist_graph, beginning_artist, ending_artist)
        print(result)

    def retrieve_artists(self):
        beginning_artist = input("Name of artist to begin search: ").lower()
        ending_artist = input("Name of artist to end search: ").lower()
        return beginning_artist, ending_artist

    def get_initial_artist_graph(self, beginning_artist, ending_artist):
        featured_artists = {beginning_artist: set([])}

        results = self.__sp.search(q=beginning_artist, limit=50)
        for track in results['tracks']['items']:
            for artist in track['artists']:
                featured_artist = artist['name'].lower()

                if featured_artist == ending_artist:
                    print(track['name'])
                    return

                if featured_artist not in featured_artists:
                    featured_artists[beginning_artist].add(featured_artist)

        return featured_artists

    def breadth_first_search(self, artist_graph, starting_artist, ending_artist):
        queue = [(starting_artist, [starting_artist])]
        # iterate through queue and pick up the first elements
        while queue:
            (vertex, path) = queue.pop(0)
            # find next unique artist in associated artists graph
            not_yet_visited = artist_graph[vertex] - set(path)
            for next_artist in not_yet_visited:

                artists = artist_graph.get(next_artist, set([]))

                results = self.__sp.search(q=next_artist, limit=50)
                for track in results['tracks']['items']:
                    if len(track['artists']) > 1:
                        for artist in track['artists']:
                            featured_artist = artist['name'].lower()

                            if featured_artist == ending_artist:
                                return path + [next_artist, featured_artist]

                            if featured_artist not in artists:
                                artists.add(featured_artist)

                artist_graph[next_artist] = artists

                if next_artist == ending_artist:
                    return path + [next_artist]
                else:
                    queue.append((next_artist, path + [next_artist]))


degrees_of_separation = DegreesOfSeparation()
degrees_of_separation.main()
