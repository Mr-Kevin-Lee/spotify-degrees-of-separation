import spotipy

sp = spotipy.Spotify()


def breadth_first_search(artist_graph, starting_artist, ending_artist):

    queue = [(starting_artist, [starting_artist])]
    # iterate through queue and pick up the first elements
    while queue:
        (vertex, path) = queue.pop(0)
        # find next unique artist in associated artists graph
        not_yet_visited = artist_graph[vertex] - set(path)
        for next_artist in not_yet_visited:

            artists = artist_graph.get(next_artist, set([]))

            results = sp.search(q=next_artist, limit=50)
            for track in results['tracks']['items']:
                if len(track['artists']) > 1:
                    for artist in track['artists']:
                        featured_artist = artist['name'].lower()
                        print(featured_artist)

                        if featured_artist == ending_artist:
                            return path + [next_artist, featured_artist]

                        if featured_artist not in artists:
                            artists.add(featured_artist)

            artist_graph[next_artist] = artists

            if next_artist == ending_artist:
                return path + [next_artist]
            else:
                queue.append((next_artist, path + [next_artist]))


def main():
    beginning_artist, ending_artist = "chance the rapper", "the weeknd"  #retrieve_artists()
    begin_search(beginning_artist, ending_artist)


def retrieve_artists():
    beginning_artist = input("Name of artist to begin search: ").lower()
    ending_artist = input("Name of artist to end search: ").lower()
    return beginning_artist, ending_artist


def begin_search(beginning_artist, ending_artist):
    featured_artists = {beginning_artist: set([])}

    results = sp.search(q=beginning_artist, limit=50)
    for track in results['tracks']['items']:
        for artist in track['artists']:
            featured_artist = artist['name'].lower()
            # print(featured_artist)

            if featured_artist == ending_artist:
                print(track['name'])
                return

            if featured_artist not in featured_artists:
                featured_artists[beginning_artist].add(featured_artist)

    print(list(breadth_first_search(featured_artists, beginning_artist, ending_artist)))

main()
