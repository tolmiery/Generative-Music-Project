import os
import subprocess
import platform
import customtkinter
from beatsApp import *


#Open the main.maxpat file using the default application.
#Necessary to actually produce any audio from the Max patch.
#Also sets the DISPLAY environment variable for GUI applications if not already set.
def setup():
    if os.environ.get('DISPLAY', '') == '':
        print('No display found. Using :0.0')
        os.environ['DISPLAY'] = ':0.0'
    script_dir = os.path.dirname(os.path.realpath(__file__))
    maxpat_file = os.path.join(script_dir, "main.maxpat")

    if os.path.exists(maxpat_file):
        print(f"Opening {maxpat_file}")
        try:
            current_os = platform.system()
            if current_os == "Darwin":  
                subprocess.Popen(["open", maxpat_file]) 
            elif current_os == "Windows":  
                subprocess.Popen(["start", maxpat_file], shell=True) 
            elif 'microsoft' in platform.release().lower():  # Need to do this if you're like me and run WSL
                # Convert WSL path (/mnt/c/...) to Windows path (C:\...)
                windows_path = maxpat_file.replace("/mnt/c/", "C:\\").replace("/", "\\")
                subprocess.Popen(["cmd.exe", "/C", "start", windows_path])  
            elif current_os == "Linux":  
                subprocess.Popen(["xdg-open", maxpat_file]) 
            else:
                print("Unsupported OS. Cannot open .maxpat file.")
        except Exception as e:
            print(f"Error opening file: {e}")
    else:
        print(f"Error: {maxpat_file} not found.")

if __name__ == "__main__":
    setup()
    root = customtkinter.CTk()
    gui = RGBeatsAPP(root)
    root.mainloop()
