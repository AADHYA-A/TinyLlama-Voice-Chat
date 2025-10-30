🦙 TinyLlama Voice Chat System
🎙️ AI-Powered Real-Time Conversational Assistant
📘 Project Overview

The TinyLlama Voice Chat System is a lightweight, locally hosted conversational AI application that enables real-time voice-based interaction with an AI model.
It combines speech recognition, natural language processing (NLP), and text-to-speech (TTS) technologies to create a hands-free conversational experience.

The system uses the TinyLlama-1.1B Chat model hosted via LM Studio, integrated with a FastAPI backend and HTML/Gradio frontend for seamless interaction.
It can also generate PDF summaries of conversations for analysis or record-keeping.

🧠 Key Features

🎤 Voice Input: Converts user speech into text using the SpeechRecognition library.

💬 TinyLlama Model: Processes queries using TinyLlama-1.1B-Chat, a lightweight large language model hosted locally.

🔊 Voice Output: Converts AI-generated text responses back to voice using pyttsx3 or gTTS.

⚙️ FastAPI Backend: Handles model interaction, voice processing, and PDF report generation.

🌐 Frontend Interface: Built using Gradio or HTML/CSS/JavaScript for user-friendly interaction.

🧾 Conversation Summaries: Automatically generates downloadable PDF summaries of user–AI interactions.

🔒 Offline & Private: Runs locally without the need for cloud APIs or internet access.


🧩 How It Works

🎙️ User speaks into the microphone.

🧠 The system uses SpeechRecognition to convert voice → text.

🤖 Text is sent to TinyLlama-1.1B Chat model for natural language processing.

💬 The model generates a conversational response.

🔊 The response is converted back to speech for voice playback.

🧾 The conversation can be saved as a PDF summary using ReportLab.

💻 Tech Stack
Layer	Technology Used
Model	TinyLlama-1.1B Chat (LM Studio)
Backend	FastAPI
Frontend	HTML / CSS / JavaScript / Gradio
Voice Input	SpeechRecognition
Voice Output	pyttsx3 / gTTS
PDF Generation	ReportLab
Programming Language	Python

🚀 Applications

Voice-based AI assistants

Policy research and analysis

Educational tools for students

Accessibility for visually impaired users

Smart Q&A and information retrieval systems
