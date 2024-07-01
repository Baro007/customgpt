AI Assistant: Your Personal GPT-4 and Claude-Powered Companion



Welcome to AI Assistant, a cutting-edge application that harnesses the power of GPT-4 and Claude 3.5 Sonnet to provide an intelligent, multi-modal interaction experience. This sophisticated assistant understands speech, analyzes images, engages in natural conversations, and delivers responses in a lifelike voice.

## 🌟 Features

- **Dual AI Models**: Choose between GPT-4 and Claude 3.5 Sonnet for varied AI experiences
- **Multi-Modal Interaction**: Communicate via text, voice, or even screen captures
- **Voice-Powered**: Utilizes OpenAI's Whisper for accurate speech-to-text conversion
- **Lifelike Responses**: ElevenLabs API transforms text responses into natural-sounding speech
- **Visual Understanding**: Analyze screenshots and images with advanced vision capabilities
- **Web Search Integration**: Access up-to-date information on any topic
- **Intuitive GUI**: User-friendly interface built with PyQt5

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or newer
- API Keys:
  - OpenAI API Key
  - ElevenLabs API Key
  - Serper API Key
  - Anthropic API Key (for Claude)

### API Requirements

This project relies on several external APIs:

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
   - Pricing: Check Anthropic's website for current pricing

### Installation and Setup

1. Clone or download this repository:


2. Run the setup script:
   ```bash

   chmod +x setup.sh && ./setup.sh

   ```

3. When prompted, enter your API keys for OpenAI, ElevenLabs, Serper, and Anthropic. (LOOK .envexample)

4. The application will start automatically once the installation is complete.

Note: This application requires Python 3.8 or a newer version.

## 🖥 Usage

1. Launch the application.
2. Choose your preferred AI model (GPT-4 or Claude 3.5 Sonnet) from the dropdown menu.
3. For voice input:
   - Click the "Speak" button to start recording.
   - Click "Stop" when you're done speaking.
4. For text input:
   - Type your message in the text box and click "Send".
5. For screenshot analysis:
   - Capture a screenshot and the AI will analyze it.
6. Toggle the "Mute" button to enable/disable voice responses.
7. Wait for the AI to process your input and listen to or read its response.

## 🛠 Key Components

- **AudioRecorder**: Handles voice input recording.
- **AIAssistant**: Main class orchestrating all functionalities.
- **text_to_speech**: Converts text responses to speech using ElevenLabs API.
- **perform_web_search**: Integrates web search capabilities.
- **analyze_screenshot**: Processes and analyzes screen captures.
- **get_ai_response**: Manages interactions with GPT-4 and Claude models.

## 🧠 How It Works

1. User input (voice/text/image) is captured and processed.
2. The input is sent to the selected AI model (GPT-4 or Claude) for analysis and response generation.
3. If needed, web searches or image analysis are performed.
4. The AI's response is converted to speech (if not muted) and played back to the user.

## 📈 Future Enhancements

- Implement conversation memory for more contextual interactions.
- Add support for multiple languages.
- Integrate more AI models for specialized tasks.
- Develop a mobile application version.
- Enhance the GUI for a more polished user experience.

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- OpenAI for GPT-4 and Whisper
- Anthropic for Claude 3.5 Sonnet
- ElevenLabs for their realistic text-to-speech API
- The PyQt5 team for the excellent GUI framework
- Serper for Web Search capabilities

Created with ❤️ by Mektep.ai
```
