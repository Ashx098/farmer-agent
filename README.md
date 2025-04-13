# 🌾 WhatsApp AI Pest Assistant 🤖🐛

An AI-powered WhatsApp chatbot that helps farmers identify pests from crop photos and provides organic solutions in their preferred language (Hindi, Telugu, or English). This tool is designed to be low-tech friendly, supporting regional voice responses for accessibility.

## 🔍 Features
- 📸 Send pest image via WhatsApp
- 🌐 Choose language: Hindi / Telugu / English
- 🧠 AI detects pest and suggests remedies
- 🔊 Voice message replies for low-literacy users (gTTS)
- 🪴 Organic + Chemical remedy suggestions
- 🛠️ Powered by GPT-4 Vision, Twilio, Flask, gTTS

## 🛠️ Tech Stack
- Python + Flask
- Twilio WhatsApp API
- OpenAI GPT-4 Vision
- gTTS (Google Text-to-Speech)
- Ngrok (for local testing)

## 📦 Project Structure
```
├── app.py               # Main Flask server
├── static/              # Stores audio (voice note) files
├── .env                 # API keys (not uploaded)
├── .gitignore
├── requirements.txt
└── README.md
```

## 🚀 How It Works
1. User sends a pest image on WhatsApp.
2. AI (GPT-4 Vision) identifies the pest and suggests remedies in English, Hindi, or Telugu.
3. A voice note (in selected language) is generated and sent as a reply.
4. Farmer receives:
   - 📄 Text summary
   - 🔊 Voice response (for Hindi/Telugu)

## 💬 Example
**User:** (sends pest image) + `Telugu`  
**Bot:**  
```
పురుగు: మీలీబగ్  
ఆపద స్థాయి: మధ్యస్థ  
పరిష్కారం: వేప నూనెను నీటితో కలిపి పూతపెట్టండి  
🔊 Voice Note Link
```

## 🧠 Motivation
Millions of farmers in India face pest-related crop damage. Most don’t speak English or use smartphones actively. This AI agent bridges that gap using WhatsApp + multilingual voice.

## 📜 License
This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.

## 🙌 Contributing
PRs welcome. Let’s improve accessibility for every farmer. 🇮🇳

## ✨ Creator
Built by [Avinash Mynampati](https://aviinashh-ai.vercel.app)
