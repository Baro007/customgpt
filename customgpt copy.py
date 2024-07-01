import sys
import asyncio
import openai
import elevenlabs
import logging
import os
import httpx
import sounddevice as sd
import soundfile as sf
import numpy as np
import time
import io
import base64
import json
import http.client
from io import BytesIO
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from PIL import ImageGrab
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QTextEdit, QScrollArea, QLineEdit
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import qasync

# API anahtarlarını ve diğer konfigürasyonları yükle
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

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
fs = 16000
conversation_history = []

# Konuşma geçmişini kaydetmek için dosya yolu
conversation_history_file = "conversation_history.json"

# ElevenLabs client'ı başlatın
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

class AudioRecorder(QThread):
    finished = pyqtSignal(object)

    def run(self):
        global recording
        audio_data = []

        def callback(indata, frames, time, status):
            if recording:
                audio_data.append(indata.copy())

        with sd.InputStream(samplerate=fs, channels=1, callback=callback):
            while recording:
                sd.sleep(100)

        if len(audio_data) > 0:
            audio_data = np.concatenate(audio_data, axis=0)
            self.finished.emit(audio_data)
        else:
            self.finished.emit(None)

class AIAssistant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_muted = False # Başlangıçta sesi açık olarak ayarlayın
        self.initUI()
        self.recorder = AudioRecorder()
        self.recorder.finished.connect(self.on_recording_finished)
        self.load_conversation_history()
        
    # API anahtarlarını kontrol et
    print(f"OpenAI API Key: {OPENAI_API_KEY[:5]}...{OPENAI_API_KEY[-5:]}")
    print(f"ElevenLabs API Key: {ELEVENLABS_API_KEY[:5]}...{ELEVENLABS_API_KEY[-5:]}")
    print(f"Serper API Key: {SERPER_API_KEY[:5]}...{SERPER_API_KEY[-5:]}")
    
    def initUI(self):
        self.setWindowTitle('Barış AI')
        self.setGeometry(100, 100, 400, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.speak_button = QPushButton('Konuş', self)
        self.speak_button.clicked.connect(self.start_recording)
        layout.addWidget(self.speak_button)

        self.stop_button = QPushButton('Durdur', self)
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

        self.mute_button = QPushButton('Sesli Cevap Kapat', self)
        self.mute_button.setCheckable(True)
        self.mute_button.clicked.connect(self.toggle_mute)
        layout.addWidget(self.mute_button)

        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("Metin girin ve 'Gönder' butonuna tıklayın")
        layout.addWidget(self.text_input)

        self.send_button = QPushButton('Gönder', self)
        self.send_button.clicked.connect(self.send_text_input)
        layout.addWidget(self.send_button)

        self.status_label = QLabel('Hazır', self)
        layout.addWidget(self.status_label)

        self.response_area = QTextEdit(self)
        self.response_area.setReadOnly(True)
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.response_area)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        central_widget.setLayout(layout)

    def toggle_mute(self):
        self.is_muted = self.mute_button.isChecked()
        print(f"Sesli cevap {'kapatıldı' if self.is_muted else 'açık'}")

    def send_text_input(self):
        user_input = self.text_input.text().strip()
        if user_input:
            conversation_history.append({"role": "user", "content": user_input})
            self.text_input.clear()
            self.update_response_area()
            asyncio.create_task(self.process_text_input(user_input))

    async def process_text_input(self, user_input):
        try:
            self.status_label.setText("Yanıt alınıyor...")
            action = await self.decide_action(user_input)
            if action == "1":
                screenshot = self.capture_screen()
                image_base64 = self.image_to_base64(screenshot)
                response_text = await self.analyze_screenshot(user_input, image_base64)
            elif action == "2":
                response_text = await self.perform_web_search(user_input)
            else:
                response_text = await self.get_gpt4_response(user_input)

            if response_text is None:
                response_text = "Üzgünüm, bir cevap üretilemedi."

            conversation_history.append({"role": "assistant", "content": response_text})
            self.update_response_area()
            self.save_conversation_history()

            await self.print_gpt4_response(response_text)

            if not self.is_muted: # Sadece ses açıksa konuştur
                audio_array, samplerate = await self.text_to_speech(response_text)
                sd.play(audio_array, samplerate=samplerate)
                sd.wait()

            self.status_label.setText("Hazır")
        except Exception as e:
            error_message = f"Hata: {str(e)}"
            self.status_label.setText(error_message)
            self.response_area.append(error_message + "\n\n")
        finally:
            self.speak_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def start_recording(self):
        global recording
        recording = True
        self.status_label.setText("Kayıt başladı...")
        self.speak_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.recorder.start()

    def stop_recording(self):
        global recording
        recording = False
        self.status_label.setText("Kayıt durduruluyor...")
        self.speak_button.setEnabled(False)
        self.stop_button.setEnabled(False)

    def on_recording_finished(self, audio_data):
        if audio_data is not None:
            self.process_audio(audio_data)
        else:
            self.status_label.setText("Ses kaydı alınamadı")
            self.speak_button.setEnabled(True)

    def process_audio(self, audio_data):
        self.status_label.setText("Ses işleniyor...")
        asyncio.create_task(self.process_audio_async(audio_data))

    def load_conversation_history(self):
        global conversation_history
        try:
            with open(conversation_history_file, "r", encoding="utf-8") as f:
                conversation_history = json.load(f)
            self.update_response_area()
        except FileNotFoundError:
            conversation_history = []

    def save_conversation_history(self):
        with open(conversation_history_file, "w", encoding="utf-8") as f:
            json.dump(conversation_history, f, ensure_ascii=False, indent=2)

    def update_response_area(self):
        self.response_area.clear()
        for message in conversation_history:
            if message['role'] == 'user':
                self.response_area.append(f"Siz: {message['content']}\n")
            elif message['role'] == 'assistant':
                self.response_area.append(f"AI: {message['content']}\n\n")
        self.response_area.verticalScrollBar().setValue(self.response_area.verticalScrollBar().maximum())

    async def process_audio_async(self, audio_data):
        try:
            user_input = await self.transcribe_audio(audio_data)
            conversation_history.append({"role": "user", "content": user_input})
            self.update_response_area()

            action = await self.decide_action(user_input)
            print(f"Decided action: {action}")

            if action == "1":
                screenshot = self.capture_screen()
                image_base64 = self.image_to_base64(screenshot)
                response_text = await self.analyze_screenshot(user_input, image_base64)
            elif action == "2":
                response_text = await self.perform_web_search(user_input)
            else:
                response_text = await self.get_gpt4_response(user_input)

            if response_text is None:
                response_text = "Üzgünüm, bir cevap üretilemedi."

            print(f"Final response: {response_text}")

            conversation_history.append({"role": "assistant", "content": response_text})
            self.update_response_area()
            self.save_conversation_history()

            await self.print_gpt4_response(response_text)

            if not self.is_muted:
                audio_array, samplerate = await self.text_to_speech(response_text)
                sd.play(audio_array, samplerate=samplerate)
                sd.wait()

            self.status_label.setText("Hazır")
        except Exception as e:
            error_message = f"Hata: {str(e)}"
            print(error_message)
            self.status_label.setText(error_message)
            self.response_area.append(error_message + "\n\n")
        finally:
            self.speak_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    async def transcribe_audio(self, audio_data):
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

        os.remove(file_name)
        return user_input

    async def get_gpt4_response(self, user_input):
        system_message = {
            "role": "system",
            "content": "Sen bir insanla sohbet eden bir AI asistanısın. Kısa, öz ve doğal cevaplar ver. Günlük konuşma dilini kullan, akademik veya resmi bir ton kullanma. Cevapların genellikle 1-3 cümle arasında olsun. İnsanlar gibi bazen küçük hatalar yapabilir veya tereddüt edebilirsin."
        }

        messages = [system_message] + conversation_history[-10:]  # Son 10 mesajı kullan

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
        return response_data['choices'][0]['message']['content']

    def capture_screen(self):
        screenshot = ImageGrab.grab()
        return screenshot

    def image_to_base64(self, image):
        image = image.convert("RGB")
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return img_str

    async def analyze_screenshot(self, query, image_base64):
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

    async def decide_action(self, query):
        prompt = f"""
        Aşağıdaki kullanıcı sorgusunu analiz edin ve hangi eylemi gerçekleştirmemiz gerektiğine karar verin:
        1. Ekran görüntüsü analizi
        2. Web araması
        3. Normal GPT-4 yanıtı
        Sadece '1', '2' veya '3' olarak cevaplayın.
        Kullanıcı Sorgusu: "{query}"
        Eğer sorgu ekrandaki bir şeyle ilgiliyse veya görsel analiz gerektiriyorsa 1'i seçin.
        Eğer sorgu açıkça bir web araması istiyorsa veya güncel bilgi gerektiriyorsa (örneğin, 'webde ara', 'internette bul', 'hava durumu', 'haberler' gibi ifadeler içeriyorsa) 2'yi seçin.
        Diğer tüm durumlar için 3'ü seçin.
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
        decision = response_data["choices"][0]["message"]["content"].strip()
        return decision
    
    async def perform_web_search(self, query):
        print(f"Performing web search for query: {query}")
        conn = http.client.HTTPSConnection("google.serper.dev")
        payload = json.dumps({
            "q": query,
            "gl": "tr",
            "hl": "tr"
        })
        headers = {
            'X-API-KEY': SERPER_API_KEY,
            'Content-Type': 'application/json'
        }
        try:
            print(f"Sending request to Serper API with payload: {payload}")
            conn.request("POST", "/search", payload, headers)
            res = conn.getresponse()
            print(f"Received response from Serper API with status: {res.status}")
            data = res.read()
        
            print(f"Raw API response: {data}")
            
            if not data:
                print("Empty response from Serper API")
                return "Arama sonuçları alınamadı."
            
            search_results = json.loads(data.decode("utf-8"))
            
            print("Decoded search results:", search_results)
            
            if not search_results:
                return "Arama sonuçları bulunamadı."
            
            response_text = await self.process_search_results_with_gpt4(query, search_results)
            return response_text
        except Exception as e:
            print(f"Error in perform_web_search: {str(e)}")
            return f"Web araması sırasında bir hata oluştu: {str(e)}"

    async def process_search_results_with_gpt4(self, query, search_results):
        print("Processing search results with GPT-4")
        if not search_results:
            return "Arama sonuçları işlenemedi."
        
        prompt = f"""
        Kullanıcının sorgusu: {query}
        Web araması sonuçları: {json.dumps(search_results, ensure_ascii=False)}

        Kullanıcıya en alakalı ve bilgilendirici yanıtı sağlamak için bu arama sonuçlarını kullanın.
        """

        try:
            async with httpx.AsyncClient(timeout=None) as client:
                headers = {
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                }
                data = {
                    "model": "gpt-4o",
                    "messages": [{"role": "user", "content": prompt}],
                }
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions", headers=headers, json=data
                )
                response.raise_for_status()
                response_data = response.json()

            return response_data['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error in process_search_results_with_gpt4: {str(e)}")
            return f"Arama sonuçları işlenirken bir hata oluştu: {str(e)}"

    async def print_gpt4_response(self, response_text):
        print("GPT-4 Yanıtı:", response_text)

    async def text_to_speech(self, text):
        async with httpx.AsyncClient(timeout=None) as client:
            headers = {
                "xi-api-key": ELEVENLABS_API_KEY,
                "Content-Type": "application/json",
            }
            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
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

        with io.BytesIO(audio_data) as f:
            audio_array, samplerate = sf.read(f)

        return audio_array, samplerate

    def closeEvent(self, event):
        self.save_conversation_history()
        event.accept()

async def main():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    # Hata ayıklama modunu etkinleştir
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger("httpx").setLevel(logging.DEBUG)

    window = AIAssistant()
    window.show()

    with loop:
        await loop.run_forever()

if __name__ == '__main__':
    asyncio.run(main())