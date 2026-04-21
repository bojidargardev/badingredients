import streamlit as st
from PIL import Image
import pytesseract

BAD_INGREDIENTS = [
    "захар",
    "глюкозо-фруктозен сироп",
    "фруктозен сироп",
    "изкуствени подсладители",
    "аспартам",
    "сукралоза",
    "ацесулфам калий",
    "консерванти",
    "натриев бензоат",
    "сорбинова киселина",
    "изкуствени оцветители",
    "изкуствени аромати",
    "аромати",
    "кофеин",
    "таурин",
    "палмово масло",
    "хидрогенирани мазнини",
    "мононатриев глутамат",
    "емулгатори",
    "стабилизатори",
    "регулатори на киселинността",
    "лимонена киселина"
]

st.title("🧪 Ingredient Checker (OCR)")

st.write("Upload a product label image to detect harmful ingredients.")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.write("### 🔍 Extracting text...")

    extracted_text = pytesseract.image_to_string(image)

    st.text_area("Extracted Text", extracted_text, height=200)

    st.write("### ⚠️ Detected Problematic Ingredients")

    found = []

    text_lower = extracted_text.lower()

    for ingredient in BAD_INGREDIENTS:
        if ingredient in text_lower:
            found.append(ingredient)

    if found:
        for item in found:
            st.error(f"❌ {item}")
    else:
        st.success("✅ No flagged ingredients found!")
