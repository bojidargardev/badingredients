import streamlit as st
from PIL import Image
import numpy as np
import easyocr

st.set_page_config(page_title="OCR Ingredients Checker")

@st.cache_resource
def load_reader():
    return easyocr.Reader(['bg', 'en'])

reader = load_reader()

BAD_INGREDIENTS_BG = [
    "аспартам": "изкуствен подсладител",
    "сукралоза": "изкуствен подсладител",
    "ацесулфам калий": "изкуствен подсладител",
    "натриев бензоат": "консервант",
    "сорбинова киселина": "консервант",
    "кофеин": "стимулант",
    "таурин": "енергийна добавка",
    "палмово масло": "спорна мазнина",
    "мононатриев глутамат": "подобрител на вкуса"
]

st.title("🧪 Проверка на съставки")

uploaded_file = st.file_uploader("Качи снимка", type=["png", "jpg", "jpeg"])

if uploaded_file:
    try:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Качено изображение", use_column_width=True)

        st.write("### 🔍 Разпознаване на текст...")

        img_array = np.array(image)

        results = reader.readtext(img_array, detail=0)
        extracted_text = " ".join(results).lower()

        st.text_area("Разпознат текст", extracted_text, height=200)

        st.write("### ⚠️ Намерени съставки")

        found = [i for i in BAD_INGREDIENTS_BG if i in extracted_text]

        if found:
            for item in found:
                st.error(f"❌ {item}")
        else:
            st.success("✅ Няма открити проблемни съставки")

    except Exception as e:
        st.error(f"Грешка: {e}")
