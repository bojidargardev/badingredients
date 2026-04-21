import streamlit as st
from PIL import Image
import easyocr

# Bulgarian + English OCR
reader = easyocr.Reader(['bg', 'en'])

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

st.title("🧪 Проверка на съставки (OCR без инсталации)")

uploaded_file = st.file_uploader("Качи снимка", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Качено изображение", use_column_width=True)

    st.write("### 🔍 Разпознаване на текст...")

    results = reader.readtext(np.array(image))
    extracted_text = " ".join([res[1] for res in results]).lower()

    st.text_area("Разпознат текст", extracted_text, height=200)

    st.write("### ⚠️ Намерени съставки")

    found = [i for i in BAD_INGREDIENTS_BG if i in extracted_text]

    if found:
        for item in found:
            st.error(f"❌ {item}")
    else:
        st.success("✅ Няма открити проблемни съставки")
