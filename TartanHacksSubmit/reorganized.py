##introduction is only needed in some scenarios

from __future__ import division

import re
import sys
import time
import io
import os
import random
import six
from classify_text_tutorial import classify
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
import wave
from six.moves import queue
import pygame
import time

from google.cloud import texttospeech
client = texttospeech.TextToSpeechClient()
def twenty(text):
    i = 0
    str = ""
    if len(text) < 20:
        while i < 20:
            str += text
            str += " "
            i += 1


    return str

def record_file(time):
    language_code = 'en-US'  # a BCP-47 language tag
    words = []
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = time
    WAVE_OUTPUT_FILENAME = "voice.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)


    wf.writeframes(b''.join(frames))
    wf.close()
    return WAVE_OUTPUT_FILENAME

def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()
    # print("read content file")

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='en-US')

    # print("config done")
    response = client.recognize(config, audio)
    # print("response found")
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.

        # print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        return result.alternatives[0].transcript

def loadmp3player(file):
        # print(file)
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        time.sleep(0.5)

def speak(entry, character, counter):
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)
    speaker = client.synthesize_speech(texttospeech.types.SynthesisInput(text=entry), character, audio_config)
    with open(str(counter)+ ".mp3", 'wb') as out:

        out.write(speaker.audio_content)

        out.close()
    file = str(counter)+ ".mp3"
    loadmp3player(file)
def respond():
    print("Recording...")
    answer = transcribe_file(record_file(5))
    return answer

#issue: we have to figure out how to get all possible categories without hardcoding at some point

class FriendConvo():
    def __init__(self, exposition, intro, questions, counter, coachprompt, required, accepted):
        self.exposition = exposition
        self.intro = intro
        self.questions = questions
        self.counter = counter
        self.required = required
        self.accepted = accepted
        self.coachprompt = coachprompt
        self.girl = texttospeech.types.VoiceSelectionParams(
        language_code='en-US', name = 'en-US-Wavenet-F',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)
        self.coach = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
    def introduction(self):
        speak(self.intro, self.girl, self.counter)
        time.sleep(3.5)
        self.counter += 1
        response = respond()
        speak(response  + ". Awesome", self.girl, self.counter)
        self.counter += 1
    def background(self):
        for item in self.exposition:
            speak(item, self.girl, self.counter)
            self.counter += 1
            time.sleep(1.5)
    def q(self):
        for item in self.questions:
            speak(item, self.girl, self.counter)
            time.sleep(2)
            self.counter += 1
            response = respond()
            while(self.appropriate(response) == False):
                speak("That's not a" + self.required + " . Try again", self.coach, self.counter)
                self.counter += 1
                time.sleep(1.5)
                speak(item, self.girl, self.counter)
                time.sleep(2)
                self.counter += 1
                response = respond()
            while(self.complete(response) == False):
                speak("That's good. Let's give a better answer. Say" + self.coachprompt + response, self.coach, self.counter)
                self.counter += 1
                time.sleep(4)
                response = respond()
                if(self.complete(response) == True):
                    speak("Awesome job. Now answer the question", self.coach, self.counter)
                    self.counter += 1
                    time.sleep(1.5)
                    speak(item, self.girl, self.counter)
                    time.sleep(1.5)
                    self.counter += 1
                    response = respond()
            speak("Cool!", self.girl, self.counter)
            self.counter += 1


        # speak("That sounds great", self.girl, self.counter)
        # self.counter += 1
        time.sleep(1)
        speak("Well, it was good catching up. See you later!", self.girl, self.counter)
        time.sleep(3.5)
        print("Finished")
    def appropriate(self, response):
        classification = classify(twenty(response))
        a = ""
        for (category, confidence) in classification.items():
            try:
                end = category[1:].index("/")
                broad_category = category[1:end+1]
                print(broad_category)
            except:
                broad_category = category[1:]
                print(broad_category)
        #
            if broad_category in self.accepted:
                return True
        # print(broad_category)
        return False

    def complete(self, response):
        for item in self.coachprompt.split(" "):
            if item not in response:
                return False
        return True

lastWeekend = FriendConvo(["I had a fun weekend", "I went swimming in our community pool"], "Hey what's up! My name is Sara. What's your name?", ["What did you do over the weekend"], 0, "I went", "action", ["Arts & Entertainment",
                    "Books & Literature",
                    "Computers & Electronics",
                    "Games",
                    "Hobbies & Leisure",
                    "Home & Garden",
                    "Jobs & Education",
                    "Online Communities",
                    "People & Society",
                    "Pets & Animals",
                    "Shopping",
                    "Sports",
                    "Travel"])
lastWeekend.introduction()
time.sleep(1.5)
lastWeekend.background()
time.sleep(1.5)
lastWeekend.q()



#
# moviecategories = ["Arts & Entertainment"]
# movie = FriendConvo(["I just watched the Avengers in 3D!", "It was so awesome!"], "Hey what's up! My name is Sara. What's your name?", ["What's your favorite movie?"], 0, "I like", "movie", moviecategories)
# movie.appropriate("The Polar Express")
# movie.introduction()
# time.sleep(1.5)
# movie.background()
# time.sleep(1.5)
# movie.q()
