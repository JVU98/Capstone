import tkinter as tk
from threading import *
from tkinter import ttk
import RPi.GPIO as GPIO
from tkinter import *
from mutagen.id3 import ID3
from mutagen.wave import WAVE
from mutagen.mp3 import MP3
import random
import time
import mutagen.id3
import datetime
import pygame
import eyed3
import os


# function for the
def threading():
    # Call work function
    t1 = Thread(target=pui)
    t1.start()


def pui():
    while True:
        # check if play button is pressed
        ply_btnstate = GPIO.input(ply_btnpin)
        if ply_btnstate:
            play_song()
            time.sleep(0.5)
        # check if pause button is pressed
        pse_btnstate = GPIO.input(pse_btnpin)
        if pse_btnstate:
            pause_song()
            time.sleep(0.5)
        # check if next button is pressed
        nxt_btnstate = GPIO.input(nxt_btnpin)
        if nxt_btnstate:
            next_song()
            time.sleep(0.5)
        # check if previous button is pressed
        prv_btnstate = GPIO.input(prv_btnpin)
        if prv_btnstate:
            prev_song()
            time.sleep(0.5)
        for i in songlist.curselection():
            selected = songlist.get(i).index()
            pygame.mixer.music.load(queuelist[selected])
        # check if volume up button is pressed
        sfl_btnstate = GPIO.input(sfl_btnpin)
        if sfl_btnstate:
            shuffle()
            time.sleep(0.5)
        

def update_gui():
    global audio_len, audio_info, pop_stat, tracklength, status, tot_min, tot_sec, tot_time

    # update play/pause button
    # if playing make button say "PAUSE" and make tag say "-Playing"
    if pop_stat == 1:
        trackstatus.config(text="~ Playing ~")
        popbtn['text'] = "PAUSE"
        trackprog['value'] += (tracklength / 2100)
    # if paused make button say "PLAY" and make tag say "-Paused"
    else:
        trackstatus.config(text="~ Paused ~")
        popbtn['text'] = "PLAY"
        trackprog['value'] = trackprog['value']
    if (status == 1) or (status == -1):
        status = 0
        trackprog['value'] = 0
        trackprog.config(maximum=tracklength)

    if pygame.mixer.music.get_pos() == -1:
        next_song()
    # update track name label
    audio_len = MP3(queuelist[0])
    audio_info = ID3(queuelist[0])
    songtrack['text'] = audio_info["TIT2"].text[0]
    tracklength = int(audio_len.info.length)
    cur_min = str(pygame.mixer.music.get_pos() // 60000)
    cur_sec = str((pygame.mixer.music.get_pos() // 1000) % 60)
    cur_time = cur_min + ":" + cur_sec.zfill(2)
    tot_min = str(tracklength // 60)
    tot_sec = str(tracklength % 60)
    tot_time = tot_min + ":" + tot_sec.zfill(2)
    song_prog.config(text=cur_time)
    song_len.config(text=tot_time)
    # run itself again after 100 ms
    root.after(100, update_gui)


# initial play and following play / pause action
def play_song():
    global pop_stat
    # Continue playing the Song
    pygame.mixer.music.unpause()
    pop_stat = 1


# initial play and following play / pause action
def pause_song():
    global pop_stat
    pygame.mixer.music.pause()
    pop_stat = 0


# initial play and following play / pause action
def pop_song():
    global pop_stat
    if pygame.mixer.music.get_busy():
        # Pause the Song
        pygame.mixer.music.pause()
        pop_stat = 0
    else:
        # Continue playing the Song
        pygame.mixer.music.unpause()
        pop_stat = 1


# previous / rewind action
def prev_song():
    global status, pop_stat
    if pygame.mixer.music.get_pos() < 10000:
        # move the previous/last song to the beginning of the
        # queuelist and move to the previous song
        queuelist.insert(0, queuelist[-1])
        queuelist.pop(-1)
        pygame.mixer.music.load(queuelist[0])
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.rewind()
    status = -1
    pop_stat = 1


# queue next action
def next_song():
    global status, pop_stat
    # move the current/first song to the end of the queuelist and
    # move to the next song
    queuelist.append(queuelist[0])
    queuelist.pop(0)
    pygame.mixer.music.load(queuelist[0])
    pygame.mixer.music.play()
    status = 1
    pop_stat = 1


def shuffle():
    global status, pop_stat
    # move the current/first song to the end of the queuelist and
    # move to the next song
    upnext = random.randint(1, len(queuelist))
    i = 0
    while i < upnext:
        queuelist.append(queuelist[0])
        queuelist.pop(0)
        i += 1
    pygame.mixer.music.load(queuelist[0])
    pygame.mixer.music.play()
    status = 1
    pop_stat = 1


def user_mode():
    root.attributes('-fullscreen', True)
    userbtn.configure(state=DISABLED)
    adminbtn.configure(state=NORMAL)
        

def admin_mode():
    real_pw = ""
    entered_pw = pw_var.get()
    if entered_pw in passcodes:
        adminbtn.configure(state=DISABLED)
        userbtn.configure(state=NORMAL)
        root.attributes('-fullscreen', False)
    else:
        user_mode()


def etr1():
    pw_var.set(pw_var.get() + str("1"))


def etr2():
    pw_var.set(pw_var.get() + str("2"))


def etr3():
    pw_var.set(pw_var.get() + str("3"))


def etr4():
    pw_var.set(pw_var.get() + str("4"))


def etr5():
    pw_var.set(pw_var.get() + str("5"))


def etr6():
    pw_var.set(pw_var.get() + str("6"))


def etr7():
    pw_var.set(pw_var.get() + str("7"))


def etr8():
    pw_var.set(pw_var.get() + str("8"))


def etr9():
    pw_var.set(pw_var.get() + str("9"))


def etr0():
    pw_var.set(pw_var.get() + str("0"))


def clear():
    pw_var.set("")


status = 0
pop_stat = 0
valid = False
queuelist = []

a_file = open("/media/pi/3135-3834/admin.txt", "r")
passcodes = []
for line in a_file:
    stripped_line = line.strip()
    passcodes.append(stripped_line)
a_file.close()
n = 0
while n < 8:
    passcodes.pop(0)
    n += 1
while n < len(passcodes):
    print(passcodes[n])
    n += 1

# Initiating Pygame
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
# Initiating Pygame Mixer
pygame.mixer.init()
pygame.mixer.get_init()
pygame.mixer.music.set_volume(1.0)

root = Tk()
root.title("MusicPlayer")
root.geometry("680x290+0+0")
pw_var = tk.StringVar()

tabs = ttk.Notebook(root)
tabs.pack(pady=10, expand=True)
# create frames
player = ttk.Frame(tabs, width=1024, height=600)
settings = ttk.Frame(tabs, width=1024, height=600)

player.pack(fill='both', expand=True)
settings.pack(fill='both', expand=True)
# add frames to notebook
tabs.add(player, text='Player')
tabs.add(settings, text='Settings')
tabs.select(settings)

# Creating the Track Frames for Song label & status label
trackframe = LabelFrame(player, text="Song Info", font=("times new roman", 15, "bold"), background="Navyblue",
                        foreground="white", bd=5, relief=GROOVE)
# Inserting Song Track Label
songtrack = ttk.Label(trackframe, text="Song Name ", font=("times new roman", 16, "bold"), background="gold",
                  foreground="red")
# Inserting Status Label
trackstatus = ttk.Label(trackframe, text="~ Paused ~", font=("times new roman", 16, "bold"), background="gold",
                    foreground="red")
# Inserting Song Progress Bar
trackprog = ttk.Progressbar(trackframe, orient="horizontal", length=400, mode="determinate", maximum=100)

# Inserting Status Label
song_prog = ttk.Label(trackframe, text="0:00", font=("times new roman", 16, "bold"), background="gold",
                  foreground="red")
# Inserting Status Label
song_len = ttk.Label(trackframe, text="0:00", font=("times new roman", 16, "bold"), background="gold",
                 foreground="red")

# label positions
trackframe.place(x=0, y=0, width=510, height=200)
songtrack.grid(row=2, column=1, columnspan=3, padx=10, pady=5)
trackstatus.grid(row=3, column=2, padx=10, pady=5)
trackprog.grid(row=4, column=1, columnspan=3, padx=10, pady=5)
song_prog.grid(row=5, column=1, padx=10, pady=5)
song_len.grid(row=5, column=3, padx=10, pady=5)

# Creating Button Frame
buttonframe = LabelFrame(player, text="Control Panel", font=("times new roman", 15, "bold"), background="grey",
                         foreground="white", bd=5, relief=GROOVE)

# Inserting Stop Button
prevbtn = Button(buttonframe, text="PREVIOUS", command=prev_song, width=10, height=1,
                 font=("times new roman", 16, "bold"), foreground="navyblue", background="pink")
# Inserting Unpause Button
popbtn = Button(buttonframe, text="PLAY", command=pop_song, width=10, height=1,
                font=("times new roman", 16, "bold"), foreground="navyblue", background="pink")
# Inserting Pause Button
nextbtn = Button(buttonframe, text="NEXT", command=next_song, width=8, height=1,
                 font=("times new roman", 16, "bold"), foreground="navyblue", background="pink")
# button positions
buttonframe.place(x=0, y=200, width=510, height=100)
prevbtn.grid(row=0, column=1, padx=10, pady=5)
popbtn.grid(row=0, column=2, padx=10, pady=5)
nextbtn.grid(row=0, column=3, padx=10, pady=5)

# Creating Songlist Frame
songsframe = LabelFrame(player, text="Song List", font=("times new roman", 15, "bold"), background="grey",
                        foreground="white", bd=5, relief=GROOVE)
# Inserting Shuffle Button
shufflebtn = Button(songsframe, text="SHUFFLE", command=shuffle, width=8, height=1,
                    font=("times new roman", 16, "bold"), foreground="navyblue", background="pink")
songsframe.place(x=450, y=0, width=510, height=560)
# Inserting scrollbar
scrol_y = Scrollbar(songsframe, orient=VERTICAL)
# Inserting Songlist listbox
songlist = Listbox(songsframe, yscrollcommand=scrol_y.set, selectbackground="gold", selectmode=SINGLE,
                   font=("times new roman", 12, "bold"), background="silver", foreground="navyblue", bd=5, relief=GROOVE)
# Applying Scrollbar to listbox
scrol_y.pack(side=RIGHT, fill=Y)
scrol_y.config(command=songlist.yview)
songlist.pack(expand=TRUE, fill=X, side=TOP)
shufflebtn.pack(fill=X, side=BOTTOM)
# Creating Controls Frame
controlsframe = LabelFrame(settings, text="Settings", font=("times new roman", 15, "bold"), background="grey",
                           foreground="white", bd=5, relief=GROOVE)

pw_label = ttk.Label(controlsframe, text="Enter the passcode and press ADMIN MODE", font=("times new roman", 16, "bold"),
                 background="gold", foreground="red")

# Create Entry Widget for password
pw_entry = ttk.Entry(controlsframe, textvariable=pw_var, show="*", width=20)

# Inserting Bluetooth Button
adminbtn = Button(controlsframe, text="ADMIN MODE", command=admin_mode, width=15, height=1,
                  font=("times new roman", 16, "bold"), foreground="navyblue", background="pink")
# Inserting Bluetooth Button
userbtn = Button(controlsframe, text="USER MODE", command=user_mode, width=15, height=1,
                 font=("times new roman", 16, "bold"), foreground="navyblue", background="pink")
controlsframe.place(x=0, y=0, width=440, height=250)
pw_label.grid(row=1, column=1, columnspan=2, padx=10, pady=5)
pw_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=5)
adminbtn.grid(row=3, column=1, padx=10, pady=5)
userbtn.grid(row=3, column=2, padx=10, pady=5)

# Creating Controls Frame
keysframe = LabelFrame(settings, text="Keypad", font=("times new roman", 15, "bold"), background="grey",
                       foreground="white", bd=5, relief=GROOVE)
# Inserting Number Pad Button
onebtn = Button(keysframe, text="1", command=etr1, width=2, height=1,
                font=("times new roman", 16, "bold"), foreground="navyblue", background="pink")
twobtn = Button(keysframe, text="2", command=etr2, width=2, height=1,
                font=("times new roman", 16, "bold"), foreground="navyblue", background="pink")
threebtn = Button(keysframe, text="3", command=etr3, width=2, height=1,
                  font=("times new roman", 16, "bold"), foreground="navyblue", background="pink")
fourbtn = Button(keysframe, text="4", command=etr4, width=2, height=1,
                 font=("times new roman", 16, "bold"), foreground="navyblue", background="pink")
fivebtn = Button(keysframe, text="5", command=etr5, width=2, height=1,
                 font=("times new roman", 16, "bold"), foreground="navyblue", background="pink")
sixbtn = Button(keysframe, text="6", command=etr6, width=2, height=1,
                font=("times new roman", 16, "bold"), foreground="navyblue", background="pink")
sevenbtn = Button(keysframe, text="7", command=etr7, width=2, height=1,
                  font=("times new roman", 16, "bold"), foreground="navyblue", background="pink")
eightbtn = Button(keysframe, text="8", command=etr8, width=2, height=1,
                  font=("times new roman", 16, "bold"), foreground="navyblue", background="pink")
ninebtn = Button(keysframe, text="9", command=etr9, width=2, height=1,
                 font=("times new roman", 16, "bold"), foreground="navyblue", background="pink")
zerobtn = Button(keysframe, text="0", command=etr0, width=2, height=1,
                 font=("times new roman", 16, "bold"), foreground="navyblue", background="pink")
clearbtn = Button(keysframe, text="X", command=clear, width=2, height=1,
                  font=("times new roman", 16, "bold"), foreground="navyblue", background="pink")

keysframe.place(x=440, y=0, width=240, height=250)
onebtn.grid(row=1, column=1, padx=20, pady=5)
twobtn.grid(row=1, column=2, pady=5)
threebtn.grid(row=1, column=3, padx=20, pady=5)
fourbtn.grid(row=2, column=1, padx=20, pady=5)
fivebtn.grid(row=2, column=2, pady=5)
sixbtn.grid(row=2, column=3, padx=20, pady=5)
sevenbtn.grid(row=3, column=1, padx=20, pady=5)
eightbtn.grid(row=3, column=2, pady=5)
ninebtn.grid(row=3, column=3, padx=20, pady=5)
zerobtn.grid(row=4, column=2, pady=5)
clearbtn.grid(row=4, column=3, padx=20, pady=5)

# Fetch Songs
# Inserting Songs into Songlist
folderpath = "/media/pi/3135-3834/Song Files/"
songtracks = os.listdir(folderpath)
# Fetch Songs
# Inserting Songs into Songlist
for track in songtracks:
    trackpath = folderpath + track
    queuelist.append(trackpath)
    audio_info = ID3(trackpath)
    trackmeta = audio_info["TIT2"].text[0] + "  -  " + audio_info["TPE1"].text[0]
    songlist.insert(END, trackmeta)
    songtrack['text'] = audio_info["TIT2"].text[0]

# Loading Selected Song
pygame.mixer.music.load(queuelist[0])
# Playing Selected Song
pygame.mixer.music.play()
pygame.mixer.music.pause()
pop_stat = 0
# Displaying Selected Song title
audio_len = MP3(queuelist[0])
audio_info = ID3(queuelist[0])
tracklength = int(audio_len.info.length)
tot_min = str(tracklength // 60)
tot_sec = str(tracklength % 60)
tot_time = tot_min + ":" + tot_sec.zfill(2)
song_len.configure(text=tot_time)
trackprog.configure(maximum=tracklength)
songtrack['text'] = audio_info["TIT2"].text[0]

GPIO.setmode(GPIO.BOARD)
# play button
ply_btnpin = 11
# pause button
pse_btnpin = 18
# next button
nxt_btnpin = 15
# previous button
prv_btnpin = 31
# shuffle button
sfl_btnpin = 35

GPIO.setup(ply_btnpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pse_btnpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(nxt_btnpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(prv_btnpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sfl_btnpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


update_gui()
threading()
root.mainloop()


# WORKING ON:
# -play function
# -play song from songlist
# -volume controls
# -pijuice power button

# NOT YET STARTED:
# -album cover

# ADDITIONAL THINGS
# -gui redesign???
