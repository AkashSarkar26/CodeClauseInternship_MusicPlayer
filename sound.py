from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import turtle
import tkinter.ttk as ttk
root=Tk()
root.config(bg="Light blue")
root.title('Music Player')
root.geometry("500x400")
pygame.mixer.init()
def play_time():
    if stopped:
        return
    cur_time=pygame.mixer.music.get_pos()/1000
    #slider_label.config(text=f'Slider: {int(my_slider.get())} and Song Pos:{int(cur_time)}')
    converted_current_time=time.strftime('%M:%S',time.gmtime(cur_time))
    #current_song= song_box.curselection()
    song = song_box.get(ACTIVE)
    song = f'C:/Users/User/Desktop/audio/{song}.mp3'
    song_mut=MP3(song)
    global  song_length
    song_length=song_mut.info.length
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
    cur_time += 1
    if int(my_slider.get()==int(song_length)):
        status_bar.config(text=f'Time Elapsed: {converted_song_length} ')
    elif paused:
        pass
    elif int(my_slider.get())==int(cur_time):
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(cur_time))
    else:
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length} ')
        #move this thing by one second
        next_time=int(my_slider.get())+1
        my_slider.config(value=next_time)
    #update slider position value to current song position
    #my_slider.config(value=int(cur_time))
    #update time
    status_bar.after(1000,play_time)
def add_song():
    song=filedialog.askopenfilename(initialdir='audio/',title="choose a song",filetypes=(("mp3 files","*.mp3"),))
    #print(song)
    song=song.replace("C:/Users/User/Desktop/audio/","")
    song = song.replace(".mp3", "")
    song = song.replace("320 Kbps", "")
  #add song to listbox
    song_box.insert(END,song)
#add many song to playlist
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='audio/', title="choose a song", filetypes=(("mp3 files", "*.mp3"),))
    #loop through song list
    for song in songs:
        song = song.replace("C:/Users/User/Desktop/audio/", "")
        song = song.replace(".mp3", "")
        song = song.replace("320 Kbps", "")
        #insert into playlist
        song_box.insert(END, song)

    #play selected song
def play():
    global stopped
    stopped=False
    song=song_box.get(ACTIVE)
    song=f'C:/Users/User/Desktop/audio/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #call the play_time funtion to get song length
    play_time()
    #update slider to position
    #slider_position=int(song_length)
    #my_slider.config(to=slider_position,value=0)
#Stop the song
global stopped
stopped=False
def stop():
    status_bar.config(text='')
    my_slider.config(value=0)
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    status_bar.config(text='')
    global stopped
    stopped=True

   #play the next song in playlist
def next_song():
     status_bar.config(text='')
     my_slider.config(value=0)
    #get the current song tuple number
     next_one=song_box.curselection()
     next_one=next_one[0]+1
     song=song_box.get(next_one)
     song = f'C:/Users/User/Desktop/audio/{song}.mp3'
     pygame.mixer.music.load(song)
     pygame.mixer.music.play(loops=0)
     #Move active bar
     song_box.selection_clear(0,END)
     #activate new song bars
     song_box.activate(next_one)
     #set bar
     song_box.selection_set(next_one,last=None)
def prev_song():
    status_bar.config(text='')
    my_slider.config(value=0)
    next_one = song_box.curselection()
    next_one = next_one[0] - 1
    song = song_box.get(next_one)
    song = f'C:/Users/User/Desktop/audio/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # Move active bar
    song_box.selection_clear(0, END)
    # activate new song bars
    song_box.activate(next_one)
    # set bar
    song_box.selection_set(next_one, last=None)

#create global pause veriable
global paused
paused=False
def delete_song():
    stop()
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

def delete_all_songs():
    stop()
    song_box.delete(0,END)
    pygame.mixer.music.stop()
def pause(is_paused):
    # pause unpause the current song
    global paused
    paused=is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused=False
    else:
        pygame.mixer.music.pause()
        paused=True
    #unpause
#create slider function
def slide(x):
    #slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
    song = song_box.get(ACTIVE)
    song = f'C:/Users/User/Desktop/audio/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0,start=int(my_slider.get()))

#creating listbox
song_box=Listbox(root,bg="black",fg="green",width=60,selectbackground="gray",selectforeground="black")
song_box.pack(pady=20)
#create player control buttons
back_btn_img=PhotoImage(file='buttons/previous.png')
forw_btn_img=PhotoImage(file='buttons/next-button.png')
play_btn_img=PhotoImage(file='buttons/play.png')
pause_btn_img=PhotoImage(file='buttons/pause.png')
stop_btn_img=PhotoImage(file='buttons/stop-button.png')
#create player control frame
controls_frame=Frame(root)
controls_frame.pack()
back_button=Button(controls_frame,image=back_btn_img,borderwidth=0,command=prev_song)
forward_button=Button(controls_frame,image=forw_btn_img,borderwidth=0,command=next_song)
play_button=Button(controls_frame,image=play_btn_img,borderwidth=0,command=play)
pause_button=Button(controls_frame,image=pause_btn_img,borderwidth=0,command=lambda :pause(paused))
stop_button=Button(controls_frame,image=stop_btn_img,borderwidth=0,command=stop)

back_button.grid(row=0,column=0,padx=20)
forward_button.grid(row=0,column=1,padx=20)
play_button.grid(row=0,column=2,padx=20)
pause_button.grid(row=0,column=3,padx=20)
stop_button.grid(row=0,column=4,padx=20)
#create menu
my_menu=Menu(root)
root.config(menu=my_menu)
#add song
add_song_menu=Menu(my_menu)
my_menu.add_cascade(label="Add songs",menu=add_song_menu)
add_song_menu.add_command(label="Add one song to playlist",command=add_song)
#add many song
add_song_menu.add_command(label="Add many song to playlist",command=add_many_songs)
#create a delete song menu
remove_song_menu=Menu(my_menu)
my_menu.add_cascade(label="Remove songs",menu=remove_song_menu)
remove_song_menu.add_command(label="Delete a song",command=delete_song)
remove_song_menu.add_command(label="Delete all songs",command=delete_all_songs)
#create statusbar
status_bar=Label(root,text='',bd=1,relief=GROOVE,anchor=E)
status_bar.pack(fill=X,side=BOTTOM,ipady=2)
my_slider=ttk.Scale(root,from_=0,to=100,orient=HORIZONTAL,value=0,command=slide,length=340)
my_slider.pack(pady=30)
#create slider label
#slider_label=Label(root,text="0")
#slider_label.pack(pady=10)
root.mainloop()