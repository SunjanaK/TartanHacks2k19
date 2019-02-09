from __future__ import division

import re
import sys
import time
import io
import random
import string

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import six

#import pyaudio
import wave
from six.moves import queue
#import pygame

import time

from classify_text_tutorial import classify

from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()


'''
def record_file(time):
    language_code = 'en-US'  # a BCP-47 language tag
    words = []
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = time
    WAVE_OUTPUT_FILENAME = "voice2.wav"

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
'''

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


def verify_response(response, expectation):

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

# Set the text input to be synthesized

entry = texttospeech.types.SynthesisInput(
    text="Hey what's up! My name is Sara! What's your name?")

name = "Bas"

action_text = ["Awesome!", "I had a fun weekend",
               "I went swimming in our community pool",
               name + ", what did you do over the weekend?"]

critic = ["Please try again, " + name]

food_text = ["Awesome!", "Man, these cookies are delicious",
             "What's your favorite dessert?"]

exit = texttospeech.types.SynthesisInput(
    text="That sounds great! Well it was good catching up! See you around!")
conversations = [action_text, food_text]

girl = texttospeech.types.VoiceSelectionParams(
    language_code='en-US',
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

print("hello")

print(classify("dog " * 500))
print(verify_response("dog "*500, "action"))
'''
while not convoDone:
    girlspeak = client.synthesize_speech(entry, girl, audio_config)
    # to transcribe_file(record_file(5)) and "My name is" not in response
    coachspeak = client.synthesize_speech(critic, coach, audio_config)
    convo = random.choice(conversations)
    for item in convo:
        girlspeak = client.synthesize_speech(item, girl, audio_config)
    ##el

coachspeak = client.synthesize_speech(synthesis_input, )


#
#


def loadmp3player(file):
    # print(file)
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    time.sleep(0.5)


# # The response's audio_content is binary.
# with open('output.mp3', 'wb') as out:
#     # Write the response to the output file.
#     out.write(response.audio_content)
#     print('Audio content written to file "output.mp3"')
#     loadmp3player("output.mp3")
# [END speech_python_migration_sync_response]
# [END speech_transcribe_sync]
print(transcribe_file(record_file(5)))
'''