from PIL import Image, ImageTk
from pythonosc.udp_client import SimpleUDPClient
import tkinter
import customtkinter
import sys
import math
import random
import time

root = customtkinter.CTk()
root.title('RGBeats')
root.geometry('1200x1000')


def is_grey_scale(img):
    w, h = img.size
    for j in range(w):
        for i in range(h):
            r, g, b, a = img.getpixel((j,i))
            if r != g or g != b or r !=b: 
                return False
    return True

def is_rgba(img):
    if img.info.get("transparency", None) is not None:
        return True
    extrema = img.getextrema()
    if extrema[3][0] < 255:
        return True
    return False

def distance(pixel, color):
    x = pixel[0]-color[0]
    y = pixel[1]-color[1]
    z = pixel[2]-color[2]
    if (x + y + z >= 0): return math.sqrt(math.sqrt(x*x+y*y+z*z))
    else: return -math.sqrt(math.sqrt(x*x+y*y+z*z))

def find_closest(pixel, colors):
    maxi = 999999
    mini = -999999
    for idx, rgb in colors:
        d = distance(pixel, rgb)
        if d < maxi and d > mini:
            if (d > 0):
                maxi = d
                mini = -d
            else:
                maxi = -d
                mini = d
            color = idx
    return color

def find_color(pixel, img, blackwhite, colors): 
    if not is_grey_scale(img):
        if abs(pixel[0] - pixel[1]) < 10 and abs(pixel[0] - pixel[2]) < 10 and abs(pixel[2] - pixel[1]) < 10 :
            bw = (pixel[0] + pixel[1] + pixel[2])/(3*255)
            if bw >= 0.5:
                return 1
            else:
                return 0
        return find_closest(pixel, colors)
        
    else:
        for i in range(len(blackwhite)):
            if pixel[0] < blackwhite[i][1]:
                return i


radio_var = tkinter.IntVar(0)
radio_var.set(2)

order_var = tkinter.IntVar(0)
comp_var = tkinter.IntVar(0)
comp_var.set(value=1)
def comp_event(variable):
    img = Image.open('og.png')
    w, h = img.size
    new_size = math.ceil(w/comp_var.get()), math.ceil(h/comp_var.get())
    resized_image = img.resize(new_size)
    resized_image.save('compressed_image.png', optimize=True, quality=50)
    pic = customtkinter.CTkImage(resized_image, size=(w, h))
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
        img = Image.open(path)
        img = img.convert("RGBA")
        img.save('og.png', optimize=True, quality=50)
        w, h = img.size
        new_size = math.ceil(w/comp_var.get()), math.ceil(h/comp_var.get())
        resized_image = img.resize(new_size)
        resized_image.save('compressed_image.png', optimize=True, quality=50)
        pic = customtkinter.CTkImage(resized_image, size=(w, h))
        imag.configure(image=pic)

ip= sys.argv[1]
sending_to_port= int(sys.argv[2])
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
    colors_bw[0] = (0,0,0)
    for i in range(int(radio_var.get())):
        temp = int(255*(float(i)/int(radio_var.get())))
        if (i +1 < len(colors_bw)): colors_bw[i+1] = (temp, temp, temp)
    colors_bw[int(radio_var.get())-1] = (255, 255, 255)

    img = Image.open('compressed_image.png')
    w, h = img.size
    print(f"Sending OSC | /on/1")
    py_to_pd_OscSender.send_message("/on", 1)
    print(f"Sending OSC | /delay/{del_button_var.get()} | /octave/{oct_button_var.get()}")
    notes = [1, 16.35, 18.35, 20.6, 21.83, 24.5, 27.5, 30.87, 32.7]
    note_str= "1 "
    for i in range(1, len(notes)):
        notes[i] = int(notes[i]*2**(oct_button_var.get()))
    py_to_pd_OscSender.send_message("/delay", del_button_var.get())
    py_to_pd_OscSender.send_message("/octave", notes)
    i = 0
    while(i < h):
        j = 0
        while(j < w):
            root.update()
            if (order_var.get() !=0):
                print("Pixel with RGBA values {} at coordinate {}".format(img.getpixel((j,i)), (j,i)))
                pan = 2*(float(j)/w)-1
                amp = int(img.getpixel((j,i))[3]*157/float(255))
                color = find_color(img.getpixel((j,i)), img, colors_bw, colors)
                if (not is_grey_scale(img)):  offset = distance(img.getpixel((j,i)), colors[color][1])
                else: 
                    
                    offset = distance(img.getpixel((j,i)), colors_bw[color])
            else:
                k = random.randrange(0, h)
                l = random.randrange(0, w)
                print("Pixel with RGBA values {} at coordinate {}".format(img.getpixel((l,k)), (l,k)))
                pan = 2*(float(l)/w)-1
                amp = int(img.getpixel((l,k))[3]*157/float(255))
                color = find_color(img.getpixel((l,k)), img, colors_bw, colors)
                if (not is_grey_scale(img)):  offset = distance(img.getpixel((l,k)), colors[color][1])
                else: offset = distance(img.getpixel((l,k)), colors_bw[color])
            if (range_slider_max_var.get() != -1): amp = int(random.randrange(range_slider_min_var.get(), range_slider_max_var.get()))
            print(f"Sending OSC | /note/amp/{amp} | /note/pan/{pan} | /note/color/{color} | /note/offset/{offset}")
            py_to_pd_OscSender.send_message("/note/pan", pan)
            py_to_pd_OscSender.send_message("/note/amp", amp)
            py_to_pd_OscSender.send_message("/note/color", color)
            py_to_pd_OscSender.send_message("/note/offset", offset)
            j+=1
            time.sleep(del_button_var.get())
        i+=1
        if (order_var.get() == -1):
            j = w-1
            while(j>=0):
                root.update()
                print("Pixel with RGBA values {} at coordinate {}".format(img.getpixel((j,i)), (j,i)))
                pan = 2*(float(j)/w)-1
                amp = int(img.getpixel((j,i))[3]*157/float(255))
                if (range_slider_max_var.get() != -1): amp = int(random.randrange(range_slider_min_var.get(), range_slider_max_var.get()))
                color = find_color(img.getpixel((j,i)), img, colors_bw, colors)
                if (not is_grey_scale(img)):  offset = distance(img.getpixel((j,i)), colors[color][1])
                else: offset = distance(img.getpixel((j,i)), colors_bw[color])
                py_to_pd_OscSender.send_message("/note/pan", pan)
                py_to_pd_OscSender.send_message("/note/amp", amp)
                py_to_pd_OscSender.send_message("/note/color", color)
                py_to_pd_OscSender.send_message("/note/offset", offset)
                j-=1
                time.sleep(del_button_var.get())
            i+=1
    print(f"Sending OSC | /on/0")
    py_to_pd_OscSender.send_message("/on", 0)

def stop():
    print(f"Sending OSC | /on/0")
    py_to_pd_OscSender.send_message("/on", 0)

if __name__ == "__main__":

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("green")
    button_frame = customtkinter.CTkFrame(master=root, width=400, height=200)
    button_frame.place(relx = 0.55, rely = 0.66, relheight=0.3)
    button_frame.pack_propagate(0)
    col_frame = customtkinter.CTkFrame(master=button_frame, width=300, height=300)
    col_frame.pack(fill= "both", padx=20, pady=20)
    read_frame = customtkinter.CTkFrame(master=button_frame, width=300, height=300)
    read_frame.pack(fill= "both", padx=20, pady=20)
    amp_frame = customtkinter.CTkFrame(master=root, width=400, height=420)
    amp_frame.place(relx = 0.55, rely = 0.05)
    amp_frame.pack_propagate(0)
    min_frame = customtkinter.CTkFrame(master=amp_frame, width=300, height=300)
    min_frame.place(relx=0.05, rely = 0.15, relwidth=0.4)
    max_frame = customtkinter.CTkFrame(master=amp_frame, width=300, height=300)
    max_frame.place(relx=0.55, rely = 0.15, relwidth=0.4)
    seg_frame = customtkinter.CTkFrame(master=root, width=515, height=300)
    seg_frame.place(relx = 0.113, rely = 0.66, relheight=0.3)
    seg_frame.pack_propagate(0)
    comp_frame = customtkinter.CTkFrame(master=seg_frame, width=300, height=300)
    col_frame.pack(fill= "both", padx=20, pady=20)
    oct_frame = customtkinter.CTkFrame(master=seg_frame, width=300, height=300)
    oct_frame.pack(fill= "both", padx=20, pady=20)
    del_frame = customtkinter.CTkFrame(master=seg_frame, width=300, height=300)
    del_frame.pack(fill= "both", padx=20, pady=20)
    play_pause_frame = customtkinter.CTkFrame(master=root, width=515, height=45)
    play_pause_frame.place(relx = 0.113, rely = 0.05)
    play_pause_frame.pack_propagate(0)
    img_frame = customtkinter.CTkFrame(master=root, width=515, height=367)
    img_frame.place(relx = 0.113, rely = 0.125)
    img_frame.pack_propagate(0)




    color_label = customtkinter.CTkLabel(col_frame, text="CTkLabel", fg_color="transparent")
    color_label.configure(text=" Select a color count: ")

    color_1 = customtkinter.CTkRadioButton(master=col_frame, text="2", variable= radio_var, value=2)
    color_2 = customtkinter.CTkRadioButton(master=col_frame, text="5", variable= radio_var, value=5)
    color_3 = customtkinter.CTkRadioButton(master=col_frame, text="8", variable= radio_var, value=8)

    order_label = customtkinter.CTkLabel(read_frame, text="CTkLabel", fg_color="transparent")
    order_label.configure(text=" Select a read order: ")

    order_1 = customtkinter.CTkRadioButton(master=read_frame, text="Random", variable= order_var, value=0)
    order_2 = customtkinter.CTkRadioButton(master=read_frame, text="Left to Right", variable= order_var, value=1)
    order_3 = customtkinter.CTkRadioButton(master=read_frame, text="Smooth", variable= order_var, value=-1)



    amp_switch_var = customtkinter.IntVar(value=1)
    amp_switch = customtkinter.CTkSwitch(amp_frame, text="Randomized Amplitudes Enabled", command=amp_switch_event,
                                 variable=amp_switch_var, onvalue=1, offvalue=0)
    
    min_label = customtkinter.CTkLabel(min_frame, text="CTkLabel", fg_color="transparent")
    min_label.configure(text="Minimum Amplitude")
    max_label = customtkinter.CTkLabel(max_frame, text="CTkLabel", fg_color="transparent")
    max_label.configure(text="Maximum Amplitude")
    min_val = customtkinter.CTkLabel(min_frame, text="CTkLabel", fg_color="transparent")
    min_val.configure(text="0")
    max_val = customtkinter.CTkLabel(max_frame, text="CTkLabel", fg_color="transparent")
    max_val.configure(text="155")
    range_min = customtkinter.CTkSlider(min_frame, from_=0, to=154, command=range_event, variable = range_slider_min_var, orientation="vertical")
    range_max = customtkinter.CTkSlider(max_frame, from_=range_slider_min_var.get(), to=155, command=range_event, variable = range_slider_max_var, orientation="vertical")
    
    comp_label = customtkinter.CTkLabel(comp_frame, text="CTkLabel", fg_color="transparent")
    comp_label.configure(text="Select a compression factor:")
    compression = customtkinter.CTkSegmentedButton(comp_frame, values=[1,2,4,8,16,32,64,128], command=comp_event, variable = comp_var)
    
    oct_label = customtkinter.CTkLabel(oct_frame, text="CTkLabel", fg_color="transparent")
    oct_label.configure(text="Select an octave:")
    oct_button = customtkinter.CTkSegmentedButton(oct_frame, values=[1,2,3,4,5,6,7,8], variable=oct_button_var)

    del_label = customtkinter.CTkLabel(del_frame, text="CTkLabel", fg_color="transparent")
    del_label.configure(text="Select a note delay:")
    del_button = customtkinter.CTkSegmentedButton(del_frame, values=[0.1, 0.25, 0.5, 0.75, 1, 1.5, 2, 4], variable=del_button_var)
    imag = customtkinter.CTkLabel(img_frame, text = " ", fg_color="transparent")

    uploadButton = customtkinter.CTkButton(play_pause_frame, text="Upload Image", command=imageUploader)
    uploadButton.place(relx = 0.025, rely = 0.15, relwidth = 0.3)
    playButton = customtkinter.CTkButton(play_pause_frame, text="Play", command=play)
    playButton.place(relx = 0.35, rely = 0.15, relwidth = 0.3)
    stopButton = customtkinter.CTkButton(play_pause_frame, text="Stop", command=stop)
    stopButton.place(relx = 0.675, rely = 0.15, relwidth=0.3)
    img = Image.open('compressed_image.png')
    w, h = img.size
    imag.place(relx=0.2, rely = 0.2, relwidth =0.6, relheight = 0.6*(h/w))

    
    color_label.pack(side= "top", padx=20, pady=10)
    order_label.pack(side= "top", padx=20, pady=10)
    color_1.pack(side= "top", padx=20, pady=10)
    order_1.pack(side= "top",padx=20, pady=10)
    color_2.pack(side= "top", padx=20, pady=10)
    order_2.pack(side= "top", padx=20, pady=10)
    color_3.pack(side= "top", padx=20, pady=10)
    order_3.pack(side= "top", padx=20, pady=10)
    col_frame.pack(side= "left", padx=20, pady=10)
    read_frame.pack(side= "left", padx=20, pady=10)


    comp_label.pack(side= "left", padx=20, pady=10)
    compression.pack(side= "right", padx=20, pady=10)
    oct_label.pack(side= "left", padx=20, pady=10)
    oct_button.pack(side= "right", padx=20, pady=10)
    del_label.pack(side= "left", padx=20, pady=10)
    del_button.pack(side= "right", padx=20, pady=10)
    comp_frame.pack(side= "top", padx=20, pady=10)
    oct_frame.pack(side= "top", padx=20, pady=10)
    del_frame.pack(side= "top", padx=20, pady=10)


    amp_switch.place(relx = 0.2, rely = 0.05, relwidth = 0.6)
    min_label.pack(side= "top", padx=20, pady=10)
    max_label.pack(side= "top", padx=20, pady=10)
    range_min.pack(side= "top", padx= 20, pady=20)
    range_max.pack(side= "top", padx= 20, pady=20)
    min_val.pack(side= "top", padx=20, pady=10)
    max_val.pack(side= "top", padx=20, pady=10)

    root.mainloop()
