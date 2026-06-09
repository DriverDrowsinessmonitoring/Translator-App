import streamlit as st
from googletrans import Translator
from gtts import gTTS
from PIL import Image
import pytesseract

# Translator
translator = Translator()

# Page Config
st.set_page_config(
    page_title="Advanced AI Translator",
    page_icon="🌍",
    layout="centered"
)



theme = st.sidebar.selectbox(
    "🌗 Choose Theme",
    ["Dark", "Light"]
)

if theme == "Dark":
    background = "#0E1117"
    text_color = "white"
    box_color = "#262730"

else:
    background = "#FFFFFF"
    text_color = "black"
    box_color = "#F0F2F6"



st.markdown(f"""
<style>

.stApp {{
    background-color: {background};
    color: {text_color};
}}

html, body, [class*="css"] {{
    color: {text_color};
}}

textarea {{
    background-color: {box_color} !important;
    color: {text_color} !important;
}}

.stTextArea textarea {{
    background-color: {box_color};
    color: {text_color};
    border-radius: 10px;
}}

.stSelectbox div {{
    background-color: {box_color};
    color: {text_color};
}}

.stButton > button {{
    background-color: #00C897;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 18px;
}}

</style>
""", unsafe_allow_html=True)



st.title("🌍 Advanced AI Translator")

st.write("Translate text into multiple languages instantly")



if "history" not in st.session_state:
    st.session_state.history = []



languages = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja",
    "Chinese": "zh-cn",
    "Korean": "ko",
    "Arabic": "ar",
    "Russian": "ru",
    "Italian": "it",
    "Portuguese": "pt",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Urdu": "ur"
}



text = st.text_area("✍ Enter Text")



uploaded_image = st.file_uploader(
    "📸 Upload Image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_image:

    image = Image.open(uploaded_image)

    st.image(image, caption="Uploaded Image")

    # Tesseract Path
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

    extracted_text = pytesseract.image_to_string(image)

    st.success("📄 Extracted Text")

    st.write(extracted_text)

    text = extracted_text



if text.strip() != "":

    try:
        detected = translator.detect(text)

        st.info(f"🌐 Detected Language: {detected.lang}")

    except:
        st.warning("Language detection failed")



choice = st.selectbox(
    "🌍 Choose Language",
    languages.keys()
)



if st.button("🚀 Translate"):

    if text.strip() != "":

        translated = translator.translate(
            text,
            dest=languages[choice]
        )

        st.success("✅ Translated Text")

        st.write(translated.text)

        # Translation History
        st.session_state.history.append(translated.text)

        # Copy Box
        st.code(translated.text)

        # Voice Output
        try:

            tts = gTTS(
                translated.text,
                lang=languages[choice]
            )

            tts.save("voice.mp3")

            audio_file = open("voice.mp3", "rb")

            audio_bytes = audio_file.read()

            st.audio(audio_bytes)

        except:
            st.warning("Voice output not supported for this language")

        # Download Button
        st.download_button(
            "⬇ Download Translation",
            translated.text,
            file_name="translation.txt"
        )

    else:
        st.warning("⚠ Please enter some text")



st.sidebar.title("📜 Translation History")

for item in st.session_state.history:
    st.sidebar.write(item)