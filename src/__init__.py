import spotipy


def main():
    # sp = spotipy.Spotify()
    # results = sp.search(q='Kendrick Lamar', limit=20)
    # for i, t in enumerate(results['tracks']['items']):
    #     print(' ', i, t['name'])
    beginning_artist, ending_artist = retrieve_artists()
    begin_search(beginning_artist, ending_artist)


def retrieve_artists():
    beginning_artist = input("Name of artist to begin search: ").lower()
    ending_artist = input("Name of artist to end search: ").lower()
    return beginning_artist, ending_artist


def begin_search(beginning_artist, ending_artist):
    sp = spotipy.Spotify()
    found_artists = {beginning_artist: set([])}
    tree_depth = 3

    results = sp.search(q=beginning_artist, limit=20)
    for index, track in enumerate(results['tracks']['items']):
        for artist in track['artists']:
            featured_artist = artist['name']

            if featured_artist in found_artists.keys():
                continue

            if featured_artist == ending_artist:
                print("found end")

            if featured_artist not in found_artists[beginning_artist]:
                found_artists[beginning_artist].add(featured_artist)

    print(found_artists)


main()
