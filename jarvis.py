import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary 
import pygame
import os
import subprocess
from tkinter import Tk,Label,Button
import threading
import pystray
from pystray import MenuItem as Item
from PIL import Image,ImageDraw

recognizer = sr.Recognizer
engine = pyttsx3.init()

# initialize pygame mixer for playing music
pygame.mixer.init()

#globals for music control
music_folder=r"D:\Music"
playlist=[song for song in os.listdir(music_folder) if song.endswith('.mp3')]
current_song_index=0
is_paused=False

def speak(text):
    engine.say(text)
    engine.setProperty("rate",150)
    engine.runAndWait()

def play_music():
    """play the current song in the playlist"""
    global is_paused, current_song_index
    
    if not playlist:
        speak("No songs found in your music folder.")
        return
    song_path=os.path.join(music_folder,playlist[current_song_index])
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()
    speak(f"playing {playlist[current_song_index]}")

def pause_or_resume_music():
    global is_paused
    if pygame.mixer.music.get_busy():
        if is_paused:
            pygame.mixer.music.unpause()
            is_paused = False
            speak("Resuming music.")
        else:
            pygame.mixer.music.pause()
            is_paused = True
            speak("Music paused.")
    else:
        speak("No music is playing.")

def next_song():
    """play the next song in the playlist"""
    global current_song_index
    if playlist:
        current_song_index=(current_song_index+1)%len(playlist)
        play_music()
    else:
        speak("no more songs")

def previous_song():
    """play the previous song in the playlist"""
    global current_song_index
    if playlist:
        current_song_index=(current_song_index-1)%len(playlist)
        play_music()
    else:
        speak("no previous songs")

    # path to your music folder
    musicapp=r"C:\Users\shbzs\AppData\Roaming\Spotify\Spotify.exe"
    music_folder = r"D:\Music"
    # Get a list of all songs in the folder
    songs=[song for song in os.listdir(music_folder) if song.endswith('.mp3')]
    
    if songs:
        #play the first song in the list 
        songs_to_play=os.path.join(music_folder,songs[0]) 
        pygame.mixer.music.load(songs_to_play)
        pygame.mixer.music.play()
        engine.say("playing your songs now...")
    else:
        engine.say("No songs found in your music folder.")
def open_app(app_name):
    app_paths={
        "chrome":r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "epic games":r"D:\epic games\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe",
    }
    
    app_path=app_paths.get(app_name.lower())
    if app_path:
        try:
            subprocess.Popen(app_path)
            speak(f"opening{app_name}")
        except Exception as e:
            speak(f"error opening{app_name}")
            print(f"Error opening {app_name}: {e}")
    else:
        speak(f"Appilication {app_name}is not configured,")
        print(f"Appilication {app_name} is not configured.")

def  process_command(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com/")
    elif "open spotify" in c.lower():
        webbrowser.open("https://open.spotify.com/")
    elif "open jiosaavn" in c.lower():
        webbrowser.open("https://www.jiosaavn.com/")
    elif "play music"in c.lower():
        play_music()
    elif "pause music" in c or "resume music" in c:
        pause_or_resume_music()
    elif "next song" in c.lower():
        next_song()
    elif "previous song" in c.lower():
        previous_song()
    elif "play music" in c.lower():
        play_music()
    elif c.lower().startswith("open"):
        app_name = c.lower().replace("open", "").strip()
        open_app(app_name)
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music.get(song,"")
        if link:
            webbrowser.open(link)
            speak("playing {}...".format(song))
        else:
            speak("Song not found in the library.")
       

def run_assistant():
    recognizer =sr.Recognizer()
    speak("Hello, Iam your assistance. say 'jarvis' to start")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for 'Jarvis'...")
                recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            trigger_word = recognizer.recognize_google(audio)
            if trigger_word.lower() == "jarvis":
                speak("At your service. What can I do for you?")
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    print("Listening for command...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    process_command(command)
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"Error: {e}")

#Tkinter GUI
def start_gui():
    app=Tk()
    app.title("Personal Assitance")
    Label(app, text="Welcome to Jarvis!", font=("Arial", 20)).pack(pady=20)
    Button(app,text="Start Assitant",command=run_assistant,font=("Arial",14)).pack(pady=10)
    app.mainloop()

def start_assistant_thread():
    """Start the Assistant  in a seprate thread"""
    threading.Thread(target=run_assistant,daemon=True).start()

#system tray
def create_icon():
    """create a system tray icon for the app"""
    def on_exit(icon,Item):
        icon.stop()
    image = Image.new('RGB', (64, 64), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 64, 64), fill=(0, 100, 200))

    menu = (Item('Exit', on_exit),)
    icon = pystray.Icon("assistant", image, "Personal Assistant", menu)
    icon.run()

if __name__ == "__main__":
    threading.Thread(target=start_gui, daemon=True).start()
    create_icon()  # System Tray icon

