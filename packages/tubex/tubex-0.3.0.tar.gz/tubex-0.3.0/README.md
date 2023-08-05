# Tubex

A simple Command Line Interface to download mp3 from youtube and mp4 from oreilly.

```
tubex download-mp3 <youtube_playlist_url> --album <album_name> --artist <artist_name>
tubex --username <username> --password <password> download-oreilly <oreilly_learning_url>
```

## Example
```bash

# To learn more about pipx: https://github.com/pipxproject/pipx
$ pipx install tubex
$ pipx upgrade tubex

# Download mp3
$ tubex download-mp3 \
    https://www.youtube.com/playlist?list=PLSdmnemG6jbv1-GRf23jwDsYWkjz7mblP \
    --album test --artist mixed
 
# Enjoy the music (e.g using `vlc`)
$ vlc tubex_out

# Download mp4 (video) 
$ tubex --outdir 20210110 download-mp4 https://www.youtube.com/watch?v=aUrmkKDJ1t8

# Download oreilly
$ tubex --username <username> --password <password> \
    download-oreilly https://learning.oreilly.com/videos/modern-python-livelessons/9780134743400
    
# Enjoy learning
$ vlc tubex_out/Modern_Python_LiveLessons_-_Big_Ideas_and_Little_Code_in_Python/

```

