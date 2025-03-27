from PIL import Image, ImageTk
from pythonosc.udp_client import SimpleUDPClient
import tkinter
import customtkinter
import sys
import random
import time
import os
from imageProcessor import *


if os.environ.get('DISPLAY','') == '':
    print('no display found. Using 127.0.0.1:0.0')
    os.environ.__setitem__('DISPLAY', '127.0.0.1:0.0')

root = customtkinter.CTk()
root.title('RGBeats')
root.geometry('1200x1000')
# GUI and event handling code

radio_var = tkinter.IntVar(0)
radio_var.set(2)

order_var = tkinter.IntVar(0)
comp_var = tkinter.IntVar(0)
comp_var.set(value=1)

def comp_event(variable):
    image_processor = ImageProcessor('og.png')
    resized_image = image_processor.resize(comp_var.get())
    resized_image.save('compressed_image.png', optimize=True, quality=50)
    pic = customtkinter.CTkImage(resized_image, size=image_processor.get_size())
    imag.configure(image=pic)

amp_switch_var = tkinter.IntVar(0)

def amp_switch_event():
    if amp_switch_var.get() == 1:
        amp_switch.configure(text=" Randomized Amplitudes Enabled")
        range_max.configure(state="normal", button_color="#2FA572", progress_color="#AAB0B5")
        range_min.configure(state="normal", button_color="#2FA572", progress_color="#AAB0B5")
        min_label.configure(text_color="#C0C7D0")
        max_label.configure(text_color="#C0C7D0")
    else:
        amp_switch.configure(text=" Randomized Amplitudes Disabled")
        range_max.configure(state="disabled", button_color="#164f36", progress_color="#333d39")
        range_min.configure(state="disabled", button_color="#164f36", progress_color="#333d39")
        min_label.configure(text_color="#4A4D50")
        max_label.configure(text_color="#4A4D50")

range_slider_min_var = tkinter.IntVar(0)
range_slider_max_var = tkinter.IntVar(0)
range_slider_max_var.set(155)

def range_event(value):
    if range_slider_max_var.get() <= range_slider_min_var.get():
        range_slider_max_var.set(range_slider_min_var.get()+1)
    range_max.configure(from_=range_slider_min_var.get())
    min_val.configure(text=str(range_slider_min_var.get()))
    max_val.configure(text=str(range_slider_max_var.get()))

oct_button_var = tkinter.IntVar(0)
oct_button_var.set(value=1)
del_button_var = tkinter.DoubleVar(0)
del_button_var.set(value=0.1)

def segmented_button_event(value):
    print("segmented button clicked:", oct_button_var.get())

def imageUploader():
    fileTypes = [("Image files", "*.png;*.jpg;*.jpeg")]
    path = tkinter.filedialog.askopenfilename(filetypes=fileTypes)

    if len(path):
        image_processor = ImageProcessor(path)
        image_processor.save_image('og.png')
        resized_image = image_processor.resize(comp_var.get())
        resized_image.save('compressed_image.png', optimize=True, quality=50)
        pic = customtkinter.CTkImage(resized_image, size=image_processor.get_size())
        imag.configure(image=pic)

ip = sys.argv[1]
sending_to_port = int(sys.argv[2])
py_to_pd_OscSender = SimpleUDPClient(ip, sending_to_port)

def play():
    colors = []
    if radio_var.get() == 2:
        colors = [(0, (0, 0, 0)),  
              (1, (255, 255, 255))]

    elif radio_var.get() == 5:
        colors = [(0, (0, 0, 0)), 
              (1, (255, 255, 255)), 
              (2, (0, 255, 0)), 
              (3, (0, 0, 255)),  
              (4, (255, 0, 0))]

    elif radio_var.get() == 8:
        colors = [(0, (0, 0, 0)), 
              (1, (255, 255, 255)), 
              (2, (0, 255, 0)), 
              (3, (0, 0, 255)), 
              (4, (255, 0, 0)),
              (5, (255, 255, 0)), 
              (7, (0, 255, 255)), 
              (7, (255, 0, 255))  ]
    
    colors_bw = [None]*int(radio_var.get())
    colors_bw[0] = (0, 0, 0)
    for i in range(int(radio_var.get())):
        temp = int(255*(float(i)/int(radio_var.get())))
        if (i + 1 < len(colors_bw)): colors_bw[i + 1] = (temp, temp, temp)
    colors_bw[int(radio_var.get()) - 1] = (255, 255, 255)

    image_processor = ImageProcessor('compressed_image.png')
    w, h = image_processor.get_size()
    print(f"Sending OSC | /on/1")
    py_to_pd_OscSender.send_message("/on", 1)
    print(f"Sending OSC | /delay/{del_button_var.get()} | /octave/{oct_button_var.get()}")
    notes = [1, 16.35, 18.35, 20.6, 21.83, 24.5, 27.5, 30.87, 32.7]
    note_str = "1 "
    for i in range(1, len(notes)):
        notes[i] = int(notes[i]*2**(oct_button_var.get()))
    py_to_pd_OscSender.send_message("/delay", del_button_var.get())
    py_to_pd_OscSender.send_message("/octave", notes)
    
    i = 0
    while(i < h):
        j = 0
        while(j < w):
            root.update()
            if (order_var.get() != 0):
                print("Pixel with RGBA values {} at coordinate {}".format(image_processor.get_pixel(j, i), (j, i)))
                pan = 2*(float(j)/w) - 1
                amp = int(image_processor.get_pixel(j, i)[3] * 157 / float(255))
                color = find_color(image_processor.get_pixel(j, i), image_processor, colors_bw, colors)
                if (not image_processor.is_grey_scale()):  offset = distance(image_processor.get_pixel(j, i), colors[color][1])
                else: 
                    offset = distance(image_processor.get_pixel(j, i), colors_bw[color])
            else:
                k = random.randrange(0, h)
                l = random.randrange(0, w)
                print("Pixel with RGBA values {} at coordinate {}".format(image_processor.get_pixel(l, k), (l, k)))
                pan = 2*(float(l)/w) - 1
                amp = int(image_processor.get_pixel(l, k)[3] * 157 / float(255))
                color = find_color(image_processor.get_pixel(l, k), image_processor, colors_bw, colors)
                if (not image_processor.is_grey_scale()):  offset = distance(image_processor.get_pixel(l, k), colors[color][1])
                else: offset = distance(image_processor.get_pixel(l, k), colors_bw[color])
            if (range_slider_max_var.get() != -1): amp = int(random.randrange(range_slider_min_var.get(), range_slider_max_var.get()))
            print(f"Sending OSC | /note/amp/{amp} | /note/pan/{pan} | /note/color/{color} | /note/offset/{offset}")
            py_to_pd_OscSender.send_message("/note/pan", pan)
            py_to_pd_OscSender.send_message("/note/amp", amp)
            py_to_pd_OscSender.send_message("/note/color", color)
            py_to_pd_OscSender.send_message("/note/offset", offset)
            j += 1
            time.sleep(del_button_var.get())
        i += 1

    print(f"Sending OSC | /on/0")
    py_to_pd_OscSender.send_message("/on", 0)

def stop():
    print(f"Sending OSC | /on/0")
    py_to_pd_OscSender.send_message("/on", 0)

if __name__ == "__main__":

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("green")
    button_frame = customtkinter.CTkFrame(master=root, width=400, height=200)
    button_frame.place(relx=0.55, rely=0.66, relheight=0.3)
    button_frame.pack_propagate(0)
    col_frame = customtkinter.CTkFrame(master=button_frame, width=300, height=300)
    col_frame.pack(fill="both", padx=20, pady=20)
    read_frame = customtkinter.CTkFrame(master=button_frame, width=300, height=300)
    read_frame.pack(fill="both", padx=20, pady=20)
    amp_frame = customtkinter.CTkFrame(master=root, width=400, height=420)
    amp_frame.place(relx=0.55, rely=0.05)
    amp_frame.pack_propagate(0)
    min_frame = customtkinter.CTkFrame(master=amp_frame, width=300, height=300)
    min_frame.place(relx=0.05, rely=0.15, relwidth=0.4)
    max_frame = customtkinter.CTkFrame(master=amp_frame, width=300, height=300)
    max_frame.place(relx=0.55, rely=0.15, relwidth=0.4)
    seg_frame = customtkinter.CTkFrame(master=root, width=515, height=300)
    seg_frame.place(relx=0.113, rely=0.66, relheight=0.3)
    seg_frame.pack_propagate(0)
    comp_frame = customtkinter.CTkFrame(master=seg_frame, width=300, height=300)
    col_frame.pack(fill="both", padx=20, pady=20)
    oct_frame = customtkinter.CTkFrame(master=seg_frame, width=300, height=300)
    oct_frame.pack(fill="both", padx=20, pady=20)
    del_frame = customtkinter.CTkFrame(master=seg_frame, width=300, height=300)
    del_frame.pack(fill="both", padx=20, pady=20)
    play_pause_frame = customtkinter.CTkFrame(master=root, width=515, height=45)
    play_pause_frame.place(relx=0.113, rely=0.05)
    play_pause_frame.pack_propagate(0)
    img_frame = customtkinter.CTkFrame(master=root, width=515, height=367)
    img_frame.place(relx=0.113, rely=0.125)
    img_frame.pack_propagate(0)

    color_label = customtkinter.CTkLabel(col_frame, text="Select a color count: ")
    color_label.configure(fg_color="transparent")

    color_1 = customtkinter.CTkRadioButton(master=col_frame, text="2", variable=radio_var, value=2)
    color_2 = customtkinter.CTkRadioButton(master=col_frame, text="5", variable=radio_var, value=5)
    color_3 = customtkinter.CTkRadioButton(master=col_frame, text="8", variable=radio_var, value=8)

    order_label = customtkinter.CTkLabel(read_frame, text="Select a read order: ")
    order_label.configure(fg_color="transparent")

    order_1 = customtkinter.CTkRadioButton(master=read_frame, text="Random", variable=order_var, value=0)
    order_2 = customtkinter.CTkRadioButton(master=read_frame, text="Left to Right", variable=order_var, value=1)
    order_3 = customtkinter.CTkRadioButton(master=read_frame, text="Smooth", variable=order_var, value=-1)

    amp_switch_var = customtkinter.IntVar(value=1)
    amp_switch = customtkinter.CTkSwitch(amp_frame, text="Randomized Amplitudes Enabled", command=amp_switch_event,
                                        variable=amp_switch_var, onvalue=1, offvalue=0)

    min_label = customtkinter.CTkLabel(min_frame, text="Minimum Amplitude", fg_color="transparent")
    max_label = customtkinter.CTkLabel(max_frame, text="Maximum Amplitude", fg_color="transparent")
    min_val = customtkinter.CTkLabel(min_frame, text="0", fg_color="transparent")
    max_val = customtkinter.CTkLabel(max_frame, text="155", fg_color="transparent")
    range_min = customtkinter.CTkSlider(min_frame, from_=0, to=154, command=range_event, variable=range_slider_min_var, orientation="vertical")
    range_max = customtkinter.CTkSlider(max_frame, from_=range_slider_min_var.get(), to=155, command=range_event, variable=range_slider_max_var, orientation="vertical")

    comp_label = customtkinter.CTkLabel(comp_frame, text="Select a compression factor:", fg_color="transparent")
    compression = customtkinter.CTkSegmentedButton(comp_frame, values=[1, 2, 4, 8, 16, 32, 64, 128], command=comp_event, variable=comp_var)

    oct_label = customtkinter.CTkLabel(oct_frame, text="Select an octave:", fg_color="transparent")
    oct_button = customtkinter.CTkSegmentedButton(oct_frame, values=[1, 2, 3, 4, 5, 6, 7, 8], variable=oct_button_var)

    del_label = customtkinter.CTkLabel(del_frame, text="Select a note delay:", fg_color="transparent")
    del_button = customtkinter.CTkSegmentedButton(del_frame, values=[0.1, 0.25, 0.5, 0.75, 1, 1.5, 2, 4], variable=del_button_var)
    imag = customtkinter.CTkLabel(img_frame, text=" ", fg_color="transparent")

    uploadButton = customtkinter.CTkButton(play_pause_frame, text="Upload Image", command=imageUploader)
    uploadButton.place(relx=0.025, rely=0.15, relwidth=0.3)
    playButton = customtkinter.CTkButton(play_pause_frame, text="Play", command=play)
    playButton.place(relx=0.35, rely=0.15, relwidth=0.3)
    stopButton = customtkinter.CTkButton(play_pause_frame, text="Stop", command=stop)
    stopButton.place(relx=0.675, rely=0.15, relwidth=0.3)

    img = Image.open('compressed_image.png')
    w, h = img.size
    imag.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.6 * (h / w))

    color_label.pack(side="top", padx=20, pady=10)
    order_label.pack(side="top", padx=20, pady=10)
    color_1.pack(side="top", padx=20, pady=10)
    order_1.pack(side="top", padx=20, pady=10)
    color_2.pack(side="top", padx=20, pady=10)
    order_2.pack(side="top", padx=20, pady=10)
    color_3.pack(side="top", padx=20, pady=10)
    order_3.pack(side="top", padx=20, pady=10)
    col_frame.pack(side="left", padx=20, pady=10)
    read_frame.pack(side="left", padx=20, pady=10)

    comp_label.pack(side="left", padx=20, pady=10)
    compression.pack(side="right", padx=20, pady=10)
    oct_label.pack(side="left", padx=20, pady=10)
    oct_button.pack(side="right", padx=20, pady=10)
    del_label.pack(side="left", padx=20, pady=10)
    del_button.pack(side="right", padx=20, pady=10)
    comp_frame.pack(side="top", padx=20, pady=10)
    oct_frame.pack(side="top", padx=20, pady=10)
    del_frame.pack(side="top", padx=20, pady=10)

    amp_switch.place(relx=0.2, rely=0.05, relwidth=0.6)
    min_label.pack(side="top", padx=20, pady=10)
    max_label.pack(side="top", padx=20, pady=10)
    range_min.pack(side="top", padx=20, pady=20)
    range_max.pack(side="top", padx=20, pady=20)
    min_val.pack(side="top", padx=20, pady=10)
    max_val.pack(side="top", padx=20, pady=10)

    root.mainloop()
