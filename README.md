# AI Assistant: Your Personal GPT-4 Powered Companion

![AI Assistant Logo]()

Welcome to AI Assistant, a cutting-edge application that brings the power of GPT-4 to your fingertips. This intelligent assistant can understand speech, analyze images, and engage in natural conversations, all while providing responses in a lifelike voice.

## 🌟 Features

- **Multi-Modal Interaction**: Communicate via text, voice, or even screen captures!
- **Voice-Powered**: Utilizes OpenAI's Whisper for accurate speech-to-text conversion.
- **Lifelike Responses**: ElevenLabs API transforms text responses into natural-sounding speech.
- **Visual Understanding**: Analyze screenshots and images with GPT-4's advanced vision capabilities.
- **Web Search Integration**: Get up-to-date information on any topic.
- **I
## 🚀 Quick Start

### Prerequisites

- Python 3.8 or newer

### Installation and Setup

1. Clone or download this repository to your computer.
2. Open Terminal and navigate to the downloaded folder.
3. Run the following command:

   
   chmod +x setup.sh && ./setup.sh

The application will start automatically once the installation is complete.

Note: This application requires Python 3.8 or a newer version.
Alternative Manual Setup
If you prefer to set up the environment manually:

Clone this repository:
bash
Copygit clone https://github.com/Baro007/customgpt
cd ai-assistant

Set up a virtual environment (recommended):
bashCopypython3 -m venv myenv
source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`

Install the required packages:
bashCopypip install openai elevenlabs httpx sounddevice soundfile numpy pillow python-dotenv PyQt5 qasync

Create a .env file in the project root and add your API keys:
CopyOPENAI_API_KEY=your_openai_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
VOICE_ID=your_elevenlabs_voice_id
SERPER_API_KEY=your_serper_api_key

Run the application:
bashCopypython customgpt.py


🖥 Usage

Click the "Speak" button to start recording your voice input.
Click "Stop" when you're done speaking.
Wait for the AI to process your input and listen to its response.
For text input or screenshot analysis, use the appropriate buttons in the UI.

🛠 Key Components

AudioRecorder: Handles voice input recording.
AIAssistant: Main class that orchestrates all functionalities.
text_to_speech: Converts text responses to speech using ElevenLabs API.
perform_web_search: Integrates web search capabilities.
analyze_screenshot: Processes and analyzes screen captures.

🧠 How It Works

User input (voice/text/image) is captured and processed.
The input is sent to GPT-4 for analysis and response generation.
If needed, web searches or image analysis are performed.
The AI's response is converted to speech and played back to the user.

📈 Future Enhancements

Implement conversation memory for more contextual interactions.
Add support for multiple languages.
Integrate more AI models for specialized tasks.
Develop a mobile application version.

🤝 Contributing
We welcome contributions! Please feel free to submit a Pull Request.
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgements

OpenAI for GPT-4 and Whisper
ElevenLabs for their realistic text-to-speech API
The PyQt5 team for the excellent GUI framework


Created with ❤️ by Mektep.ai