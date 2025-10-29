import gradio as gr
import requests
import os

# -------------------------------
# BACKEND CONFIG
# -------------------------------
BACKEND_URL = "http://127.0.0.1:8000"
conversation_history = ""
user_details = {}

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------
def check_backend_connection():
    """Check if FastAPI backend is live before continuing."""
    try:
        res = requests.get(f"{BACKEND_URL}/")
        return res.status_code == 200
    except:
        return False


def submit_user_info(name, email, university, topic):
    """Store user details from scholar."""
    global user_details
    if not name or not email or not university or not topic:
        return "⚠️ Please fill all details before continuing."
    user_details = {
        "name": name,
        "email": email,
        "university": university,
        "topic": topic,
    }
    return f"✅ Welcome {name} from {university}! You may now start your voice chat with TinyLlama."


def chat_with_voice(audio):
    """Convert speech → text → TinyLlama → response speech."""
    global conversation_history

    import speech_recognition as sr
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        audio_data = recognizer.record(source)
        try:
            user_text = recognizer.recognize_google(audio_data)
        except:
            return "⚠️ Could not understand audio.", None

    # Send query to backend
    payload = {"user_input": user_text}
    try:
        res = requests.post(f"{BACKEND_URL}/query", json=payload)
        if res.status_code != 200:
            return f"⚠️ Backend error: {res.text}", None
        ai_reply = res.json().get("response", "")
    except Exception as e:
        return f"❌ Backend connection error: {e}", None

    # Append to chat history
    conversation_history += f"You: {user_text}\nTinyLlama: {ai_reply}\n\n"

    # Convert reply to audio
    try:
        from gtts import gTTS
        tts = gTTS(text=ai_reply, lang="en")
        tts.save("response.mp3")
    except Exception as e:
        return f"Error generating audio: {e}", None

    return ai_reply, "response.mp3"


def download_pdf():
    """Send chat history + scholar details to backend for PDF creation."""
    global conversation_history, user_details
    if not check_backend_connection():
        return "❌ Backend not reachable. Please start FastAPI first."
    if not conversation_history:
        return "⚠️ No chat history available."
    data = {"conversation": conversation_history, "user": user_details}
    try:
        res = requests.post(f"{BACKEND_URL}/download-pdf", json=data)
        msg = res.json().get("message", "")
        return msg
    except Exception as e:
        return f"❌ PDF generation failed: {e}"


# -------------------------------
# GRADIO INTERFACE
# -------------------------------
with gr.Blocks(theme="soft") as demo:
    gr.Markdown("## 🎓 TinyLlama Voice Chat")
    gr.Markdown("Fill in your details and start an intelligent voice conversation with TinyLlama!")

    # Scholar Details
    with gr.Tab("👩‍🎓 Scholar Details"):
        name = gr.Textbox(label="Full Name")
        email = gr.Textbox(label="Email")
        university = gr.Textbox(label="University / Institution")
        topic = gr.Textbox(label="Specialization")
        submit_btn = gr.Button("Submit Details")
        submit_status = gr.Textbox(label="Status")
        submit_btn.click(
            submit_user_info,
            inputs=[name, email, university, topic],
            outputs=[submit_status],
        )

    # Voice Chat
    with gr.Tab("🎙️ Voice Chat"):
        with gr.Row():
            audio_in = gr.Audio(sources=["microphone"], type="filepath", label="Speak your question")
            text_out = gr.Textbox(label="🧠 TinyLlama's Reply")
            audio_out = gr.Audio(label="🔊 AI Voice Reply")

        send_btn = gr.Button("Ask")
        send_btn.click(chat_with_voice, inputs=[audio_in], outputs=[text_out, audio_out])

    # Download PDF
    with gr.Tab("📘 Download Chat Record"):
        pdf_btn = gr.Button("Download Chat PDF")
        pdf_status = gr.Textbox(label="PDF Status")
        pdf_btn.click(download_pdf, outputs=[pdf_status])


# Launch App
demo.launch(server_name="127.0.0.1", server_port=7860)
