import numpy as np
import random
import time
from tkinter import *
import tkinter.font as tkfont
from PIL import Image, ImageTk

cmds = ['Play/Pause song', 'Previous song', 'Next song', 'Turn up the volume', 'Turn down the volume', 'Answer a call', 'Reject a call', 'Open an app with voice', 'Take voice note', 'Check the weather', 'Read a message', 'Reply a message']
taps = ['2345-0-2345', '3-2', '2-3', '2-0-2', '3-0-3', '23-0-23', '4-0-4', '4-3-2', '3-2-4', '3-2-3', '2-4-2', '4-2-4']

N_TRAIN		= 1
N_TEST_DAY1	= 4
N_TEST_DAY2	= 4
N 			= len(cmds)

block = 0
index = 0
phase = 0

config_type = 0
config_day = 1

order = list(range(0, N))
start = False
block_break = 0
f = None

def record(info=None, tag=None):
	global block
	global index
	global phase
	global f
	t = time.time()
	if info is not None:
		f.write(str(t) + ' ' + tag + ' ' + str(info) + '\n')
	else:
		f.write(str(t) + ' trial ' + str(block) + ' ' + str(index) + ' ' + str(phase) + '\n')

def renew_interface():
	global block
	global index
	global phase
	global config_type
	global config_day
	global order
	global block_break
	if block_break > 0:
		if block_break == 1:
			label_process.configure(text='Have a break')
			record('', 'break')
		else:
			label_process.configure(text="Finish " + ('day 1' if config_day == 1 else 'day 2'))
		label_cmd.configure(text='')
		label_tap.configure(text='')
		label_ges.configure(image=pics[N])
	else:
		if block >= N_TRAIN: record()
		s = 'Test' if block >= N_TRAIN else 'Train'
		label_process.configure(text=s + ':  Block ' + str(block) + '  Command ' + str(index))
		label_cmd.configure(text=cmds[order[index]])
		if config_type == 0:
			if phase == 0:
				label_tap.configure(text='')
			else:
				label_tap.configure(text=taps[order[index]])
			label_ges.configure(image=pics[N])
		else:
			label_tap.configure(text='')
			if phase == 0:
				label_ges.configure(image=pics[N])
			else:
				label_ges.configure(image=pics[order[index]])

def key_func(event):
	global block
	global index
	global phase
	global config_day
	global order
	global start
	global block_break
	if not start: return

	if block_break == 1:
		block_break = 0
	else:
		if block >= N_TRAIN:
			phase += 1
		else:
			index += 1
		if phase > 1:
			index += 1
			phase = 0
		if index >= N:
			block += 1
			index = 0
			phase = 0
			random.shuffle(order)
			record(order, 'order')
			block_break = 1
		if config_day == 1:
			if block >= N_TRAIN + N_TEST_DAY1:
				block_break = 2
				start = False
				f.close()
		else:
			if block >= N_TRAIN + N_TEST_DAY1 + N_TEST_DAY2:
				block_break = 2
				start = False
				f.close()
	renew_interface()

def button_start_onclick():
	global block
	global index
	global phase
	global config_type
	global config_day
	global start
	global block_break
	global f
	if start: return
	config_type = var_type.get()
	config_day = var_day.get()
	random.shuffle(order)
	f = open('memory-' + entry_name.get() + '-' + ('tap' if config_type == 0 else 'ges') + '-day' + str(config_day) + '.txt', 'a')
	record('', 'start')
	if config_day == 1:
		block = 0
		index = 0
		phase = 1
	else:
		block = N_TRAIN + N_TEST_DAY1
		index = 0
		phase = 0
		record(order, 'order')
	start = True
	block_break = 0
	renew_interface()

def resize(img):
	w, h = img.size
	k = 100 / h
	w = int(w * k)
	h = int(h * k)
	return ImageTk.PhotoImage(img.resize((w, h), Image.ANTIALIAS))


# window
win = Tk()
win.title("exp")
win.geometry("400x400+200+20")
win.bind("<Key>", key_func)
pics = [resize(Image.open('pics2/' + str(i) + '.gif')) for i in range(N+1)]

# top
frame_top = Frame(win)
button_start = Button(frame_top, text='Start', command=button_start_onclick)
button_start.pack(side=LEFT)
entry_name = Entry(frame_top, width=10)
entry_name.pack()
frame_top.pack()

# type
frame_config = Frame(win)
var_type = IntVar()
group_type = LabelFrame(frame_config, text='type')
group_type.pack(side=LEFT)
Radiobutton(group_type, text='Tap', variable=var_type, value=0).pack(anchor=W)
Radiobutton(group_type, text='Gesture', variable=var_type, value=1).pack(anchor=W)

# day
var_day = IntVar()
group_day = LabelFrame(frame_config, text='day')
group_day.pack()
Radiobutton(group_day, text='Day 1', variable=var_day, value=1).pack(anchor=W)
Radiobutton(group_day, text='Day 2', variable=var_day, value=2).pack(anchor=W)
frame_config.pack()

# process
label_process = Label(win, text='not start', font=tkfont.Font(size=20))
label_process.pack()

# margin
Label(win, text='').pack()
Label(win, text='').pack()

# command
label_cmd = Label(win, text='', font=tkfont.Font(size=20))
label_cmd.pack()

# tap
label_tap = Label(win, text='', font=tkfont.Font(size=20))
label_tap.pack()

# gesture
label_ges = Label(win, image=pics[N])
label_ges.pack()

win.mainloop()