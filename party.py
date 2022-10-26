import random
import time
import vlc
import pathlib
import threading
from pynput import keyboard

skip_signal = False
terminate_signal = False

movie_dir = pathlib.Path('/opt/movies')
#movie_dir = pathlib.Path('smb://192.168.1.87/storage/Movies')
#namesList = ['How_The_Grinch_Stole_Christmas', "Santa_Claus_Is_Comin'", 'Rudolph_The_Red', 'Gremlins', 'Home_Alone', 'A_Christmas_Story', 'Christmas_Vacation', 'Krampus', 'Batman_Returns', 'Nightmare_Before_Christmas']
namesDic = {'How_The_Grinch_Stole_Christmas': [[1]], "Santa_Claus_Is_Comin'": [[2]], 'Nightmare_Before_Christmas': [[2,4]]}
#def input_thread(skip_signal):
#    while True:
#        keyboard.wait('space') 
#        skip_signal.set()
#        time.sleep(3)
#        skip_signal.clear()
def on_press(key):
    global skip_signal
    global terminate_signal
    if key == keyboard.Key.space:
        skip_signal = True
        time.sleep(3)
    elif key == keyboard.Key.esc:
        terminate_signal = True
        return False


def play_movie_chapters(movie_dir):
    global skip_signal
    global terminate_signal
    playing = True
    media_player = vlc.MediaPlayer()
    media_player.set_fullscreen(True)
#    christmas_paths_list = []
    for name in namesDic.keys():
        for path in movie_dir.glob(f'**/*{name}*.mkv'):
            namesDic[name].append(path)

        
#    movies_directory_list = movie_dir.glob('**/*')
#    movies_path_list = [movie for movie in movies_directory_list if movie.suffix in EXTENSIONS]
    print(namesDic)
    while playing:
        skip_signal = False
        random_movie_key = random.choice(list(namesDic.keys()))
        movie_path = namesDic[random_movie_key][1]
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
        elif len(namesDic[random_movie_key][0]) > 0:
            chapters_list = namesDic[random_movie_key][0]
            random_chapter = random.choice(chapters_list)
            media_player.set_chapter(random_chapter)
        else:
            random_chapter = random.randint(1,num_chapters-1)
            print("Current chapter: " + str(random_chapter))
            media_player.set_chapter(random_chapter)
        current_chapter = random_chapter
        time.sleep(2)
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
play_thread = threading.Thread(target=play_movie_chapters, args=(movie_dir,))
listener = keyboard.Listener(on_press=on_press)
play_thread.start()
listener.start()

play_thread.join()
listener.join()
