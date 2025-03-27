from PIL import Image, ImageTk
from pythonosc.udp_client import SimpleUDPClient
import tkinter
import customtkinter
import sys
import random
import time
from imageProcessor import *

class RGBeatsAPP:
    def __init__(self, root):
        self.root = root
        self.root.title('RGBeats')
        self.root.geometry('1200x1000')

        # Initial Variables
        self.radio_var = tkinter.IntVar(0)
        self.radio_var.set(2)
        self.order_var = tkinter.IntVar(0)
        self.comp_var = tkinter.IntVar(0)
        self.comp_var.set(value=1)
        self.amp_switch_var = tkinter.IntVar(0)
        self.range_slider_min_var = tkinter.IntVar(0)
        self.range_slider_max_var = tkinter.IntVar(0)
        self.range_slider_max_var.set(155)
        self.oct_button_var = tkinter.IntVar(0)
        self.oct_button_var.set(value=1)
        self.del_button_var = tkinter.DoubleVar(0)
        self.del_button_var.set(value=0.1)

        self.py_to_pd_OscSender = SimpleUDPClient('127.0.0.1', int(sys.argv[1]))

        self._setup_gui()

    def _setup_gui(self):
        # Setup all frames and components here
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")

        self.button_frame = customtkinter.CTkFrame(master=self.root, width=400, height=200)
        self.button_frame.place(relx=0.55, rely=0.66, relheight=0.3)
        self.button_frame.pack_propagate(0)

        self.col_frame = customtkinter.CTkFrame(master=self.button_frame, width=300, height=300)
        self.col_frame.pack(fill="both", padx=20, pady=20)

        self.read_frame = customtkinter.CTkFrame(master=self.button_frame, width=300, height=300)
        self.read_frame.pack(fill="both", padx=20, pady=20)

        self.amp_frame = customtkinter.CTkFrame(master=self.root, width=400, height=420)
        self.amp_frame.place(relx=0.55, rely=0.05)
        self.amp_frame.pack_propagate(0)

        self.min_frame = customtkinter.CTkFrame(master=self.amp_frame, width=300, height=300)
        self.min_frame.place(relx=0.05, rely=0.15, relwidth=0.4)

        self.max_frame = customtkinter.CTkFrame(master=self.amp_frame, width=300, height=300)
        self.max_frame.place(relx=0.55, rely=0.15, relwidth=0.4)

        self.seg_frame = customtkinter.CTkFrame(master=self.root, width=515, height=300)
        self.seg_frame.place(relx=0.113, rely=0.66, relheight=0.3)
        self.seg_frame.pack_propagate(0)

        self.comp_frame = customtkinter.CTkFrame(master=self.seg_frame, width=300, height=300)
        self.comp_frame.pack(fill="both", padx=20, pady=20)

        self.oct_frame = customtkinter.CTkFrame(master=self.seg_frame, width=300, height=300)
        self.oct_frame.pack(fill="both", padx=20, pady=20)

        self.del_frame = customtkinter.CTkFrame(master=self.seg_frame, width=300, height=300)
        self.del_frame.pack(fill="both", padx=20, pady=20)

        self.play_pause_frame = customtkinter.CTkFrame(master=self.root, width=515, height=45)
        self.play_pause_frame.place(relx=0.113, rely=0.05)
        self.play_pause_frame.pack_propagate(0)

        self.img_frame = customtkinter.CTkFrame(master=self.root, width=515, height=367)
        self.img_frame.place(relx=0.113, rely=0.125)
        self.img_frame.pack_propagate(0)

        self.color_label = customtkinter.CTkLabel(self.col_frame, text="Select a color count: ")
        self.color_label.configure(fg_color="transparent")

        # Components and Buttons Initialization
        self.color_1 = customtkinter.CTkRadioButton(master=self.col_frame, text="2", variable=self.radio_var, value=2)
        self.color_2 = customtkinter.CTkRadioButton(master=self.col_frame, text="5", variable=self.radio_var, value=5)
        self.color_3 = customtkinter.CTkRadioButton(master=self.col_frame, text="8", variable=self.radio_var, value=8)

        self.order_label = customtkinter.CTkLabel(self.read_frame, text="Select a read order: ")
        self.order_label.configure(fg_color="transparent")

        self.order_1 = customtkinter.CTkRadioButton(master=self.read_frame, text="Random", variable=self.order_var, value=0)
        self.order_2 = customtkinter.CTkRadioButton(master=self.read_frame, text="Left to Right", variable=self.order_var, value=1)
        self.order_3 = customtkinter.CTkRadioButton(master=self.read_frame, text="Smooth", variable=self.order_var, value=-1)

        self.amp_switch = customtkinter.CTkSwitch(self.amp_frame, text="Randomized Amplitudes Enabled", command=self.amp_switch_event, variable=self.amp_switch_var, onvalue=1, offvalue=0)

        self.min_label = customtkinter.CTkLabel(self.min_frame, text="Minimum Amplitude", fg_color="transparent")
        self.max_label = customtkinter.CTkLabel(self.max_frame, text="Maximum Amplitude", fg_color="transparent")
        self.min_val = customtkinter.CTkLabel(self.min_frame, text="0", fg_color="transparent")
        self.max_val = customtkinter.CTkLabel(self.max_frame, text="155", fg_color="transparent")
        self.range_min = customtkinter.CTkSlider(self.min_frame, from_=0, to=154, command=self.range_event, variable=self.range_slider_min_var, orientation="vertical")
        self.range_max = customtkinter.CTkSlider(self.max_frame, from_=self.range_slider_min_var.get(), to=155, command=self.range_event, variable=self.range_slider_max_var, orientation="vertical")

        self.comp_label = customtkinter.CTkLabel(self.comp_frame, text="Select a compression factor:", fg_color="transparent")
        self.compression = customtkinter.CTkSegmentedButton(self.comp_frame, values=[1, 2, 4, 8, 16, 32, 64, 128], command=self.comp_event, variable=self.comp_var)

        self.oct_label = customtkinter.CTkLabel(self.oct_frame, text="Select an octave:", fg_color="transparent")
        self.oct_button = customtkinter.CTkSegmentedButton(self.oct_frame, values=[1, 2, 3, 4, 5, 6, 7, 8], variable=self.oct_button_var)

        self.del_label = customtkinter.CTkLabel(self.del_frame, text="Select a note delay:", fg_color="transparent")
        self.del_button = customtkinter.CTkSegmentedButton(self.del_frame, values=[0.1, 0.25, 0.5, 0.75, 1, 1.5, 2, 4], variable=self.del_button_var)
        self.imag = customtkinter.CTkLabel(self.img_frame, text=" ", fg_color="transparent")

        self.uploadButton = customtkinter.CTkButton(self.play_pause_frame, text="Upload Image", command=self.imageUploader)
        self.uploadButton.place(relx=0.025, rely=0.15, relwidth=0.3)
        self.playButton = customtkinter.CTkButton(self.play_pause_frame, text="Play", command=self.play)
        self.playButton.place(relx=0.35, rely=0.15, relwidth=0.3)
        self.stopButton = customtkinter.CTkButton(self.play_pause_frame, text="Stop", command=self.stop)
        self.stopButton.place(relx=0.675, rely=0.15, relwidth=0.3)

        self.img = Image.open('compressed_image.png')
        w, h = self.img.size
        self.imag.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.6 * (h / w))

        # Layout packing
        self.color_label.pack(side="top", padx=20, pady=10)
        self.order_label.pack(side="top", padx=20, pady=10)
        self.color_1.pack(side="top", padx=20, pady=10)
        self.order_1.pack(side="top", padx=20, pady=10)
        self.color_2.pack(side="top", padx=20, pady=10)
        self.order_2.pack(side="top", padx=20, pady=10)
        self.color_3.pack(side="top", padx=20, pady=10)
        self.order_3.pack(side="top", padx=20, pady=10)
        self.col_frame.pack(side="left", padx=20, pady=10)
        self.read_frame.pack(side="left", padx=20, pady=10)

        self.comp_label.pack(side="left", padx=20, pady=10)
        self.compression.pack(side="right", padx=20, pady=10)
        self.oct_label.pack(side="left", padx=20, pady=10)
        self.oct_button.pack(side="right", padx=20, pady=10)
        self.del_label.pack(side="left", padx=20, pady=10)
        self.del_button.pack(side="right", padx=20, pady=10)
        self.comp_frame.pack(side="top", padx=20, pady=10)
        self.oct_frame.pack(side="top", padx=20, pady=10)
        self.del_frame.pack(side="top", padx=20, pady=10)

        self.amp_switch.place(relx=0.2, rely=0.05, relwidth=0.6)
        self.min_label.pack(side="top", padx=20, pady=10)
        self.max_label.pack(side="top", padx=20, pady=10)
        self.range_min.pack(side="top", padx=20, pady=20)
        self.range_max.pack(side="top", padx=20, pady=20)
        self.min_val.pack(side="top", padx=20, pady=10)
        self.max_val.pack(side="top", padx=20, pady=10)

    def comp_event(self, variable):
        image_processor = ImageProcessor('og.png')
        resized_image = image_processor.resize(self.comp_var.get())
        resized_image.save('compressed_image.png', optimize=True, quality=50)
        pic = customtkinter.CTkImage(resized_image, size=image_processor.get_size())
        self.imag.configure(image=pic)

    def amp_switch_event(self):
        if self.amp_switch_var.get() == 1:
            self.amp_switch.configure(text=" Randomized Amplitudes Enabled")
            self.range_max.configure(state="normal", button_color="#2FA572", progress_color="#AAB0B5")
            self.range_min.configure(state="normal", button_color="#2FA572", progress_color="#AAB0B5")
            self.min_label.configure(text_color="#C0C7D0")
            self.max_label.configure(text_color="#C0C7D0")
        else:
            self.amp_switch.configure(text=" Randomized Amplitudes Disabled")
            self.range_max.configure(state="disabled", button_color="#164f36", progress_color="#333d39")
            self.range_min.configure(state="disabled", button_color="#164f36", progress_color="#333d39")
            self.min_label.configure(text_color="#4A4D50")
            self.max_label.configure(text_color="#4A4D50")

    def range_event(self, value):
        if self.range_slider_max_var.get() <= self.range_slider_min_var.get():
            self.range_slider_max_var.set(self.range_slider_min_var.get() + 1)
        self.range_max.configure(from_=self.range_slider_min_var.get())
        self.min_val.configure(text=str(self.range_slider_min_var.get()))
        self.max_val.configure(text=str(self.range_slider_max_var.get()))

    def imageUploader(self):
        fileTypes = [("Image files", "*.png;*.jpg;*.jpeg")]
        path = tkinter.filedialog.askopenfilename(filetypes=fileTypes)

        if len(path):
            image_processor = ImageProcessor(path)
            image_processor.save_image('og.png')
            resized_image = image_processor.resize(self.comp_var.get())
            resized_image.save('compressed_image.png', optimize=True, quality=50)
            pic = customtkinter.CTkImage(resized_image, size=image_processor.get_size())
            self.imag.configure(image=pic)

    def play(self):
        colors = colorSet(int(self.radio_var.get()))
        colors_bw = bwSet(int(self.radio_var.get()))

        image_processor = ImageProcessor('compressed_image.png')
        w, h = image_processor.get_size()
        print(f"Sending OSC | /on/1")
        self.py_to_pd_OscSender.send_message("/on", 1)
        print(f"Sending OSC | /delay/{self.del_button_var.get()} | /octave/{self.oct_button_var.get()}")
        notes = [1, 16.35, 18.35, 20.6, 21.83, 24.5, 27.5, 30.87, 32.7]
        note_str = "1 "
        for i in range(1, len(notes)):
            notes[i] = int(notes[i] * 2 ** (self.oct_button_var.get()))
        self.py_to_pd_OscSender.send_message("/delay", self.del_button_var.get())
        self.py_to_pd_OscSender.send_message("/octave", notes)

        i = 0
        while (i < h):
            j = 0
            while (j < w):
                self.root.update()
                if (self.order_var.get() != 0):
                    print("Pixel with RGBA values {} at coordinate {}".format(image_processor.get_pixel(j, i), (j, i)))
                    pan = 2 * (float(j) / w) - 1
                    amp = int(image_processor.get_pixel(j, i)[3] * 157 / float(255))
                    color = find_color(image_processor.get_pixel(j, i), image_processor, colors_bw, colors)
                    if (not image_processor.is_grey_scale()): offset = distance(image_processor.get_pixel(j, i), colors[color][1])
                    else:
                        offset = distance(image_processor.get_pixel(j, i), colors_bw[color])
                else:
                    k = random.randrange(0, h)
                    l = random.randrange(0, w)
                    print("Pixel with RGBA values {} at coordinate {}".format(image_processor.get_pixel(l, k), (l, k)))
                    pan = 2 * (float(l) / w) - 1
                    amp = int(image_processor.get_pixel(l, k)[3] * 157 / float(255))
                    color = find_color(image_processor.get_pixel(l, k), image_processor, colors_bw, colors)
                    if (not image_processor.is_grey_scale()): offset = distance(image_processor.get_pixel(l, k), colors[color][1])
                    else: offset = distance(image_processor.get_pixel(l, k), colors_bw[color])
                if (self.range_slider_max_var.get() != -1): amp = int(random.randrange(self.range_slider_min_var.get(), self.range_slider_max_var.get()))
                print(f"Sending OSC | /note/amp/{amp} | /note/pan/{pan} | /note/color/{color} | /note/offset/{offset}")
                self.py_to_pd_OscSender.send_message("/note/pan", pan)
                self.py_to_pd_OscSender.send_message("/note/amp", amp)
                self.py_to_pd_OscSender.send_message("/note/color", color)
                self.py_to_pd_OscSender.send_message("/note/offset", offset)
                j += 1
                time.sleep(self.del_button_var.get())
            i += 1
        self.stop()

    def stop(self):
        print(f"Sending OSC | /on/0")
        self.py_to_pd_OscSender.send_message("/on", 0)