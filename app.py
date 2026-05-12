import streamlit as st
import requests
from PIL import Image

API_KEY = "helloworld"

# Dictionary of problematic ingredients
BAD_INGREDIENTS_BG = {
    "E407": "Карагенан (възпаления, храносмилателни проблеми)",
    "E621": "Натриев глутамат (главоболие, алергии)",
    "E262": "Натриев ацетат (дразни стомаха)",
    "E300": "Аскорбинова киселина (в големи дози дразни стомаха)",
    "E330": "Лимонена киселина (уврежда зъбния емайл)",
    "E250": "Натриев нитрит (риск от онкологични заболявания)",
    "E952": "Цикламат подсладител",
    "E471": "Емулгатор",
    "E472": "Емулгатор",
}

st.title("OCR Ingredient Checker")

uploaded_file = st.file_uploader(
    "Upload image",
    type=["png", "jpg", "jpeg"]
)

def extract_text(file):
    url = "https://api.ocr.space/parse/image"

    try:
        response = requests.post(
            url,
            files={"file": file},
            data={
                "apikey": API_KEY,
                "language": "bul"
            }
        )

        result = response.json()

        if result.get("IsErroredOnProcessing"):
            return ""

        return result["ParsedResults"][0]["ParsedText"]

    except Exception as e:
        st.error(f"OCR Error: {e}")
        return ""

if uploaded_file:
    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Image", use_container_width=True)

    text = extract_text(uploaded_file)

    # normalize text
    normalized_text = text.upper().replace("Е", "E")

    st.text_area("Extracted text", text, height=200)

    found = []

    for code, description in BAD_INGREDIENTS_BG.items():
        if code in normalized_text:
            found.append((code, description))

    if found:
        st.subheader("Detected ingredients")

        for code, description in found:
            st.write(f"❌ {code} — {description}")

    else:
        st.success("✅ No problematic ingredients found")
