from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ------------------------------
# CONFIGURATION
# ------------------------------
app = FastAPI(title="TinyLlama Voice Chat API (No CSV)")

# Allow frontend (Gradio) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"  # LM Studio TinyLlama endpoint
MODEL_NAME = "tinyllama-1.1b-chat-v1.0"


# ------------------------------
# MODELS
# ------------------------------
class QueryRequest(BaseModel):
    user_input: str


class PdfRequest(BaseModel):
    conversation: str
    user: dict


# ------------------------------
# ROUTES
# ------------------------------

@app.get("/")
def root():
    """Root endpoint for connection check."""
    return {"message": "🚀 TinyLlama Voice Chat API is running!"}


@app.post("/query")
async def query_tinyllama(req: QueryRequest):
    """Send user query to TinyLlama running in LM Studio."""
    user_input = req.user_input

    # Prepare prompt (without CSV context)
    prompt = f"""
    You are TinyLlama, a helpful AI research assistant for PhD scholars.
    Respond thoughtfully to the scholar’s question.

    Question:
    {user_input}
    """

    try:
        response = requests.post(
            LM_STUDIO_URL,
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": "You are a knowledgeable AI assistant for research guidance."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.7,
            },
            timeout=30,
        )

        result = response.json()
        if "choices" in result:
            ai_reply = result["choices"][0]["message"]["content"]
            return {"response": ai_reply}
        else:
            return {"response": f"⚠️ Unexpected LM Studio response: {result}"}

    except Exception as e:
        return {"response": f"❌ Could not connect to LM Studio: {e}"}


@app.post("/download-pdf")
async def download_pdf(req: PdfRequest):
    """Generate and save a PDF of the conversation and user details."""
    conversation = req.conversation
    user = req.user

    filename = f"{user.get('name', 'Scholar')}_TinyLlama_Chat.pdf"
    pdf_path = os.path.join(os.getcwd(), filename)

    try:
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        # Header
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 50, "TinyLlama Chat Report")

        c.setFont("Helvetica", 11)
        c.drawString(50, height - 80, f"Name: {user.get('name', '')}")
        c.drawString(50, height - 100, f"Email: {user.get('email', '')}")
        c.drawString(50, height - 120, f"University: {user.get('university', '')}")
        c.drawString(50, height - 140, f"Research Topic: {user.get('topic', '')}")
        c.line(50, height - 150, width - 50, height - 150)

        # Chat content
        y = height - 170
        c.setFont("Helvetica", 10)
        for line in conversation.split("\n"):
            if y < 60:  # Create new page if space runs out
                c.showPage()
                y = height - 60
                c.setFont("Helvetica", 10)
            c.drawString(50, y, line)
            y -= 14

        c.save()
        return {"message": f"✅ PDF saved as '{filename}' in project folder."}

    except Exception as e:
        return {"message": f"❌ PDF generation failed: {e}"}
