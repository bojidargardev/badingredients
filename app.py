import streamlit as st
from PIL import Image
import requests

API_KEY = "helloworld"  # free demo key (limited)

BAD_INGREDIENTS_BG = [
    "аспартам",
    "сукралоза",
    "ацесулфам",
    "натриев бензоат",
    "сорбинова киселина",
    "кофеин",
    "таурин",
    "палмово масло",
    "мононатриев глутамат",
]

st.title("🧪 Проверка на съставки (без инсталации)")

uploaded_file = st.file_uploader("Качи снимка", type=["png", "jpg", "jpeg"])

def extract_text_api(file):
    url = "https://api.ocr.space/parse/image"
    response = requests.post(
        url,
        files={"file": file},
        data={
            "apikey": API_KEY,
            "language": "bul",
        },
    )
    result = response.json()

    try:
        return result["ParsedResults"][0]["ParsedText"]
    except:
        return ""

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Качено изображение", use_column_width=True)

    st.write("### 🔍 Разпознаване на текст...")

    text = extract_text_api(uploaded_file).lower()

    st.text_area("Разпознат текст", text, height=200)

    st.write("### ⚠️ Намерени съставки")

    found = [i for i in BAD_INGREDIENTS_BG if i in text]

    if found:
        for item in found:
            st.error(f"❌ {item}")
    else:
        st.success("✅ Няма открити проблемни съставки")
