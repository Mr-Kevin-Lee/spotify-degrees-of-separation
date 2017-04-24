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
    found_artists = {}

    results = sp.search(q=beginning_artist, limit=50)
    for index, track in enumerate(results['tracks']['items']):
        print('Track: ', track['name'])
        for artist in track['artists']:
            print(' Artist: ', artist['name'])


main()
