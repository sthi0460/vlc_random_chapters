import vlc
import time
import pathlib

media_path = pathlib.Path('/home/stephen/Videos/Hocus_Pocus (1993).mkv')
media_player = vlc.MediaPlayer()
media = vlc.Media(media_path)
media_player.set_media(media)
media_player.set_chapter(3)


media_player.play()
value = media_player.video_get_spu_count()
print(value)
media_player.set_chapter(3)
value = media_player.video_get_spu()
print(value)
time.sleep(2)
media_player.video_set_spu(-1)
value = media_player.video_get_spu()
print(value)
time.sleep(100)
