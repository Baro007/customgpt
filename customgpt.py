import openai
import elevenlabs
import asyncio
import logging
import os
import httpx
import sounddevice as sd
import soundfile as sf
import numpy as np
import time
import io
import base64
import websockets
import json
from io import BytesIO
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from PIL import ImageGrab
from pynput import keyboard
from dotenv import load_dotenv
from io import BytesIO
from typing import IO
import threading
import subprocess
import wave
import pyaudio
import aiohttp

# API anahtarlarını ve diğer konfigürasyonları yükle
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ],
)

# Global değişkenler
recording = False
stop_recording = False
audio_data = []
fs = 16000
messages = []
current_playback = None

# Konuşma geçmişini kaydetmek için dosya yolu
conversation_history_file = "conversation_history.txt"

# ElevenLabs client'ı başlatın
client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)


async def get_audio_input():
    global recording, stop_recording, audio_data
    audio_data = []
    recording = True
    print("Kayıt başladı. Konuşun, bitirmek için Space'e basın...")

    def callback(indata, frames, time, status):
        if recording:
            audio_data.append(indata.copy())

    def on_press(key):
        global recording, stop_recording
        if key == keyboard.Key.space:
            recording = False
            stop_recording = True
            print("Kayıt durduruldu.")
            return False

    with keyboard.Listener(on_press=on_press) as listener:
        with sd.InputStream(samplerate=fs, channels=1, callback=callback, dtype='float32'):
            while recording:
                await asyncio.sleep(0.1)

    stop_recording = False
    if len(audio_data) > 0:
        audio_data = np.concatenate(audio_data, axis=0)
    else:
        print("Ses kaydı alınamadı.")
        return None
    return audio_data

async def transcribe_audio(audio_data):
    """Ses verilerini Whisper API kullanarak metne dönüştürür ve dosyayı siler."""
    timestamp = int(time.time())
    file_name = f"input_{timestamp}.wav"
    with sf.SoundFile(file_name, mode="w", samplerate=fs, channels=1) as outfile:
        outfile.write(audio_data)

    async with httpx.AsyncClient(timeout=None) as client:
        with open(file_name, "rb") as audio_file:
            files = {"file": (file_name, audio_file, "audio/wav")}
            headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
            response = await client.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers=headers,
                files=files,
                data={"model": "whisper-1"},
            )
            response.raise_for_status()
            transcript = response.json()

    user_input = transcript["text"]
    print(f"Giriş: {user_input}")

    # Ses dosyasını sil
    os.remove(file_name)
    return user_input


async def get_gpt4_response(user_input, messages):
    """OpenAI'nin GPT-4 API'sine istek gönderir ve insansı, kısa yanıtlar alır."""
    system_message = {
        "role": "system",
        "content": "Sen bir insanla sohbet eden bir AI asistanısın. Kısa, öz ve doğal cevaplar ver. Günlük konuşma dilini kullan, akademik veya resmi bir ton kullanma. Cevapların genellikle 1-3 cümle arasında olsun. . İnsanlar gibi bazen küçük hatalar yapabilir veya tereddüt edebilirsin."
    }
    
    messages = [system_message] + messages  # System message'ı ekle
    messages.append({"role": "user", "content": user_input})

    async with httpx.AsyncClient(timeout=None) as client:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "gpt-4o",
            "messages": messages,
        }
        response = await client.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=data
        )
        response.raise_for_status()
        response_data = response.json()
    messages.append({"role": "assistant", "content": response_data['choices'][0]['message']['content']})
    return response_data['choices'][0]['message']['content']



def capture_screen():
    """Ekran görüntüsünü alır ve PIL.Image nesnesi olarak döndürür."""
    screenshot = ImageGrab.grab()
    return screenshot


def image_to_base64(image):
    """PIL.Image nesnesini base64 kodlu bir dizeye dönüştürür."""
    image = image.convert("RGB")
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return img_str


async def analyze_screenshot(query, image_base64):
    """GPT-4 Vision API'sini kullanarak ekran görüntüsünü analiz eder."""
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": [
                {"type": "text", "text": query},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
            ]}
        ],
        "max_tokens": 4000,
    }
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
    return response_data['choices'][0]['message']['content']


async def is_screenshot_needed(query):
    """OpenAI kullanarak ekran görüntüsü gereksinimini kontrol eder."""
    prompt = f"""
    Aşağıdaki kullanıcı sorgusu, bir ekran görüntüsü analizine ihtiyaç duyuyor mu?
    Sadece 'evet' veya 'hayır' olarak cevaplayın.
    Kullanıcı Sorgusu: "{query}"
    """
    async with httpx.AsyncClient() as client:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
        }
        response = await client.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=data
        )
        response.raise_for_status()
        response_data = response.json()
    return "evet" in response_data["choices"][0]["message"]["content"].strip().lower()

async def print_gpt4_response(response_text):
   """GPT-4'ten gelen yanıtı konsola yazdırır."""
   print("GPT-4 Yanıtı:", response_text)

async def save_conversation_history(user_input, response_text):
    """Konuşma geçmişini dosyaya kaydeder."""
    with open(conversation_history_file, "a", encoding="utf-8") as f:
       f.write(f"Kullanıcı: {user_input}\n")
       f.write(f"GPT-4: {response_text}\n\n")

async def text_to_speech(text):
   """ElevenLabs API'sini kullanarak metni sese dönüştürür."""
   async with httpx.AsyncClient(timeout=None) as client:  # Zaman aşımı sınırını kaldırıyoruz
       headers = {
           "xi-api-key": ELEVENLABS_API_KEY,
           "Content-Type": "application/json",
       }
       data = {
           "text": text,
            "model_id": "eleven_multilingual_v2",  # Multilingual v2 modelini kullan

           "voice_settings": {
               "stability": 0.5,
               "similarity_boost": 0.8
           }
       }
       response = await client.post(
           f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
           headers=headers,
                      json=data,
       )
       response.raise_for_status()
       audio_data = response.content


   # Bytes verisini soundfile ile aç
   with io.BytesIO(audio_data) as f:
       audio_array, samplerate = sf.read(f)


   return audio_array, samplerate



async def main():
   """Ana uygulama döngüsünü başlatır."""
   global recording, audio_data, messages
   print("Program başlatıldı.")
   print("Konuşmak için Space'e basın.")


   while True:
       # Space tuşuna basılana kadar bekle
       with keyboard.Listener(on_press=lambda key: key == keyboard.Key.space) as listener:
           listener.join()
      
       if not recording:
           audio_data = await get_audio_input()
           user_input = await transcribe_audio(audio_data)


           # Ekran görüntüsü gerekli mi kontrol et
           screenshot_needed = await is_screenshot_needed(user_input)


           if screenshot_needed:
               # Ekran görüntüsü al ve base64'e dönüştür
               screenshot = capture_screen()
               image_base64 = image_to_base64(screenshot)


               # GPT-4 Vision API ile analiz et
               response_text = await analyze_screenshot(user_input, image_base64)
           else:
               # Normal GPT-4 API ile yanıt al
               response_text = await get_gpt4_response(user_input, messages)


           await print_gpt4_response(response_text)
           await save_conversation_history(user_input, response_text)


           # Metni sese dönüştür ve çal
           audio_array, samplerate = await text_to_speech(response_text)
           sd.play(audio_array, samplerate=samplerate)
           sd.wait()


           print("Konuşmak için Space'e basın.")

if __name__ == "__main__":
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY çevre değişkeni ayarlanmadı.")
    if not ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY çevre değişkeni ayarlanmadı.")
    if not VOICE_ID:
        raise ValueError("VOICE_ID çevre değişkeni ayarlanmadı.")

    asyncio.run(main())
