# import speech_recognition as sr
import webbrowser
import os
import pywintypes
from win10toast import ToastNotifier
import ctypes
import winshell
import requests
import json
import wolframalpha
import time
from selenium import webdriver
import urllib.request
import re
import pyautogui
from word2number import w2n

import pyttsx3 as tts

from datetime import datetime

from wiki_automation import information
from youtube_automation import playVideo
from notepad_auto import notepadAuto

# from AttendanceProject import Recognition

toast = ToastNotifier()
toast.show_toast("My Assistant", "Your Assistant is ready", duration=1)
os.chdir("E:\Projects\SpeechRecognition")

r = sr.Recognizer()
speaker = tts.init()
speaker.setProperty('rate', 130)
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[1].id)


def record_audio(ask=''):
    with sr.Microphone() as source:
        r.energy_threshold = 3000  # Captures even the low voices when value increased
        r.adjust_for_ambient_noise(source, 1)  # cancel noises around you
        r.dynamic_energy_threshold = True
        if ask:
            say(ask)
        audio = r.listen(source)
        voice_input = ''
        try:
            voice_input = r.recognize_google(audio)
            # print(voice_input)
        except sr.UnknownValueError:
            pass
            # say('Sorry, I did not get that')

        except sr.RequestError:
            say('Sorry, my speech is down')

        return voice_input


def say(text):
    speaker.say(text)
    speaker.runAndWait()


def respond(voice_input):
    if 'name' in voice_input:
        say('My name is Joker')

    elif 'time' in voice_input:
        # say(ctime())
        now = datetime.now()
        say(now.strftime('%I:%M %p'))
    elif 'search' in voice_input:
        search = record_audio('What do you want to search for?')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        say('Here is what I found for ' + search)


    elif 'where is' in voice_input.lower():
        index = voice_input.lower().split().index("is")

        # location = record_audio('What is the location')
        location = voice_input.split()[index + 1:]
        url = 'https://google.nl/maps/place/' + "".join(location)
        webbrowser.get().open(url)
        say("Here is the location of " + str(location))

    elif 'my location' in voice_input.lower():
        url = "https://maps.google.com/?saddr=My+Location/"
        # url = "https://www.google.com/maps/place/My%20Location"
        webbrowser.get().open(url)
        say("Here is your location")

    elif "directions to" in voice_input.lower():
        index = voice_input.lower().split().index("to")
        destination = voice_input.split()[index + 1:]
        url = "https://maps.google.com/?saddr=My%20Location/&daddr=" + "".join(destination)
        webbrowser.get().open(url)
        say("Here are the directions")

    elif "weather" in voice_input.lower():
        key = "657e01b607aaf93eaa33b18766b2bf89"
        weather_url = "https://api.openweathermap.org/data/2.5/weather?"
        index = voice_input.split().index("in")
        location = voice_input.split()[index + 1:]
        url = weather_url + "appid=" + key + "&q=" + "".join(location)
        js = requests.get(url).json()
        if js["cod"] != "404":
            temperature = js["main"]["temp"] - 273.15  # in celsius
            feels_like = js["main"]["feels_like"] - 273.15
            temperature = int(temperature)
            feels_like = int(feels_like)
            response = "The temperature in " + str(location) + " is " + str(temperature) + " degree celsius" + \
                       ", and it feels like " + str(feels_like)
            say(response)
            print(response)
        else:
            say("City not found")

    elif "calculate" in voice_input.lower():
        app_id = "8RUQQ7-2EX9QU9RGG"
        client = wolframalpha.Client(app_id)
        index = voice_input.lower().split().index("calculate")
        text = voice_input.split()[index + 1:]
        res = client.query(" ".join(text))
        answer = next(res.results).text
        if answer.find('.') is not -1:
            ansIndex = answer.find('.')
            answer = answer[:ansIndex + 3]
        # answer = round(float(answer),2)
        print("The answer is " + str(answer))
        say("The answer is " + str(answer))

    elif 'bye' in voice_input:
        say("Have a good day sir. Bye ")
        exit()

    elif 'information' in voice_input:
        info = record_audio('What information do you want?')
        # say("Here is what I found for {}".format(info))
        assist = information()
        say("Here is what I found for {}".format(info))
        assist.get_info(info)

    elif 'play' and 'video' in voice_input:
        say("Sure, Which video would you like me to play?")
        # video = record_audio('Sure, Which video would you like me to play?')
        video = ''
        while video == '':
            video = record_audio()
        say("Playing {} on youtube".format(video))
        assist = playVideo()
        assist.play(video)

    elif 'open' in voice_input.lower():

        if 'notepad' in voice_input.lower():
            np = notepadAuto()
            np.open()
            say("What do you want to write?")

            while True:
                voice = record_audio()
                if "close Notepad" in voice:
                    np.close()
                    break
                np.write(voice + " .")

        elif "word" in voice_input.lower():
            say("Opening word!")
            os.startfile(r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE")

        elif "google" in voice_input.lower():
            say("Opening Google!")
            webbrowser.open("https://google.com")

    elif "youtube" in voice_input.lower():
        index = voice_input.lower().split().index('youtube')
        search = voice_input.split()[index + 1:]
        # webbrowser.open("https://www.youtube.com/results?search_query=" + "+".join(search))
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + "+".join(search))
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

        webbrowser.open("https://www.youtube.com/watch?v=" + video_ids[0])
        html.close()
        say("Playing " + str(search) + " on youtube")


    elif "empty recycle bin" in voice_input.lower():
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)

        say("Recycle bin emptied successfully")

    elif "please sleep" in voice_input:

        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


def main():
    # recog = Recognition() // for face recognition
    # name = recog.match()
    # name = "Shivam Mahajan"
    trigger = 0

    # while int(trigger) != 1729:
    #     trigger = record_audio()
    # print(trigger)

    say("Hello, I am your virtual assistant.")

    say("How may I help you?")
    while True:
        voice_data = record_audio()
        if "stop listening" in voice_data.lower():

            say("Stopped Listening")

            while True:
                voice_data = record_audio()
                if "start listening" in voice_data.lower():
                    say("Started listening")
                    break
        print(voice_data)
        respond(voice_data)


if __name__ == '__main__':
    main()
