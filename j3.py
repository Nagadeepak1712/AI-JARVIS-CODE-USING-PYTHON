import speech_recognition as sr
import pyttsx3
import requests
from bs4 import BeautifulSoup
import datetime
import os
import subprocess
import webbrowser

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not catch that.")
            return None
        except sr.RequestError:
            speak("Sorry, there seems to be a problem with the service.")
            return None

def get_weather(city):
    api_key = "YOUR_API_KEY"  # Replace with your OpenWeatherMap API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"] - 273.15  # Convert from Kelvin to Celsius
        weather_description = data["weather"][0]["description"]
        return f"The temperature in {city} is {temperature:.2f}°C with {weather_description}."
    else:
        return "City not found."

def get_wikipedia_summary(query):
    response = requests.get(f"https://en.wikipedia.org/wiki/{query}")
    soup = BeautifulSoup(response.content, "html.parser")
    paragraphs = soup.find_all("p")
    if paragraphs:
        return paragraphs[0].text
    else:
        return "No information found."

def search_web(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")

def set_reminder(task):
    reminder_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
    return reminder_time

def open_application(app_name):
    if app_name.lower() == "calculator":
        subprocess.Popen("calc.exe")  # For Windows
        # subprocess.Popen(["gnome-calculator"])  # For Linux
        speak("Opening Calculator.")
    elif app_name.lower() == "notepad":
        subprocess.Popen("notepad.exe")  # For Windows
        # subprocess.Popen(["gedit"])  # For Linux
        speak("Opening Notepad.")
    else:
        speak("Application not recognized.")

def shutdown_computer():
    speak("Shutting down now.")
    os.system("shutdown /s /t 1")  # For Windows
    # os.system("sudo shutdown now")  # For Linux

def main():
    reminders = []
    speak("Hello! I am your assistant. How can I help you today?")

    while True:
        command = listen()
        if command:
            if "weather" in command:
                if "in" in command:
                    city = command.split("in")[-1].strip()
                    weather_info = get_weather(city)
                    speak(weather_info)
                else:
                    speak("Please specify the city.")
            elif "wikipedia" in command:
                if "about" in command:
                    topic = command.split("about")[-1].strip()
                    summary = get_wikipedia_summary(topic)
                    speak(summary)
                else:
                    speak("Please specify what you want to know about.")
            elif "search for" in command:
                query = command.split("search for")[-1].strip()
                search_web(query)
                speak(f"Searching the web for {query}.")
            elif "remind me to" in command:
                task = command.split("remind me to")[-1].strip()
                reminder_time = set_reminder(task)
                reminders.append({"task": task, "time": reminder_time})
                speak(f"Reminder set for {task}.")
            elif "check reminders" in command:
                if reminders:
                    for reminder in reminders:
                        speak(f"Reminder: {reminder['task']} at {reminder['time']}")
                else:
                    speak("You have no reminders.")
            elif "open" in command:
                if "calculator" in command or "notepad" in command:
                    app_name = command.split("open")[-1].strip()
                    open_application(app_name)
                else:
                    speak("I can only open Calculator or Notepad.")
            elif "shutdown" in command:
                shutdown_computer()
                break
            else:
                speak("Sorry, I didn't understand that command.")
                
        # Check reminders
        current_time = datetime.datetime.now()
        for reminder in reminders[:]:
            if current_time >= reminder["time"]:
                speak(f"Reminder: {reminder['task']}")
                reminders.remove(reminder)

if __name__ == "__main__":
    main()
