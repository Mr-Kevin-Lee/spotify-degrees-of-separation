# Degrees of Separation of Music Artists

This is a project based on the idea, <a href="https://en.wikipedia.org/wiki/Six_degrees_of_separation">Six Degrees of Separation</a>, written
in Python and using the Spotipy library. Works well with your favorite rappers!

![](https://media.giphy.com/media/7prA745iHHzgY/giphy.gif)

## TODO
- Optimize BFS
- Sort returned tracks by relevance
- Optimize number of elements returned in each search
- Create Track class to display additional information e.g. track title
- Change from Spotify API to Genius API (down the road)
    - Things it offers that Spotify doesn't (AFAIK):
        - Images
        - Producers
        - Samples
        - Covered by
        - Remixed by
        - And probably a whole lot more!
- BUG FIXES:
    - main function executing is TWICE
- REFACTOR:
    - Remove duplicate code