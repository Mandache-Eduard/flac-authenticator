import shutil
import subprocess

def call_spek(file_path):
    if not shutil.which("spek"):
        print("Spek not detected. Please install it from https://spek.cc and ensure it's in your PATH.")
        return
    # Run Spek via command line
    try:
        subprocess.run(["spek", file_path], check=True)
    except FileNotFoundError:
        print("Spek is not installed or not in your PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Spek exited with an error: {e}")

def spek_manual():
    print("""
        Menu
    
    Ctrl-O : Open a new file.
    
    Ctrl-S : Save the spectrogram as an image file.
    
    Ctrl-E : Show the preferences dialog.
    
    F1 : Open online manual in the browser.
    
    Shift-F1 : Show the about dialog.
    
    Spectrogram
    
    c, C : Change the audio channel.
    
    f, F : Change the DFT window function.
    
    l, L : Change the lower limit of the dynamic range in dBFS.
    
    p, P : Change the palette.
    
    s, S : Change the audio stream.
    
    u, U : Change the upper limit of the dynamic range in dBFS.
    
    w, W : Change the DFT window size.""")