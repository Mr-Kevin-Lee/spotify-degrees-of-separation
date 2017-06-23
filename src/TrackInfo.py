class TrackInfo(object):

    def __init__(self, track_name, main_artist, featured_artist):
        self.track_name = track_name
        self.main_artist = main_artist
        self.featured_artist = featured_artist

    def __str__(self):
        return str.format("Track: {} \n  Artist: {} \n  Feature: {}",
                          self.track_name, self.main_artist, self.featured_artist)
