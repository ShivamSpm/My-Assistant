import speech_recognition as sr
import webbrowser
import os
import time
import playsound
import pyttsx3 as tts

from gtts import gTTS
from datetime import datetime

from wiki_automation import information
from youtube_automation import playVideo
from notepad_auto import notepadAuto

r = sr.Recognizer()
speaker = tts.init()
speaker.setProperty('rate', 130)
voices = speaker.getProperty('voices')
speaker.setProperty('voice',voices[1].id)


def record_audio(ask=''):
    with sr.Microphone() as source:
        r.energy_threshold = 4000 # Captures even the low voices when value increased
        r.adjust_for_ambient_noise(source,0.5) #cancel noises around you
        r.dynamic_energy_threshold = True
        if ask:
            say(ask)
        audio = r.listen(source)
        voice_input = ''
        try:
            voice_input = r.recognize_google(audio)
            # print(voice_input)
        except sr.UnknownValueError:

            say('Sorry, I did not get that')

        except sr.RequestError:
            say('Sorry, my speech is down')

        return voice_input

#
# def textToSpeech(audio_string):
#     tts = gTTS(audio_string, lang='en')
#     ran = random.randint(1, 10000)
#     audio_file = 'audio-' + str(ran) + '.mp3'
#     tts.save(audio_file)
#     # playsound.playsound(audio_file)
#     speaker.say(audio_file)
#     speaker.runAndWait()
#     # song = AudioSegment.from_mp3(audio_file)
#     # play(song)
#     # print(audio_file)
#     os.remove(audio_file)

def say(text):
    speaker.say(text)
    speaker.runAndWait()

def respond(voice_input):
    if 'name' in voice_input:
        say('My name is Chinal')

    elif 'time' in voice_input:
        # say(ctime())
        now = datetime.now()
        say(now.strftime('%I:%M %p'))
    elif 'search' in voice_input:
        search = record_audio('What do you want to search for?')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        say('Here is what I found for ' + search)

    elif 'find location' in voice_input:
        location = record_audio('What is the location')

        url = 'https://google.nl/maps/place/' + location + "/&amp;"
        webbrowser.get().open(url)
        say("Here is the location of " + location)

    elif 'my location' and 'current location' in voice_input:

        url = 'https://maps.google.com/?saddr=My%20Location/'
        webbrowser.get().open(url)
        say("Here is your location")

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
        video = record_audio('Sure, Which video would you like me to play?')
        say("Playing {} on youtube".format(video))
        assist = playVideo()
        assist.play(video)

    elif 'Notepad' in voice_input:
        np = notepadAuto()
        np.open()
        say("What do you want to write?")

        while True:

            voice = record_audio()
            if "close Notepad" in voice:
                np.close()
                break
            np.write(voice+" .")
    elif "please sleep" in voice_input:
        print(voice_input)
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def main():
    # time.sleep(1)

    say("Hello, I am your virtual assistant.")
    # voice_data = record_audio()
    # if "What" and "about" and "you" in voice_data:
    #     say("I am having a good day sir, Thank you")

    say("How may I help you?")
    while True:
        voice_data = record_audio()
        respond(voice_data)

if __name__ == '__main__':
    main()