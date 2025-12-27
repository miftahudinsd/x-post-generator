import streamlit as st
from google.genai import Client
import PyPDF2
import io

# Konfigurasi halaman agar terlihat profesional
st.set_page_config(page_title="Miftah X-Generator", page_icon="🐦")

st.title("🐦 X Content Generator")
st.write("Ubah data PDF menjadi postingan X dengan gaya tokoh favoritmu.")

# Mengambil API Key dari Secrets Streamlit
# Pastikan di Advanced Settings sudah diisi: GEMINI_API_KEY = "KODE_ANDA"
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = Client(api_key=api_key)
except Exception as e:
    st.error("API Key tidak ditemukan di Secrets. Pastikan sudah diatur di Streamlit Cloud.")
    st.stop()

def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text

# Input Antarmuka
persona = st.text_input("Gaya Karakter", placeholder="Contoh: Ferry Irwandi - Kritis & Edukatif")
uploaded_file = st.file_uploader("Upload PDF Proyek", type="pdf")

if st.button("Generate Postingan ✨"):
    if persona and uploaded_file:
        with st.spinner("AI sedang berpikir..."):
            raw_text = extract_text(uploaded_file)
            
            # Prompt Engineering khusus untuk gaya Ferry Irwandi & Crypto Yapping
            prompt = f"""
            Anda adalah pakar konten X dengan gaya: {persona}.
            Data proyek: {raw_text[:8000]}
            
            Buat 3 Opsi:
            1. OPSI 1: 1 Tweet (Maks 280 Karakter).
            2. OPSI 2: Thread 3 Tweet (Maks 280 Karakter per tweet).
            3. OPSI 3: Long Post (Maks 700 Karakter).
            
            Gunakan bahasa yang tajam dan berbasis data. Tampilkan jumlah karakter di akhir setiap opsi.
            """
            
            try:
                # Menggunakan jalur stable (non-beta) secara otomatis
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=prompt
                )
                st.divider()
                st.subheader("Hasil Generasi:")
                st.markdown(response.text)
                st.balloons()
            except Exception as e:
                st.error(f"Terjadi kendala teknis: {e}")
    else:
        st.warning("Mohon isi gaya karakter dan unggah file PDF.")
