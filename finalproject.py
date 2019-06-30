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


# [START speech_transcribe_sync]
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

def speak(response, counter):
    with open(str(counter)+ ".mp3", 'wb') as out:

        out.write(response.audio_content)

        out.close()
    file = str(counter)+ ".mp3"
    loadmp3player(file)

# Set the text input to be synthesized

def verify_response(response, expectation):
    print(response)
    if response.split(" ")[0] == "yeah" or response.split(" ")[0] == "had" or response.split(" ")[0] == "fun" or response.split(" ")[0] == "weekend" or response.split(" ")[0] == "went":
        return False


    accepted = []
    if expectation == "action":
        accepted = ["Arts & Entertainment",
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
                    "Travel"]
    classification = classify(response)
    for (category, confidence) in classification.items():
        try:
            end = category[1:].index("/")
            broad_category = category[1:end+1]
        except:
            broad_category = category[1:]
        print(broad_category)
        if broad_category in accepted:
            return True
    return False
def remove(mydir):
    filelist = [ f for f in os.listdir(mydir) if f.endswith(".mp3") ]
    for f in filelist:
        os.remove(os.path.join(mydir, f))
def conversation():
    entry = texttospeech.types.SynthesisInput(text="Hey what's up! My name is Sara! What's your name?")
    action = ["Awesome!", "I had a fun weekend", "I went swimming in our community pool", "What did you do over the weekend?"]
    critic = "Try again"
    affirmation = "That sounds good"
    reinforcement = "Awesome job!"

    food = ["Awesome!", "Man, these cookies are delicious", "What's your favorite dessert?"]

    exit = texttospeech.types.SynthesisInput(text="That sounds great! Well it was good catching up! See you around!")
    conversations = [action]

    girl = texttospeech.types.VoiceSelectionParams(
        language_code='en-US', name = 'en-US-Wavenet-F',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)


    coach = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type


    convoDone = False

    counter = 0

    while convoDone == False:
        girlspeak = client.synthesize_speech(entry, girl, audio_config)
        counter += 1
        speak(girlspeak, counter)
        time.sleep(4)
        name = transcribe_file(record_file(5))
        convo = random.choice(conversations)
        girlspeak = client.synthesize_speech(texttospeech.types.SynthesisInput(text=name), girl, audio_config)
        counter += 1
        speak(girlspeak, counter)
        notYet = True
        if convo == action:
            for item in convo:
                girlspeak = client.synthesize_speech(texttospeech.types.SynthesisInput(text=item), girl, audio_config)
                counter += 1
                speak(girlspeak, counter)
                # if len(item.split(" ")) != 1:
                #     for word in item.split(" "):
                #         if len(word) > 1 and verify_response(twenty(word), "action"):
                #             openImage("beet")
                time.sleep(1.5)
                if convo.index(item) == len(convo)-1:
                    response = transcribe_file(record_file(5))
                    while notYet:
                        if response == None:
                            coachspeak = client.synthesize_speech(texttospeech.types.SynthesisInput(text= ("That's not an action")), coach, audio_config)
                            counter += 1
                            speak(coachspeak, counter)
                            time.sleep(1.5)
                            coachspeak = client.synthesize_speech(texttospeech.types.SynthesisInput(text=critic), coach, audio_config)
                            counter += 1
                            speak(coachspeak, counter)
                            time.sleep(1.5)
                            girlspeak = client.synthesize_speech(texttospeech.types.SynthesisInput(text=convo[-1]), girl, audio_config)
                            counter += 1
                            speak(girlspeak, counter)
                            time.sleep(1.5)
                            response = transcribe_file(record_file(5))
                        else:
                            i = response.split(" ")[-1]
                            print(i)
                            if verify_response(twenty(i), "action") and ("I" not in response and "did" not in response):
                                coachspeak = client.synthesize_speech(texttospeech.types.SynthesisInput(text=affirmation), coach, audio_config)
                                counter += 1
                                speak(coachspeak, counter)
                                time.sleep(1.5)
                                coachspeak = client.synthesize_speech(texttospeech.types.SynthesisInput(text="Let's give a better response"), coach, audio_config)
                                counter += 1
                                speak(coachspeak, counter)
                                time.sleep(1.5)
                                coachspeak = client.synthesize_speech(texttospeech.types.SynthesisInput(text=("Say I did" + str(i))), coach, audio_config)
                                counter += 1
                                speak(coachspeak, counter)
                                time.sleep(1.5)
                                response = transcribe_file(record_file(5))
                                print(response)
                                if "I" in response or "did" in response:
                                    coachspeak = client.synthesize_speech(texttospeech.types.SynthesisInput(text=reinforcement), coach, audio_config)
                                    counter += 1
                                    speak(coachspeak, counter)
                                    time.sleep(1.5)
                                    girlspeak = client.synthesize_speech(texttospeech.types.SynthesisInput(text=convo[-1]), girl, audio_config)
                                    counter += 1
                                    speak(girlspeak, counter)
                                    time.sleep(1.5)
                                    response = transcribe_file(record_file(5))
                                    if "I" in response or "did" in response:
                                        notYet = False
                            elif verify_response(twenty(i), "action") == False:
                                coachspeak = client.synthesize_speech(texttospeech.types.SynthesisInput(text= ("That's not an action")), coach, audio_config)
                                counter += 1
                                speak(coachspeak, counter)
                                time.sleep(1.5)
                                coachspeak = client.synthesize_speech(texttospeech.types.SynthesisInput(text=critic), coach, audio_config)
                                counter += 1
                                speak(coachspeak, counter)
                                time.sleep(1.5)
                                girlspeak = client.synthesize_speech(texttospeech.types.SynthesisInput(text=convo[-1]), girl, audio_config)
                                counter += 1
                                speak(girlspeak, counter)
                                time.sleep(1.5)
                                response = transcribe_file(record_file(5))
                            elif verify_response(twenty(i), "action") and ("I" in response or "did" in response):
                                coachspeak = client.synthesize_speech(texttospeech.types.SynthesisInput(text=reinforcement), coach, audio_config)
                                counter += 1
                                speak(coachspeak, counter)
                                time.sleep(1.5)
                                notYet = False
        girlspeak = client.synthesize_speech(exit, girl, audio_config)
        counter += 1
        speak(girlspeak, counter)
        time.sleep(5)
        remove("/Users/sunjana/Desktop/TartanHacks2k19")
        convoDone = True





conversation()

# # The response's audio_content is binary.
# with open('output.mp3', 'wb') as out:
#     # Write the response to the output file.
#     out.write(response.audio_content)
#     print('Audio content written to file "output.mp3"')
#     loadmp3player("output.mp3")


    # [END speech_python_migration_sync_response]
# [END speech_transcribe_sync]
