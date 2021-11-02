# vlc_random_chapters
Script to play random chapters from movies located in a directory. Written for Linux

Change variable "media_path" to point to where your movie directory resides.

The script should randomly select any .mkv or .avi files within media_path and play a random chapter from that file. Once the chapter ends, or the space bar is pressed, another random move and chapter will begin. 
To stop the script, use mouse to minimize vlc window and exit the player.
To-Do:
1. add thread to watch for "escape" to gracefully exit program.
2. force subtitles off by default 
