import streamlit as st
import google.generativeai as genai
import PyPDF2
import io

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Miftah X-Generator Pro", page_icon="🐦")

st.title("🐦 X Content Generator by Miftah")
st.write("Aplikasi untuk membuat konten X yang jujur, analitis, dan bebas 'AI-Slop'.")

# 2. Setup API Key secara Aman
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("API Key tidak ditemukan di 'Secrets' Streamlit.")
    st.stop()

# 3. Fungsi Ekstrak PDF & Pencarian Model
def get_best_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for target in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro']:
            if target in available_models: return target
        return available_models[0] if available_models else 'models/gemini-1.5-flash'
    except:
        return 'models/gemini-1.5-flash'

def extract_pdf_text(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    return "".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])

# 4. Antarmuka Pengguna (UI)
persona = st.text_input("Gaya Karakter", placeholder="Contoh: Ferry Irwandi")

format_pilihan = st.selectbox(
    "Pilih Format Hasil Postingan:",
    ("Single Post", "Thread (5 Tweet)", "Long Post")
)

uploaded_file = st.file_uploader("Upload PDF Proyek", type="pdf")

if st.button("Generate Postingan ✨"):
    if persona and uploaded_file:
        with st.spinner(f"Sedang meracik {format_pilihan}..."):
            raw_text = extract_pdf_text(uploaded_file)
            working_model = get_best_model()
            model = genai.GenerativeModel(working_model)
            
            # --- LOGIKA TUGAS UTAMA (DIPERKETAT) ---
            if format_pilihan == "Single Post":
                tugas_absolut = "TUGAS: HANYA BUAT 1 TWEET SINGKAT (maks 280 karakter). Dilarang membuat thread atau teks panjang."
            elif format_pilihan == "Thread (5 Tweet)":
                tugas_absolut = "TUGAS: HANYA BUAT THREAD 5 TWEET (masing-masing maks 280 karakter). Dilarang menggabungkannya menjadi satu tweet tunggal."
            else:
                tugas_absolut = "TUGAS: HANYA BUAT 1 POSTINGAN PANJANG (maks 1000 karakter). Pastikan isi penuh dengan analisis kritis dan mendalam."

            # --- PROMPT DENGAN STRUKTUR PRIORITAS ---
            prompt = f"""
            {tugas_absolut}

            PERSONA: {persona}
            DATA PROYEK: {raw_text[:8000]}

            GAYA BAHASA & NADA (WAJIB):
            - Tenang, reflektif, hangat, analitis. Kalimat pendek; satu ide per baris.
            - Nada: berdiskusi antar pemikir, bukan menggurui atau berjualan.
            - Dilarang: janji keuntungan, prediksi harga, FOMO, atau promosi agresif.

            OVERRIDE RULE — ANTI AI-SLOP:
            1. Konten harus spesifik pada mekanisme unik proyek, bukan umum.
            2. Tambahkan sudut pandang/reframing, jangan hanya ringkasan.
            3. Gunakan bahasa hipotesis/probabilistik (bukan klaim absolut).
            4. Tutup dengan refleksi atau implikasi desain.
            5. Tampilkan jumlah karakter di akhir output.
            """
            
            try:
                response = model.generate_content(prompt)
                st.divider()
                st.subheader(f"Hasil {format_pilihan}:")
                # Menampilkan dalam box agar mudah dibaca/copy
                st.info(response.text)
                st.balloons()
            except Exception as e:
                st.error(f"Gagal generate: {e}")
    else:
        st.warning("Mohon isi gaya karakter dan unggah file PDF.")
