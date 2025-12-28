# ❓ AURIX FAQ
## Frequently Asked Questions

---

## General Questions

### Q: Apa itu AURIX?
**A:** AURIX (AUdit Risk Intelligence eXcellence) adalah platform AI komprehensif untuk Internal Audit di industri keuangan Indonesia. Platform ini menggabungkan metodologi McKinsey dan Big 4 dengan kecerdasan buatan modern.

### Q: Apakah AURIX gratis?
**A:** Ya, platform AURIX adalah open source dan gratis. LLM providers yang digunakan (Groq, Together AI, Google) juga menyediakan tier gratis yang cukup untuk penggunaan normal.

### Q: Siapa yang membuat AURIX?
**A:** AURIX dikembangkan oleh MS Hadianto, seorang GRC Expert dan AI-Powered Builder. Platform ini dibuat untuk komunitas auditor Indonesia.

### Q: Regulasi apa saja yang di-cover?
**A:** AURIX mencakup regulasi dari:
- OJK (Otoritas Jasa Keuangan)
- Bank Indonesia
- PPATK (AML/CFT)
- ISO Standards (27001, 31000)

---

## Technical Questions

### Q: Apa persyaratan sistem minimum?
**A:** 
- Python 3.10+
- RAM 4GB minimum (8GB recommended)
- Storage 500MB
- Browser modern (Chrome, Firefox, Edge)

### Q: Bagaimana cara install AURIX?
**A:** 
```bash
# Extract zip
unzip aurix_v4.zip
cd aurix_v4

# Install dependencies
pip install -r requirements.txt

# Run
streamlit run streamlit_app.py
```
Lihat INSTALLATION_GUIDE.md untuk detail lengkap.

### Q: Apakah bisa di-deploy di cloud?
**A:** Ya, AURIX bisa di-deploy di:
- Streamlit Cloud (gratis)
- AWS / Azure / GCP
- On-premise server
- Docker container

### Q: Apakah perlu database?
**A:** Opsional. AURIX bisa berjalan tanpa database (data disimpan di session). Untuk persistensi, bisa koneksi ke PostgreSQL.

---

## AI & LLM Questions

### Q: Provider AI apa yang didukung?
**A:**
| Provider | Tier Gratis | Speed |
|----------|-------------|-------|
| Groq | ✅ Gratis | Tercepat |
| Together AI | ✅ $25 credit | Cepat |
| Google AI Studio | ✅ Gratis | Cepat |
| OpenRouter | ✅ Gratis (limited) | Varies |
| Ollama | ✅ Local | Varies |

### Q: Bagaimana cara mendapatkan API key?
**A:** 
1. Daftar di website provider (gratis)
2. Buat API key di dashboard
3. Masukkan ke Settings di AURIX
4. Test connection

### Q: Apakah data saya aman?
**A:** 
- Data hanya dikirim ke LLM provider saat Anda menggunakan AI Chat
- LLM providers umumnya tidak menyimpan/melatih dari data Anda
- Untuk keamanan maksimal, gunakan Ollama (local)
- Opsi on-premise tersedia

### Q: Bagaimana jika API limit tercapai?
**A:** 
- Switch ke provider lain (bisa punya multiple keys)
- Gunakan mock mode untuk demo/testing
- Tunggu reset (biasanya per hari/bulan)

---

## Feature Questions

### Q: Apa itu PTCF?
**A:** PTCF adalah framework prompt engineering:
- **P**ersona - Siapa yang menjawab
- **T**ask - Apa yang diminta
- **C**ontext - Informasi pendukung
- **F**ormat - Bentuk output

Framework ini memastikan output AI konsisten dan berkualitas.

### Q: Apa itu metodologi 5Cs?
**A:** 5Cs adalah framework dokumentasi finding dari Big 4:
- **C**ondition - Fakta yang ditemukan
- **C**riteria - Standar yang dilanggar
- **C**ause - Penyebab kondisi
- **C**onsequence - Dampak jika tidak diperbaiki
- **C**orrective Action - Rekomendasi

### Q: Berapa banyak KRI yang dipantau?
**A:** 20+ Key Risk Indicators dalam 6 kategori:
- Credit Risk
- Liquidity Risk
- Operational Risk
- Compliance Risk
- IT/Cyber Risk
- Market Risk

### Q: Apa saja red flags fraud yang tersedia?
**A:** 60+ red flags dalam 5 kategori:
- Financial Statement Fraud
- Asset Misappropriation
- Procurement Fraud
- Credit Fraud
- AML Red Flags

---

## Usage Questions

### Q: Apakah perlu training khusus?
**A:** Tidak. Interface dirancang intuitif untuk auditor. Training 2-4 jam cukup untuk penguasaan dasar. User manual lengkap tersedia.

### Q: Bisa digunakan untuk industri selain keuangan?
**A:** Ya, dengan modifikasi. Framework PTCF dan 5Cs universal. Seed data (regulasi, KRI, red flags) bisa disesuaikan untuk industri lain.

### Q: Bagaimana cara export laporan?
**A:** 
1. Buka Analytics
2. Pilih Report yang diinginkan
3. Klik Generate/Export
4. Pilih format (Excel, PDF, CSV)

### Q: Bisa integrasi dengan sistem lain?
**A:** Ya, melalui:
- Python API
- Database connection
- File import/export
- Custom development

---

## Troubleshooting

### Q: Aplikasi tidak bisa diakses
**A:** 
1. Cek apakah sudah menjalankan `streamlit run streamlit_app.py`
2. Coba port lain: `--server.port 8502`
3. Pastikan tidak ada firewall blocking

### Q: Error "Module not found"
**A:** 
```bash
pip install -r requirements.txt --force-reinstall
```

### Q: AI tidak merespons
**A:** 
1. Cek API key di Settings
2. Test connection
3. Coba provider lain
4. Gunakan mock mode untuk testing

### Q: Data hilang setelah restart
**A:** Secara default, data disimpan di session. Untuk persistensi:
1. Koneksi ke database PostgreSQL, atau
2. Export data sebelum menutup (Data & Export di Settings)

---

## Support

### Q: Dimana dokumentasi lengkap?
**A:** 
- USER_MANUAL.md - Panduan lengkap
- DEMO_GUIDE.md - Panduan demo
- QUICK_REFERENCE.md - Referensi cepat
- INSTALLATION_GUIDE.md - Panduan instalasi

### Q: Bagaimana melaporkan bug?
**A:** 
1. GitHub Issues: github.com/mshadianto/aurix/issues
2. Sertakan screenshot dan langkah reproduksi
3. Sebutkan versi AURIX dan browser yang digunakan

### Q: Apakah ada community?
**A:** 
- GitHub: github.com/mshadianto
- LinkedIn: linkedin.com/in/mshadianto
- Email: sopian.hadianto@gmail.com

### Q: Bagaimana cara kontribusi?
**A:** 
1. Fork repository
2. Buat branch baru
3. Submit pull request
4. Ikuti coding standards

---

## Future Plans

### Q: Apa roadmap ke depan?
**A:** 
- v4.1: User authentication, role-based access
- v4.2: API integrations, mobile responsive
- v5.0: ML-based prediction, workflow automation

### Q: Bisa request fitur baru?
**A:** Ya! Submit feature request di GitHub Issues dengan label "enhancement".

---

*© 2025 MS Hadianto - AURIX Platform*
