AI Voice Assistant
This project is an advanced AI voice assistant that combines the power of OpenAI's GPT-4 for natural language processing, Whisper for speech recognition, and ElevenLabs for text-to-speech synthesis. It offers a seamless, conversational interface for users to interact with AI, complete with screen analysis capabilities and customizable voice output.
Features

Speech Recognition: Utilizes OpenAI's Whisper model for accurate speech-to-text conversion.
Natural Language Processing: Leverages GPT-4 for intelligent, context-aware responses.
Text-to-Speech: Employs ElevenLabs for high-quality, natural-sounding voice synthesis.
Screen Analysis: Capability to analyze screen content when prompted.
Real-time Conversation: Enables fluid, back-and-forth dialogue with the AI.
Customizable Voice: Options to adjust voice settings for personalized interaction.

Prerequisites

Python 3.8+
OpenAI API key
ElevenLabs API key
Required Python packages (see requirements.txt)

Installation

Clone the repository:
Copygit clone https://github.com/yourusername/ai-voice-assistant.git
cd ai-voice-assistant

Create and activate a virtual environment:
Copypython -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install required packages:
Copypip install -r requirements.txt

Set up environment variables:
Create a .env file in the project root and add your API keys:
CopyOPENAI_API_KEY=your_openai_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
VOICE_ID=your_chosen_elevenlabs_voice_id


Usage
Run the main script to start the voice assistant:
Copypython main.py

Press the designated key (e.g., Space) to start recording your voice input.
Speak your query or command.
Release the key to stop recording and process your input.
The AI will respond both textually and verbally.

Configuration

Adjust voice settings in the text_to_speech function.
Modify GPT-4 parameters in the get_gpt4_response function.
Customize screen analysis behavior in the analyze_screenshot function.

Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
License
This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

OpenAI for GPT-4 and Whisper models
ElevenLabs for text-to-speech technology
All contributors and supporters of this projec
