import pyttsx3
import speech_recognition as sr
import pywhatkit
import wikipedia
import datetime
import os
import requests
from selenium import webdriver
from tkinter import *
from PIL import Image, ImageTk

# Initialize the speech engine
engine = pyttsx3.init()

USER = "YourName"
BOTNAME = "JARVIS"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio).lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            speak("Sorry, there was a problem with the speech recognition service.")
            return None

def greet_user():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak(f"Good morning, {USER}")
    elif 12 <= hour < 18:
        speak(f"Good afternoon, {USER}")
    else:
        speak(f"Good evening, {USER}")
    speak(f"I am {BOTNAME}. How can I assist you today?")

def tell_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    speak(f"The current time is {current_time}")

def open_chrome():
    os.system('start chrome')

def search_chrome(query):
    driver = webdriver.Chrome()
    driver.get(f"https://www.google.com/search?q={query}")

def open_website(url):
    driver = webdriver.Chrome()
    driver.get(url)

def download_image(query):
    url = f"https://www.google.com/search?tbm=isch&q={query}"
    driver = webdriver.Chrome()
    driver.get(url)
    images = driver.find_elements_by_tag_name('img')
    for i, image in enumerate(images[:5]):
        src = image.get_attribute('src')
        img_data = requests.get(src).content
        with open(f'image_{i}.jpg', 'wb') as handler:
            handler.write(img_data)
    driver.quit()

def get_meaning(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url).json()
    if response:
        meaning = response[0]['meanings'][0]['definitions'][0]['definition']
        speak(f"The meaning of {word} is {meaning}")
    else:
        speak(f"Sorry, I couldn't find the meaning of {word}")

def create_gui():
    root = Tk()
    root.title("Personal Assistant")
    root.configure(bg='yellow')

    label = Label(root, text="Welcome to Your Personal Assistant", bg='red', fg='white', font=("Helvetica", 16))
    label.pack(pady=20)

    button = Button(root, text="Start", command=greet_user, bg='red', fg='white', font=("Helvetica", 14))
    button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
    while True:
        command = listen()
        if command:
            if 'open notepad' in command:
                os.system('notepad.exe')
            elif 'play' in command:
                song = command.replace('play', '')
                speak(f"Playing {song}")
                pywhatkit.playonyt(song)
            elif 'search' in command:
                search_query = command.replace('search', '')
                speak(f"Searching for {search_query}")
                pywhatkit.search(search_query)
            elif 'wikipedia' in command:
                search_query = command.replace('wikipedia', '')
                results = wikipedia.summary(search_query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
            elif 'open youtube' in command:
                open_website('https://www.youtube.com')
            elif 'open chrome' in command:
                open_chrome()
            elif 'search on chrome' in command:
                search_query = command.replace('search on chrome', '')
                search_chrome(search_query)
            elif 'download image' in command:
                image_query = command.replace('download image', '')
                download_image(image_query)
            elif 'meaning of' in command:
                word = command.replace('meaning of', '').strip()
                get_meaning(word)
            elif 'time' in command:
                tell_time()
            elif 'exit' in command:
                speak("Goodbye!")
                break
