**Overview**

Project ini melakukan analisis model pertumbuhan Solow pada data GDP menggunakan metode numerik Euler untuk integrasi/diskretisasi. Tujuan: mereplikasi dinamika modal per pekerja (atau per efektif worker) dan melihat implikasi parameter (tabungan, depresiasi, pertumbuhan populasi dan teknologi) terhadap keseimbangan jangka panjang.

**Files**
- **`app.py`**: Script utama untuk memuat data, menjalankan simulasi model Solow dengan metode Euler, dan menghasilkan visualisasi / ringkasan hasil.
- **`GDP.csv`**: Data input (mis. tahun, GDP, populasi atau kolom terkait). Periksa kolom aktual sebelum menjalankan; contoh kolom yang umum: `Year`, `GDP`, `Population`.
- **`gdp.ipynb`**: Notebook analisis interaktif (opsional) dengan eksplorasi data dan langkah-langkah yang sama secara notebook.

**Requirements**
- **Python** 3.8+ (disarankan). Dependency tercantum di `requirements.txt`.

**Quick Start (Windows PowerShell)**
1. Pasang dependency:

```powershell
pip install -r requirements.txt
```

2. Jalankan analisis (sederhana):

```powershell
python app.py
```

Catatan: Jika `app.py` menerima argumen (mis. path file atau parameter model), panggil sesuai opsi yang ada. Periksa header atau help di `app.py`.

**Ringkasan Model Solow (sederhana)**
Model Solow standar (per efektif worker) memodelkan evolusi modal per efektif worker $k$ sebagai:

$$
\frac{dk}{dt} = s\,f(k) - (n + g + \delta)\,k
$$

Di mana:
- $s$ = laju tabungan (saving rate)
- $f(k)$ = fungsi produksi per pekerja (mis. Cobb-Douglas $f(k)=k^{\alpha}$)
- $n$ = laju pertumbuhan populasi
- $g$ = laju pertumbuhan teknologi (efektivitas tenaga kerja)
- $\delta$ = laju depresiasi modal

Keseimbangan stasioner $k^*$ dipenuhi saat $dk/dt = 0$.

**Metode Numerik: Euler Eksplisit**
Untuk mensimulasikan persamaan diferensial di atas secara numerik, Euler eksplisit memdiskretkan waktu dengan langkah $\Delta t$ dan memperbarui $k$ sebagai:

$$
k_{t+\Delta t} = k_t + \Delta t \;\bigl( s\,f(k_t) - (n + g + \delta)\,k_t \bigr)
$$

Implementasi Euler mudah dan cepat; perhatikan kestabilan numerik (pilih $\Delta t$ yang cukup kecil untuk hasil yang stabil).

**Apa yang dilakukan `app.py` (umum)**
- Memuat `GDP.csv` dan menyiapkan seri input (mis. GDP per kapita jika perlu).
- Mengestimasikan atau menerima parameter model (mis. $s$, $\alpha$, $n$, $g$, $\delta$).
- Menentukan fungsi produksi (seringnya Cobb-Douglas) dan memulai simulasi Euler dari kondisi awal $k_0$.
- Menyimpan atau menampilkan output: grafik lintasan $k(t)$, output per pekerja, dan perbandingan data observasi bila relevan.

**Data (`GDP.csv`)**
- Periksa isi kolom terlebih dahulu. README ini mengasumsikan minimal ada kolom tahun (`Year`) dan ukuran output seperti `GDP` serta, bila tersedia, `Population`.
- Jika hanya tersedia GDP total, Anda mungkin perlu menghitung GDP per kapita: `GDP / Population`.

**Menyesuaikan parameter**
- Parameter penting: `s` (saving rate), `alpha` (produktivitas modal dalam Cobb-Douglas), `n`, `g`, `delta`, dan `delta_t` (langkah waktu untuk Euler).
- Untuk eksperimen, jalankan simulasi di rentang parameter dan bandingkan lintasan ke keadaan stasioner.

**Tips reproduksi**
- Jalankan `python app.py` setelah memasang dependensi.
- Atau buka `gdp.ipynb` untuk alur interaktif jika tersedia.

**Interpretasi hasil singkat**
- Jika lintasan modal per pekerja mendekati nilai tetap, negara/daerah dalam dataset mengarah ke keadaan stasioner menurut asumsi model.
- Sensitivitas terhadap `s` dan $\alpha$ seringkali paling besar: laju tabungan dan elastisitas modal mengubah level $k^*$ yang tercapai.

**Catatan & Limitasi**
- Model Solow adalah model sederhana: mengabaikan beberapa fitur seperti perbedaan sektor, human capital, friksi pasar, atau shock sementara.
- Euler eksplisit mudah tapi bisa numerically unstable untuk langkah waktu besar; pertimbangkan metode yang lebih baik (Runge–Kutta) bila diperlukan.

**Sumber & Referensi**
- Mankiw, Romer, Weil (1992) — introduksi Solow modern.
- Literatur dasar ekonomi pertumbuhan dan numerik untuk teknik Euler.

**Kontak / Pengembangan selanjutnya**
- Jika Anda ingin saya menambahkan instruksi menjalankan `app.py` dengan argumen, contoh output, atau menulis skrip pengujian otomatis, beri tahu saya dan saya akan tambahkan.

---
File README ini diperbarui secara otomatis untuk menjelaskan cara menggunakan `app.py` dan data `GDP.csv`, serta memberikan konteks model Solow dan metode Euler.
