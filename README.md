# PyChat - Conversational AI Chatbot

A simple conversational AI chatbot built using Python and the Hugging Face Transformers library. This chatbot uses the BlenderBot model to generate human-like responses in a conversation.

## Features

- Interactive command-line chat interface
- Modern graphical user interface (GUI)
- Conversation history management
- Natural language processing using BlenderBot model
- Context-aware responses
- Real-time response generation
- User-friendly status indicators

## Requirements

- Python 3.8 or higher
- PyTorch
- Transformers library
- Tokenizers
- tkinter (included with Python)

## Installation

1. Create a virtual environment:
```bash
python -m venv env
```

2. Activate the virtual environment:
- Windows:
```bash
.\env\Scripts\activate
```
- Linux/Mac:
```bash
source env/bin/activate
```

3. Install the required packages:
```bash
pip install transformers torch
```

## Usage

### Command-line Version
1. Make sure your virtual environment is activated
2. Run the command-line chatbot:
```bash
python chatbot.py
```
3. Start chatting! Type your messages and press Enter
4. To exit, press Ctrl+C

### GUI Version
1. Make sure your virtual environment is activated
2. Run the GUI chatbot:
```bash
python gui_chatbot.py
```
3. The chat window will open
4. Type your message in the input field
5. Press Enter or click the Send button
6. To exit, close the window

## How it Works

The chatbot uses the BlenderBot model from Facebook, specifically the `facebook/blenderbot-400M-distill` version. It maintains a conversation history to provide context-aware responses. The model processes both the conversation history and your current input to generate appropriate responses.

### GUI Features
- Clean and modern interface
- Scrollable chat history
- Real-time status updates
- Non-blocking response generation (keeps UI responsive)
- Easy-to-use input field with Enter key support
- Clear message formatting for better readability

## Note

The first time you run the chatbot, it will download the model files (approximately 730MB). This may take a few minutes depending on your internet connection.

## License

This project is open source and available under the MIT License.
