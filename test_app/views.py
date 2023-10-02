from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
import random
from Test.settings import BASE_DIR
from django.shortcuts import render
from django.http import JsonResponse
import sounddevice as sd
import soundfile as sf
import numpy as np
import openai
import os
import requests
import re
from colorama import Fore, Style, init
import datetime
import time
import base64
from pydub import AudioSegment
from pydub.playback import play
import pygame
import elevenlabs
elevenlabs.set_api_key("2adca02be8233d841cff320df4e5af3e")
pygame.init()
pygame.mixer.init()

def index(request):
   
    return render(request, 'index.html')
    
def open_file(filepath):
    file_path = os.path.join(BASE_DIR, filepath)
    with open(file_path, 'r', encoding='utf-8') as infile:
        return infile.read()

api_key = open_file('openaiapikey2.txt')
elapikey = open_file('elabapikey.txt')

conversation1 = []  
chatbot1 = open_file('chatbot1.txt')


def chatgpt(api_key, conversation, chatbot, user_input, temperature=0.9, frequency_penalty=0.2, presence_penalty=0):
    openai.api_key = api_key
    conversation.append({"role": "user","content": user_input})
    messages_input = conversation.copy()
    prompt = [{"role": "system", "content": chatbot}]
    messages_input.insert(0, prompt[0])
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        temperature=temperature,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        messages=messages_input)
    chat_response = completion['choices'][0]['message']['content']
    conversation.append({"role": "assistant", "content": chat_response})
    return chat_response

str_transcription=""     
def your_view_name(request,duration=4, fs=44100):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        while True:
            print('Recording...')
            myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
            sd.wait()
            print('Recording complete.')
            filename = 'myrecording.wav'
            sf.write(filename, myrecording, fs)
            with open(filename, "rb") as file:
                openai.api_key = api_key
                result = openai.Audio.transcribe("whisper-1", file)
            transcription = result['text']
            # return transcription
            user_message = transcription
            str_transcription=transcription
            response = chatgpt(api_key, conversation1, chatbot1, user_message)
            audio= elevenlabs.generate(
            text=response,
            voice="Bella"
            )
            elevenlabs.play(audio)  
            data = {
                    "transcription": str_transcription,
                }
            return JsonResponse(data)
 
    else:
        return render(request, 'index.html')

