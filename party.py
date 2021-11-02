import random
import time
import vlc
import pathlib
import threading
import keyboard

media_path = pathlib.Path('/opt/movies')
def input_thread(skip_signal):
    while True:
        keyboard.wait('space') 
        skip_signal.set()
        time.sleep(3)
        skip_signal.clear()

def play_movie_chapters(media_path, skip_signal):

    media_player = vlc.MediaPlayer()
    media_player.set_fullscreen(True)
    EXTENSIONS = {'.mkv', '.avi'}
    movies_directory_list = media_path.glob('**/*')
    movies_path_list = [movie for movie in movies_directory_list if movie.suffix in EXTENSIONS]
    print(movies_path_list)
    while True:
        movie_path_idx = random.randint(0,len(movies_path_list)-1)
        print(movies_path_list[movie_path_idx])
        media = vlc.Media(movies_path_list[movie_path_idx])
        media_player.set_media(media)
        media_player.play()
        loading = True
        while loading:
            time.sleep(1)
            if media_player.get_state() == vlc.State.Playing:
                loading = False
        num_chapters = media_player.get_chapter_count()
        print("Number of chapters: " + str(num_chapters))
        if num_chapters == 0:
            media_player.set_chapter(0)
            random_chapter = 0
        else:
            random_chapter = random.randint(1,num_chapters)
            print("Current chapter: " + str(random_chapter))
            media_player.set_chapter(random_chapter)
        current_chapter = random_chapter
        time.sleep(2)        
        same_chapter = True
        while same_chapter:
            time.sleep(1)  
            current_chapter = media_player.get_chapter()
            if current_chapter != random_chapter or skip_signal.is_set():
                same_chapter = False


skip_signal = threading.Event()
play_thread = threading.Thread(target=play_movie_chapters, args=(media_path, skip_signal,))
listener = threading.Thread(target=input_thread, args=(skip_signal,))
play_thread.start()
listener.start()

play_thread.join()
listener.join()
