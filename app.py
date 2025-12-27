import streamlit as st
import google.generativeai as genai
import PyPDF2
import io

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Miftah X-Generator Pro", page_icon="🐦")

st.title("🐦 X Content Generator by Miftah")
st.write("Aplikasi ini akan membantu kamu dalam membuat konten X sesuai dengan role model kamu.")

# 2. Setup API Key secara Aman
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("API Key tidak ditemukan di 'Secrets' Streamlit.")
    st.stop()

# 3. Fungsi Diagnostik & Ekstrak PDF
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
    ("Single Post (280 Karakter Huruf)", "Thread (5 Tweet)", "Long Post (1000 Karakter Huruf - Deep Insight)")
)

uploaded_file = st.file_uploader("Upload PDF Proyek", type="pdf")

if st.button("Generate Postingan ✨"):
    if persona and uploaded_file:
        with st.spinner(f"Sedang meracik {format_pilihan} dengan standar Anti AI-Slop..."):
            raw_text = extract_pdf_text(uploaded_file)
            working_model = get_best_model()
            model = genai.GenerativeModel(working_model)
            
            # --- SISTEM INSTRUKSI (GAYA BAHASA & LARANGAN) ---
            sistem_rules = """
            GAYA BAHASA & NADA:
            - Tenang, reflektif, hangat, analitis.
            - Bahasa Indonesia rapi, netral, kalimat pendek.
            - Satu ide per baris; gunakan line breaks.
            - Nada: berdiskusi antar pemikir, bukan menggurui atau berjualan.
            - Hindari slang ("gue/lo") dan jargon tanpa konteks.

            LARANGAN (WAJIB):
            - Tidak: janji keuntungan, prediksi harga, FOMO, promosi agresif.
            - Tidak: teks generik, klikbait emosional, tribalism.
            - Jangan menyertakan catatan proses atau metadata dalam output.

            OVERRIDE RULE — ANTI AI-SLOP (FINAL GATE):
            Sebelum mengirim output, pastikan:
            1. Konten spesifik pada mekanisme unik proyek, bukan umum.
            2. Tambahkan sudut pandang/reframing, jangan hanya ringkasan.
            3. Pecah ritme agar tidak template-like.
            4. Gunakan bahasa hipotesis/probabilistik (bukan klaim absolut).
            5. Kembali ke analisis insentif dan trade-off (bukan hype).
            6. Tutup dengan refleksi atau implikasi desain (bukan CTA klise).
            7. Konten harus terasa 'jujur dan berpikir' daripada 'rapi dan pintar'.
            """

            if format_pilihan == "Single Post (280 Karakter)":
                tugas = "Buat 1 tweet (maks 280 karakter huruf) dengan hook provokatif cerdas."
            elif format_pilihan == "Thread (5 Tweet)":
                tugas = "Buat thread 5 tweet (masing-masing maks 280 karakter huruf) yang mengalir dari masalah ke analisis."
            else:
                tugas = "Buat 1 long post (maks 1000 karakter huruf) yang penuh analisis kritis dan konsekuensi tidak eksplisit."

            prompt = f"{sistem_rules}\n\nDATA PROYEK: {raw_text[:8000]}\nPERSONA: {persona}\nTUGAS: {tugas}"
            
            try:
                response = model.generate_content(prompt)
                st.divider()
                st.subheader(f"Hasil {format_pilihan}:")
                # Menampilkan teks dengan format line break yang benar
                st.write(response.text)
                st.balloons()
            except Exception as e:
                st.error(f"Gagal generate: {e}")
    else:
        st.warning("Mohon isi gaya dan upload file PDF.")
