from datetime import datetime
import multiprocessing
from random import choice
from typing import Self
import numpy as np
import sounddevice as sd
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.config import Config
from kivy.graphics import Rotate, Rectangle, Color
from kivy.uix.image import Image
# import speech_recognition as sr
import speech_recognition as sr
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import time
from kivy.uix.textinput import TextInput
import threading
import keyboard
import pyttsx3
import pyautogui
import webbrowser
import os
import subprocess as sp
import pywhatkit
import wolframalpha
import imdb
import pprint
import requests
from conv import random_text
from multiprocessing.pool import ThreadPool
from deco_rator import *
# from main import wish_me,take_user_input

from online import find_my_ip, youtube, search_on_google, search_on_wikipedia, send_email, get_latest_news, \
    get_random_joke, get_weather_report

# Set the width and height of the screen
width, height = 1920, 1080

# Print the width and height for verification
print(width, height)

# Configure the graphics settings
Config.set('graphics', 'width', width)
Config.set('graphics', 'height', height)
Config.set('graphics', 'fullscreen', 'True')

# Get the configured screen width and height
SCREEN_WIDTH = Config.getint('graphics', 'width')
SCREEN_HEIGHT = Config.getint('graphics', 'height')

# Print the screen width and height for verification
print(SCREEN_WIDTH, SCREEN_HEIGHT)

engine = pyttsx3.init('sapi5')

engine.setProperty('volume', 1.5)
engine.setProperty('rate', 220)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()


@threaded
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        # elif 'what is' in query or 'who is' in query or 'which is' in query or 'where did ' in query:
        #             app_id = ""  # Replace with your actual Wolfram Alpha App ID
        #             client = wolframalpha.Client(app_id)
        #             try:

        #                 ind = query.lower().index('what is') if 'what is' in query.lower() else \
        #                     query.lower().index('who is') if 'who is' in query.lower() else \
        #                         query.lower().index('which is') if 'which is' in query.lower() else None

        #                 if ind is not None:
        #                     text = query.split()[ind + 2:]
        #                     res = client.query(" ".join(text))
        #                     ans = next(res.results).text
        #                     speak("The answer is " + ans)
        #                     print("The answer is " + ans)
        #                 else:
        #                     speak("I couldn't find that. Please try again.")
        #             except StopIteration:
        #                 speak("I couldn't find that. Please try again.")

        # elif 'ip address' in query:
        #             ip_address = find_my_ip()
        #             speak(
        #                 f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
        #             print(f'Your IP Address is {ip_address}')

        elif 'search on wikipedia' in query:
        speak('What do you want to search on Wikipedia, sir?')
        return_val = take_command().result_queue.get()
        results = search_on_wikipedia(return_val)
        speak(f"According to Wikipedia, {results}")
        # speak("For your convenience, I am printing it on the screen sir.")
        # print(results)

    elif 'youtube' in query:
    speak('What do you want to play on Youtube, sir?')
    video = take_command().result_queue.get()
    play_on_youtube(video)

elif 'search on google' in query:
speak('What do you want to search on Google, sir?')
query = take_command().result_queue.get()
search_on_google(query)

elif "send an email" in query:
speak("On what email address do I send sir? Please enter in the console: ")
receiver_address = input("Enter email address: ")
speak("What should be the subject sir?")
subject = take_command().result_queue.get()
speak("What is the message sir?")
message = take_command().result_queue.get()
if send_email(receiver_address, subject, message):
    speak("I've sent the email sir.")
    print("I've sent the email sir.")
else:
    speak("Something went wrong while I was sending the mail. Please check the error logs sir.")

# elif 'tell me any joke' in query:
#             speak(f"Hope you like this one sir")
#             joke = get_random_joke()
#             speak(joke)
#             speak("For your convenience, I am printing it on the screen sir.")
#             pprint(joke)

elif 'movie' in query:
movies_db = imdb.IMDb()
speak("please tell me the movie name :")
text = take_command().result_queue.get()
movies = movies_db.search_movie(text)
speak("Searching for" + text)
speak("I Found these: ")
for movie in movies:
    title = movie["title"]
    year = movie["year"]
    speak(f"{title}-{year}")
    info = movie.getID()
    movie_info = movies_db.get_movie(info)
    rating = movie_info["rating"]
    cast = movie_info["cast"]
    actor = cast[0:5]
    plot = movie_info.get('plot outline', 'Plot summary not available')
    speak(
        f'{title} was released in {year} has imdb ratings of {rating}.It has a cast of {actor} . The plot summary'
        f'of movie is {plot}')
    print(
        f'{title} was released in {year} has imdb ratings of {rating}.It has a cast of {actor} The plot summary '
        f'of movie is {plot}')

elif 'give me news' in query:

speak(f"I'm reading out the latest news hea`dlines, sir")
speak(get_latest_news())

elif 'weather' in query:
ip_address = find_my_ip()
city = 'indore'
speak(f"Getting weather report for your city {city}")
weather, temperature, feels_like = get_weather_report(city)
speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
speak(f"Also, the weather report talks about {weather}")
speak("For your convenience, I am printing it on the screen sir.")
print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")


# Custom Kivy App class
class MyKivyApp(App):

    def build(self):
        # speak('Hey Dhruv I am Jarvis your personal assistant')

        circle_widget = CircleWidget()

        # Start listening to the audio stream
        circle_widget.start_listening()

        # Schedule the update events for the circle widget
        self.update_event = Clock.schedule_interval(circle_widget.update_circle, 1 / 60)
        self.btn_rotation_event = Clock.schedule_interval(circle_widget.circle.rotate_button, 1 / 60)

        return circle_widget


# Run the Kivy application
if __name__ == '__main__':
    MyKivyApp().run()