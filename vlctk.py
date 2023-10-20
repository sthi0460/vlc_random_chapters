import random
import time
import vlc
import pathlib
import threading
import tkinter as tk
from tkinter import ttk
import  pickle
global skip_signal
global terminate_signal
import asyncio

def pressed_space(event):
    global skip_signal
    skip_signal = True
    #time.sleep(3)

def pressed_esc(event):
	global terminate_signal
	terminate_signal = True
	root.destroy()

def play_chapters(namesDic):
	global skip_signal
	global terminate_signal
	
	playing = True
	print(str(tk_frame.winfo_id()))
	

	while playing:
		skip_signal = False
		random_movie_key = random.choice(list(namesDic.keys()))
		movie_path = namesDic[random_movie_key][1]
		print(movie_path)
		media = vlc.Media(movie_path)
		media_player.set_media(media)
		media_player.play()
		media_player.set_fullscreen(True)
		#media_player.toggle_fullscreen()
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
			random_chapter = random.choice(chapters_list) - 1
			media_player.set_chapter(random_chapter)
		else:
			random_chapter = random.randint(1,num_chapters-1)
			print("Current chapter: " + str(random_chapter))
			media_player.set_chapter(random_chapter)
		#media_player.toggle_fullscreen()
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

	
skip_signal = False
terminate_signal = False

movie_dir = pathlib.Path('/opt/movies')
with open('HalloweenMovies2022.pickle', 'rb') as handle:
    namesDic = pickle.load(handle)
print(namesDic)    
root = tk.Tk()
#root.overrideredirect(False)
root.attributes('-fullscreen', True)
#tk_frame = ttk.Frame(root, width=8000, height=8000)
tk_frame = ttk.Frame(root)
media_player = vlc.MediaPlayer('--vout mmal_vout')
media_player.set_xwindow(root.winfo_id())
root.bind('<space>', pressed_space)
root.bind('<Escape>', pressed_esc)
root.bind('p', play_chapters)
player_thread = threading.Thread(target=play_chapters, args=(namesDic,))
player_thread.start()
#root.focus_set()
root.mainloop()
#player_thread.join()


