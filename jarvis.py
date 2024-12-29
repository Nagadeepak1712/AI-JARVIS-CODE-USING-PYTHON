import os
import shutil
import subprocess
import webbrowser
from plyer import notification
import pyttsx3
import speech_recognition as sr
import datetime


# Initialize Text-to-Speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to the microphone and return the recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
        except sr.RequestError:
            speak("Sorry, the service is down.")
    return ""

# System Commands
def shutdown():
    """Shutdown the computer."""
    speak("Shutting down your computer.")
    os.system("shutdown /s /t 1")  # Windows
    # os.system("shutdown -h now")  # Linux/Mac

def restart():
    """Restart the computer."""
    speak("Restarting your computer.")
    os.system("shutdown /r /t 1")  # Windows
    # os.system("reboot")  # Linux/Mac

def lock_screen():
    """Lock the computer screen."""
    speak("Locking the screen.")
    os.system("rundll32.exe user32.dll,LockWorkStation")  # Windows
    # os.system("gnome-screensaver-command -l")  # Linux

# File Management
def create_file(filename, content):
    """Create a file with specified content."""
    with open(filename, 'w') as file:
        file.write(content)
    speak(f"File {filename} created with content.")

def delete_file(filename):
    """Delete a file."""
    try:
        os.remove(filename)
        speak(f"File {filename} deleted.")
    except FileNotFoundError:
        speak(f"File {filename} not found.")

def move_file(src, dst):
    """Move a file from source to destination."""
    try:
        shutil.move(src, dst)
        speak(f"File {src} moved to {dst}.")
    except FileNotFoundError:
        speak(f"File {src} not found.")

# Media Control
def play_music():
    """Play a music file."""
    music_file = "path_to_music_file.mp3"
    if os.path.exists(music_file):
        speak("Playing music.")
        os.startfile(music_file)  # Windows
        # subprocess.Popen(['xdg-open', music_file])  # Linux
    else:
        speak("Music file not found.")

def pause_music():
    """Pause the music (Placeholder)."""
    speak("Pausing music is not implemented in this example.")

def stop_music():
    """Stop the music (Placeholder)."""
    speak("Stopping music is not implemented in this example.")

# Notifications
def notify(title, message):
    """Send a desktop notification."""
    notification.notify(
        title=title,
        message=message,
        timeout=10  # seconds
    )

# Web Browsing
def open_website(url):
    """Open a website in the default browser."""
    webbrowser.open(url)
    speak(f"Opening {url}")

def search_web(query):
    """Search the web using the default browser."""
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"Searching the web for {query}")

# Command Execution
def execute_command(command):
    """Execute a command based on the user input."""
    if 'shutdown' in command:
        shutdown()
    elif 'restart' in command:
        restart()
    elif 'lock screen' in command:
        lock_screen()
    elif 'create file' in command:
        create_file('test.txt', 'Hello World!')
    elif 'delete file' in command:
        delete_file('test.txt')
    elif 'move file' in command:
        move_file('test.txt', 'new_folder/test.txt')
    elif 'play music' in command:
        play_music()
    elif 'pause music' in command:
        pause_music()
    elif 'stop music' in command:
        stop_music()
    elif 'notify' in command:
        notify('Test Title', 'This is a test notification.')
    elif 'open website' in command:
        url = command.split('open website ')[-1]
        open_website(url)
    elif 'search web' in command:
        query = command.split('search web ')[-1]
        search_web(query)
    else:
        speak("Command not recognized.")

# Main Loop
def main():
    """Main loop for listening to commands and executing them."""
    speak("Hello! How can I assist you today?")
    while True:
        command = listen()
        if command:
            execute_command(command)
        if 'exit' in command or 'quit' in command:
            speak("Goodbye!")
            break

if __name__ == "__main__":
    main()
