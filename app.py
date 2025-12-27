import streamlit as st
import google.generativeai as genai
import PyPDF2
import io

# Konfigurasi Halaman
st.set_page_config(page_title="Miftah X-Generator", page_icon="🐦")

st.title("🐦 X Content Generator")
st.write("Ubah data PDF menjadi postingan X dengan gaya favoritmu.")

# Ambil API Key dari Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("API Key belum diatur di Secrets Streamlit Cloud.")
    st.stop()

def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text

# Antarmuka Pengguna
persona = st.text_input("Gaya Karakter", placeholder="Contoh: Ferry Irwandi")
uploaded_file = st.file_uploader("Upload PDF Proyek", type="pdf")

if st.button("Generate Postingan ✨"):
    if persona and uploaded_file:
        with st.spinner("Sedang memproses..."):
            raw_text = extract_text(uploaded_file)
            
            # MENGHINDARI ERROR 404: 
            # Kita panggil model secara eksplisit tanpa prefix v1beta
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"Bertindaklah sebagai {persona}. Gunakan data ini: {raw_text[:7000]}. Buat 3 opsi postingan X: 1 tweet singkat, 1 thread 3 tweet, dan 1 long post 700 karakter. Sertakan jumlah karakter."
            
            try:
                # Menggunakan safety_settings untuk memastikan respon lancar
                response = model.generate_content(prompt)
                
                st.divider()
                st.subheader("Hasil untuk Konten X Anda:")
                st.markdown(response.text)
                st.balloons()
            except Exception as e:
                st.error(f"Terjadi kendala pada model AI: {e}")
                st.info("Saran: Coba hapus dan buat ulang API Key di Google AI Studio jika masalah berlanjut.")
    else:
        st.warning("Mohon lengkapi input gaya dan file PDF.")
