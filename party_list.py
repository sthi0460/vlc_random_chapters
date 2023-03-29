import random
import time
import vlc
import pathlib
import threading
from pynput import keyboard
import  pickle
from unique_chap_list import gen_unique_chap_list
skip_signal = False
terminate_signal = False

# Path to movie pickle
path = pathlib.Path('/home/stephen/Projects/vlc_random_chapters/MoviePickle.pickle')

unique_chap_list = gen_unique_chap_list(path)


def on_press(key):
    global skip_signal
    global terminate_signal
    if key == keyboard.Key.space:
        skip_signal = True
        time.sleep(3)
    elif key == keyboard.Key.esc:
        terminate_signal = True
        return False


def play_movie_chapters(unique_chap_list):
    global skip_signal
    global terminate_signal
    playing = True
    media_player = vlc.MediaPlayer()
    media_player.set_fullscreen(True)

    while playing:
        for movie in unique_chap_list:
            if not playing:
                break
            skip_signal = False
            movie_path = movie[2]
            print(movie_path)
            media = vlc.Media(movie_path)
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
            elif movie[1]-1 >= 0 and movie[1] <num_chapters:
                random_chapter = movie[1]-1
                media_player.set_chapter(random_chapter)
            else:
                random_chapter = random.randint(1,num_chapters-1)
                print("Current chapter: " + str(random_chapter))
                media_player.set_chapter(random_chapter)
            current_chapter = random_chapter
            time.sleep(1)
            media_player.video_set_spu(-1)
            same_chapter = True
            while same_chapter:
                time.sleep(3)  
                current_chapter = media_player.get_chapter()
                if terminate_signal == True:
                    playing = False
                    break
                elif current_chapter != random_chapter or skip_signal == True:
                    same_chapter = False
                    skip_signal = False


#skip_signal = threading.Event()
#terminate_signal = threading.Event()
play_thread = threading.Thread(target=play_movie_chapters, args=(unique_chap_list,))
listener = keyboard.Listener(on_press=on_press)
play_thread.start()
listener.start()

play_thread.join()
listener.join()
