from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client as TwilioClient
from dotenv import load_dotenv
from openai import OpenAI
from gtts import gTTS
import os
import base64
import requests

# Load .env variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

# Init services
app = Flask(__name__)
openai_client = OpenAI(api_key=OPENAI_API_KEY)
twilio_client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Store latest image per user (phone number)
user_last_image = {}

# 🧠 GPT Prompt Template
def build_prompt(lang):
    if lang == "English":
        return """Identify the pest in this image. Respond in English in the following format:
Bug identified: "..."
Risk factor: "..." (e.g. Moderate / Critical / Low)
Natural remedy: "..." (organic solution only)"""
    
    elif lang == "Hindi":
        return """इस चित्र में कीट की पहचान करें। जवाब हिंदी में इस प्रारूप में दें:
कीट की पहचान: "..."
जोखिम स्तर: "..."
प्राकृतिक उपचार: "..." (केवल जैविक समाधान)"""
    
    elif lang == "Telugu":
        return """ఈ చిత్రంలో పురుగును గుర్తించండి. సమాధానం తెలుగులో ఈ ఫార్మాట్‌లో ఇవ్వండి:
పురుగు గుర్తింపు: "..."
ఆపద స్థాయి: "..."
ప్రाकृतिक పరిష్కారం: "..." (సేంద్రీయ పరిష్కారం మాత్రమే)"""

# 🖼️ Download image from Twilio → save → return path
def download_image(media_url, phone):
    try:
        res = requests.get(media_url, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
        if res.status_code == 200:
            path = f"static/{phone}.jpg"
            with open(path, "wb") as f:
                f.write(res.content)
            return path
        else:
            raise Exception("Twilio image download failed")
    except Exception as e:
        raise Exception(f"Image error: {e}")

# 🧠 Send image to GPT-4 Vision
def ask_gpt(image_path, lang):
    with open(image_path, "rb") as f:
        base64_img = base64.b64encode(f.read()).decode('utf-8')

    prompt = build_prompt(lang)

    response = openai_client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                ]
            }
        ]
    )
    return response.choices[0].message.content.strip()

# 🔊 Generate Telugu voice (only if needed)
def generate_telugu_audio(text):
    tts = gTTS(text=text, lang="te")
    audio_path = "static/telugu.mp3"
    tts.save(audio_path)
    return audio_path

# 🔊 Generate Hindi voice (only if needed)
def generate_telugu_audio(text):
    tts = gTTS(text=text, lang="hi")
    audio_path = "static/hindi.mp3"
    tts.save(audio_path)
    return audio_path


# 📩 WhatsApp webhook handler
@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    from_number = request.form.get("From")
    body = request.form.get("Body", "").strip()
    media_url = request.form.get("MediaUrl0")
    resp = MessagingResponse()

    print(f"📲 From: {from_number} | Text: {body} | Media: {media_url}")

    # Step 1: If image is sent
    if media_url:
        try:
            image_path = download_image(media_url, from_number)
            user_last_image[from_number] = image_path
            resp.message("✅ Image received! Now reply with a language: English, Hindi, or Telugu.")
        except Exception as e:
            resp.message(f"❌ Failed to process image: {e}")
        return str(resp)

    # Step 2: If user sent language preference
    if body.lower() in ["english", "hindi", "telugu"]:
        lang = body.capitalize()
        image_path = user_last_image.get(from_number)

        if not image_path:
            resp.message("⚠️ Please send an image of the pest first.")
            return str(resp)

        try:
            response_text = ask_gpt(image_path, lang)
            final_message = f"🌐 {lang}:\n" + response_text

            if lang == "Telugu":
                audio_path = generate_telugu_audio(response_text)
                audio_url = f"{request.host_url}static/telugu.mp3"
                final_message += f"\n🔊 Voice Note: {audio_url}"

            elif lang == "Hindi":
                audio_path = generate_telugu_audio(response_text)
                audio_url = f"{request.host_url}static/hindi.mp3"
                final_message += f"\n🔊 Voice Note: {audio_url}"

            resp.message(final_message)
        except Exception as e:
            resp.message(f"❌ Failed to analyze image: {e}")
        return str(resp)

    # Step 3: Fallback message
    resp.message("👋 Send a pest image first, then reply with 'English', 'Hindi', or 'Telugu'.")
    return str(resp)

# ✅ Run Flask server
if __name__ == "__main__":
    app.run(debug=True)
