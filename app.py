import streamlit as st
import google.generativeai as genai
import PyPDF2
import io

# Konfigurasi halaman
st.set_page_config(page_title="Miftah X-Generator", page_icon="🐦")

st.title("🐦 X Content Generator")
st.write("Ubah data PDF menjadi postingan X dengan gaya tokoh favoritmu.")

# Ambil API Key dari "Secrets" (Langkah 4 nanti)
# Ini cara paling aman agar API Key tidak dicuri orang lain
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    return "".join([page.extract_text() for page in reader.pages if page.extract_text()])

persona = st.text_input("Gaya Karakter (Contoh: Ferry Irwandi)")
uploaded_file = st.file_uploader("Upload PDF Proyek", type="pdf")

if st.button("Generate Postingan ✨"):
    if persona and uploaded_file:
        with st.spinner("Sedang memproses..."):
            text = extract_text(uploaded_file)
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Gaya: {persona}. Data: {text[:8000]}. Buat 3 opsi postingan X: 1 tweet 280 char, thread 3 tweet, dan long post 700 char."
            
            response = model.generate_content(prompt)
            st.markdown(response.text)
    else:
        st.error("Mohon isi gaya dan upload file.")
