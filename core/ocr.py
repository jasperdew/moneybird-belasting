import google.generativeai as genai
import json
from PIL import Image
import io
import os  # ← deze moet er zeker staan

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro-vision")

def extract_fields(file_bytes: bytes) -> dict:
    img = Image.open(io.BytesIO(file_bytes))
    rsp = model.generate_content(
        [img, "Geef alleen JSON met keys: bedrag, jaar, categorie, toelichting."])
    return json.loads(rsp.text)
