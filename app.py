
import streamlit as st
import requests
from PIL import Image

API_KEY = "helloworld"

BAD_INGREDIENTS_BG = [
   "E407": "Карагенан (възпаления, храносмилателни проблеми)",
"Е621": "Натриев глутамат (главоболие, алергии)",
"Е262": "Натриев ацетат (дразни стомаха)",
"Е300": "Аскорбинова киселина (в големи дози дразни стомаха)",
"Е330": "Лимонена киселина (уврежда зъбния емайл)",
"Е250": "Натриев нитрит (риск от онкологични заболявания)",
"Е952": "Цикламат подсладител",
"Е471": "Емулгатор",
"Е472": "Емулгатор",
]

st.title("OCR Ingredient Checker")

uploaded_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

def extract_text(file):
    url = "https://api.ocr.space/parse/image"
    r = requests.post(
        url,
        files={"file": file},
        data={"apikey": API_KEY, "language": "bul"}
    )
    result = r.json()
    try:
        return result["ParsedResults"][0]["ParsedText"]
    except:
        return ""

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image)

    text = extract_text(uploaded_file).lower()

    st.text_area("Extracted text", text)

    found = [i for i in BAD_INGREDIENTS_BG if i in text]

    if found:
        for i in found:
            st.write(f"❌ {i}")
    else:
        st.write("✅ Nothing found")
