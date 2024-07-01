# AI Assistant: Your Personal GPT-4 and Claude-Powered Companion

![AI Assistant Logo]()

Welcome to AI Assistant, a cutting-edge application that brings the power of GPT-4 and Claude 3.5 Sonnet to your fingertips. This intelligent assistant can understand speech, analyze images, and engage in natural conversations, all while providing responses in a lifelike voice.

## 🌟 Features

- **Multi-Modal Interaction**: Communicate via text, voice, or even screen captures!
- **Voice-Powered**: Utilizes OpenAI's Whisper for accurate speech-to-text conversion.
- **Lifelike Responses**: ElevenLabs API transforms text responses into natural-sounding speech.
- **Visual Understanding**: Analyze screenshots and images with GPT-4's advanced vision capabilities.
- **Web Search Integration**: Get up-to-date information on any topic.
- **Dual AI Models**: Switch between GPT-4 and Claude 3.5 Sonnet for diverse AI experiences.
- **Intuitive GUI**: User-friendly interface built with PyQt5.

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or newer
- API Keys:
  - OpenAI API Key
  - ElevenLabs API Key
  - Serper API Key
  - Anthropic API Key (for Claude)

### API Requirements

This project relies on several external APIs to function properly. You'll need to obtain API keys from the following services:

1. **OpenAI API**: 
   - Used for GPT-4 and Whisper models
   - Sign up at [OpenAI](https://openai.com/api/)
   - Pricing: Pay-as-you-go model

2. **ElevenLabs API**:
   - Used for text-to-speech conversion
   - Sign up at [ElevenLabs](https://elevenlabs.io/)
   - Pricing: Free tier available, paid plans for more usage

3. **Serper API**:
   - Used for web search functionality
   - Sign up at [Serper](https://serper.dev/)
   - Pricing: Free tier available, paid plans for more usage

4. **Anthropic API**:
   - Used for Claude 3.5 Sonnet model
   - Sign up at [Anthropic](https://www.anthropic.com/)
   - Pricing: Pay-as-you-go model

Once you have obtained these API keys, you'll need to add them to your `.env` file. See the Installation and Setup section for more details.

### Installation and Setup

1. Clone or download this repository to your computer.
2. Open Terminal and navigate to the downloaded folder.
3. Run the following command:

   ```bash
   chmod +x setup.sh && ./setup.sh

When prompted, enter your API keys for OpenAI, ElevenLabs, Serper, and Anthropic.
The application will start automatically once the installation is complete.

Note: This application requires Python 3.8 or a newer version.
🖥 Usage

Launch the application.
Use the dropdown menu to select between GPT-4 and Claude 3.5 Sonnet.
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
get_ai_response: Manages responses from both GPT-4 and Claude models.

🧠 How It Works

User input (voice/text/image) is captured and processed.
The input is sent to the selected AI model (GPT-4 or Claude) for analysis and response generation.
If needed, web searches or image analysis are performed.
The AI's response is converted to speech and played back to the user.

📈 Future Enhancements

Implement conversation memory for more contextual interactions.
Add support for multiple languages.
Integrate more AI models for specialized tasks.
Develop a mobile application version.
Enhance the GUI for better user experience.
Implement real-time model switching without restarting the application.

🤝 Contributing
We welcome contributions! Please feel free to submit a Pull Request.
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgements

OpenAI for GPT-4 and Whisper
Anthropic for Claude 3.5 Sonnet
ElevenLabs for their realistic text-to-speech API
The PyQt5 team for the excellent GUI framework
Serper for Web Search

Created with ❤️ by Mektep.ai