# from __future__ import division
#
# import re
# import sys
# import time
# import io
#
# from google.cloud import speech
# from google.cloud.speech import enums
# from google.cloud.speech import types
# import pyaudio
# import wave
# from six.moves import queue
#
# import time
#
# from google.cloud import texttospeech
# client = texttospeech.TextToSpeechClient()
#
#
#
#
# import pygame
#
# i = 0
#
#
# string = " "
# def transcribe_file(speech_file):
#     """Transcribe the given audio file."""
#     from google.cloud import speech
#     from google.cloud.speech import enums
#     from google.cloud.speech import types
#     client = speech.SpeechClient()
#
#     with io.open(speech_file, 'rb') as audio_file:
#         content = audio_file.read()
#     # print("read content file")
#
#     audio = types.RecognitionAudio(content=content)
#     config = types.RecognitionConfig(
#         encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
#         sample_rate_hertz=44100,
#         language_code='en-US')
#
#     # print("config done")
#     response = client.recognize(config, audio)
#     # print("response found")
#     # Each result is for a consecutive portion of the audio. Iterate through
#     # them to get the transcripts for the entire audio file.
#     for result in response.results:
#         # The first alternative is the most likely one for this portion.
#
#         # print(u'Transcript: {}'.format(result.alternatives[0].transcript))
#         return result.alternatives[0].transcript
#
# def loadmp3player(file):
#         # print(file)
#         pygame.init()
#         pygame.mixer.init()
#         pygame.mixer.music.load(file)
#         pygame.mixer.music.play()
#         time.sleep(0.5)
# def speech():
#     synthesis_input = texttospeech.types.SynthesisInput(text="Hello")
#
#     voice = texttospeech.types.VoiceSelectionParams(
#         language_code='en-US',
#         ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
#     audio_config = texttospeech.types.AudioConfig(
#         audio_encoding=texttospeech.enums.AudioEncoding.MP3)
#     response = client.synthesize_speech(synthesis_input, voice, audio_config)
#     return response

from google.cloud import texttospeech

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
synthesis_input = texttospeech.types.SynthesisInput(text="Hello, World!")

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.types.VoiceSelectionParams(
    language_code='en-US',
    ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

# Select the type of audio file you want returned
audio_config = texttospeech.types.AudioConfig(
    audio_encoding=texttospeech.enums.AudioEncoding.MP3)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(synthesis_input, voice, audio_config)

# The response's audio_content is binary.
with open('output.mp3', 'wb') as out:
    # Write the response to the output file.
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')

#
# def record_file(time):
#     language_code = 'en-US'  # a BCP-47 language tag
#     words = []
#     CHUNK = 1024
#     FORMAT = pyaudio.paInt16
#     CHANNELS = 1
#     RATE = 44100
#     RECORD_SECONDS = time
#     WAVE_OUTPUT_FILENAME = "voice.wav"
#
#     p = pyaudio.PyAudio()
#
#     stream = p.open(format=FORMAT,
#                     channels=CHANNELS,
#                     rate=RATE,
#                     input=True,
#                     frames_per_buffer=CHUNK)
#
#     print("* recording")
#
#     frames = []
#
#     for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#         data = stream.read(CHUNK)
#         frames.append(data)
#
#     print("* done recording")
#
#     stream.stop_stream()
#     stream.close()
#     p.terminate()
#
#     wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#     wf.setnchannels(CHANNELS)
#     wf.setsampwidth(p.get_sample_size(FORMAT))
#     wf.setframerate(RATE)
#
#
#     wf.writeframes(b''.join(frames))
#     wf.close()






























# import os, requests, time
# from xml.etree import ElementTree
# try: input = raw_input
# except NameError: pass
# class TextToSpeech(object):
#     def __init__(self, subscription_key):
#         self.subscription_key = "92c3294749ee4d70855ebcd48cabc04f"
#         self.tts = input("I like chicken")
#         self.timestr = time.strftime("%Y%m%d-%H%M")
#         self.access_token = None
#     def get_token(self):
#         fetch_token_url = "https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
#         headers = {
#             'Ocp-Apim-Subscription-Key': self.subscription_key
#         }
#         response = requests.post(fetch_token_url, headers=headers)
#         self.access_token = str(response.text)
#     def save_audio(self):
#         base_url = 'https://eastus.tts.speech.microsoft.com/'
#         path = 'cognitiveservices/v1'
#         constructed_url = base_url + path
#         headers = {
#             'Authorization': 'Bearer ' + self.access_token,
#             'Content-Type': 'application/ssml+xml',
#             'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
#             'User-Agent': 'TartanHacks'
#         }
#         xml_body = ElementTree.Element('speak', version='1.0')
#         xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
#         voice = ElementTree.SubElement(xml_body, 'voice')
#         voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
#         voice.set('name', 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)')
#         voice.text = self.tts
#         body = ElementTree.tostring(xml_body)
#
#         response = requests.post(constructed_url, headers=headers, data=body)
#         if response.status_code == 200:
#             with open('sample-' + self.timestr + '.wav', 'wb') as audio:
#                 audio.write(response.content)
#                 print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
#         else:
#             print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
# if __name__ == "__main__":
#     subscription_key = "92c3294749ee4d70855ebcd48cabc04f"
#     app = TextToSpeech(subscription_key)
#     app.get_token()
#     app.save_audio()
