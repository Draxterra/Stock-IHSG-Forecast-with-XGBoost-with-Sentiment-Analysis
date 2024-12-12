# Stock-IHSG-Forecast-with-XGBoost-with-Sentiment-Analysis

Proyek ini merupakan bagian dari tugas akhir saya sebagai mahasiswa Data Science. Proyek ini berfokus pada peramalan Indeks Harga Saham Gabungan (IHSG) menggunakan algoritma *Extreme Gradient Boosting* (XGBoost) yang dikombinasikan dengan analisis sentimen berita finansial.

## Deskripsi Proyek

IHSG adalah indikator utama pasar saham di Indonesia. Peramalan pergerakan IHSG menjadi tantangan menarik karena dipengaruhi oleh banyak faktor, termasuk data historis dan sentimen pasar yang dipengaruhi oleh berita.

Tujuan utama dari proyek ini adalah:

1. Membuat model prediksi IHSG menggunakan XGBoost.
2. Melakukan analisis sentimen terhadap berita finansial sebagai salah satu fitur input untuk model prediksi.
3. Mengintegrasikan data sentimen dan data historis untuk meningkatkan akurasi prediksi IHSG.

## Dataset

Proyek ini menggunakan dua jenis dataset:

1. **Data Historis IHSG**: Data ini mencakup harga penutupan, volume perdagangan, dan data teknikal lainnya yang diambil dari sumber terpercaya seperti Yahoo Finance atau IDX.
2. **Data Berita Finansial**: Artikel berita finansial yang dikumpulkan dari berbagai sumber, seperti situs berita ekonomi, untuk melakukan analisis sentimen.

## Teknologi yang Digunakan

- **Python**: Bahasa pemrograman utama untuk analisis data dan implementasi model.
- **XGBoost**: Algoritma pembelajaran mesin berbasis *gradient boosting* untuk prediksi.
- **LLM Chatgpt**: Untuk analisis sentimen teks berita.
- **Pandas dan NumPy**: Untuk manipulasi dan analisis data.
- **Matplotlib**: Untuk visualisasi data.
- **Scikit-learn**: Untuk praproses data dan evaluasi model.

## Hasil dan Visualisasi

Hasil dari proyek ini meliputi:

- Visualisasi hubungan antara data historis IHSG dan sentimen berita finansial.
- Evaluasi akurasi model prediksi IHSG menggunakan metrik seperti RMSE, MAE, dan R-squared.
- Prediksi pergerakan IHSG berdasarkan data terbaru.


## Cara Menjalankan Proyek

1. **Clone repositori ini**:
Untuk duplikasi proyek, gunakan perintah berikut:
   ```bash
   git clone https://github.com/Draxterra/Stock-IHSG-Forecast-with-XGBoost-with-Sentiment-Analysis.git
  
3. **Install dependencies**:
Untuk menginstal dependencies proyek, gunakan perintah berikut:

  ```bash
  pip install -r requirements.txt

```
## Jalankan notebook atau script

- Gunakan *Jupyter Notebook* untuk menjalankan file di folder `notebooks`.
- Atau, jalankan file di folder `src` untuk pipeline end-to-end.


## Kontak

Jika ada pertanyaan atau diskusi terkait proyek ini, silakan hubungi saya melalui email: rizkiwirat13@gmail.com.


