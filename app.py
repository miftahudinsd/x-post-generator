import streamlit as st
import google.generativeai as genai
import PyPDF2
import io

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Miftah X-Generator", page_icon="🐦")

st.title("🐦 X Content Generator by Miftah")
st.write("Aplikasi ini akan membantu kamu dalam membuat konten X sesuai dengan karakter atau role model kamu. Hasilnya terdiri dari 3 opsi yaitu : 1 single tweet, 3 tweet thread dan 1 tweet long post atau panjang.")

# 2. Setup API Key secara Aman
try:
    # Mengambil dari Advanced Settings > Secrets di Streamlit Cloud
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("API Key tidak ditemukan. Pastikan sudah diatur di 'Secrets' Streamlit.")
    st.stop()

# 3. Fungsi Diagnostik (Diambil dari logika Colab Anda)
def get_best_model():
    """Mencari model yang aktif secara otomatis"""
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Urutan prioritas model
        for target in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-1.0-pro']:
            if target in available_models:
                return target
        return available_models[0] if available_models else None
    except:
        return 'models/gemini-1.5-flash' # Default jika list gagal

def extract_pdf_text(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    return "".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])

# 4. Antarmuka Streamlit (Pengganti input() dan files.upload())
persona = st.text_input("Gaya Karakter", placeholder="Contoh: Ferry Irwandi")
uploaded_file = st.file_uploader("Upload PDF Proyek", type="pdf")

if st.button("Generate Postingan ✨"):
    if persona and uploaded_file:
        with st.spinner("Mendiagnosa model dan memproses konten..."):
            # Ekstrak Teks
            raw_text = extract_pdf_text(uploaded_file)
            
            # Deteksi Model Aktif (Logika Colab Anda)
            working_model = get_best_model()
            st.caption(f"Sistem menggunakan model: {working_model}")
            
            model = genai.GenerativeModel(working_model)
            prompt = f"""
            Bertindaklah sebagai {persona}. 
            Gunakan data ini: {raw_text[:8000]}
            
            Buat 3 opsi postingan X:
            1. 1 Tweet (280 char)
            2. Thread 3 Tweet
            3. Long Post (700 char)
            """
            
            try:
                response = model.generate_content(prompt)
                st.divider()
                st.subheader("HASIL POSTINGAN ANDA:")
                st.markdown(response.text)
                st.balloons()
            except Exception as e:
                st.error(f"Gagal generate: {e}")
    else:
        st.warning("Mohon isi gaya dan upload file PDF.")
