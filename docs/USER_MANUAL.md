# 📘 AURIX User Manual
## AUdit Risk Intelligence eXcellence Platform

**Version 4.0 | December 2024**

---

## 📑 Daftar Isi

1. [Pendahuluan](#1-pendahuluan)
2. [Memulai Aplikasi](#2-memulai-aplikasi)
3. [Dashboard](#3-dashboard)
4. [Document Management](#4-document-management)
5. [PTCF Builder](#5-ptcf-builder)
6. [Risk Assessment](#6-risk-assessment)
7. [Findings Tracker](#7-findings-tracker)
8. [Continuous Audit](#8-continuous-audit)
9. [KRI Dashboard](#9-kri-dashboard)
10. [Fraud Detection](#10-fraud-detection)
11. [Regulatory Compliance](#11-regulatory-compliance)
12. [AI Chat](#12-ai-chat)
13. [Analytics](#13-analytics)
14. [Settings](#14-settings)
15. [Troubleshooting](#15-troubleshooting)

---

## 1. Pendahuluan

### 1.1 Apa itu AURIX?

AURIX (AUdit Risk Intelligence eXcellence) adalah platform AI komprehensif yang dirancang khusus untuk Internal Audit di industri keuangan Indonesia. Platform ini menggabungkan:

- **Metodologi McKinsey & Big 4** - Framework audit profesional
- **Kecerdasan Buatan (AI)** - LLM untuk analisis dan generasi dokumen
- **Regulasi Indonesia** - OJK, Bank Indonesia, ISO Standards
- **Free LLM Providers** - Groq, Together AI, Google AI Studio

### 1.2 Fitur Utama

| Modul | Fungsi |
|-------|--------|
| 📊 Dashboard | Overview metrics dan navigasi cepat |
| 📁 Documents | Upload dan manajemen dokumen audit |
| 🎭 PTCF Builder | Framework prompt engineering profesional |
| ⚖️ Risk Assessment | Penilaian risiko dengan matriks 5x5 |
| 📋 Findings Tracker | Dokumentasi temuan dengan metodologi 5Cs |
| 🔄 Continuous Audit | Monitoring real-time dan alerting |
| 📈 KRI Dashboard | Key Risk Indicators dengan gauge visual |
| 🔍 Fraud Detection | Analisis red flag dan investigasi |
| 📚 Regulations | Tracking kepatuhan regulasi |
| 🤖 AI Chat | Asisten AI untuk audit |
| 📊 Analytics | Laporan dan analitik audit |

### 1.3 Persyaratan Sistem

- **Python**: 3.10 atau lebih tinggi
- **Browser**: Chrome, Firefox, Edge (versi terbaru)
- **RAM**: Minimal 4GB
- **Storage**: 500MB untuk aplikasi

---

## 2. Memulai Aplikasi

### 2.1 Instalasi

```bash
# 1. Ekstrak file zip
unzip aurix_v4.zip
cd aurix_v4

# 2. Buat virtual environment (opsional tapi direkomendasikan)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Jalankan aplikasi
streamlit run streamlit_app.py
```

### 2.2 Konfigurasi Awal

1. **Buka Settings** (⚙️) dari sidebar
2. **Pilih AI Provider** - Rekomendasi: Groq (gratis dan cepat)
3. **Masukkan API Key** - Dapatkan dari provider yang dipilih
4. **Test Connection** - Pastikan koneksi berhasil

### 2.3 Mendapatkan API Key Gratis

| Provider | Link | Catatan |
|----------|------|---------|
| Groq | https://console.groq.com/keys | Tercepat, gratis |
| Together AI | https://api.together.xyz | Credit gratis $25 |
| Google AI Studio | https://aistudio.google.com/app/apikey | Gemini 2.0 gratis |
| OpenRouter | https://openrouter.ai/keys | Multi-model |

---

## 3. Dashboard

### 3.1 Overview

Dashboard adalah halaman utama yang menampilkan:
- **Welcome Banner** - Branding dan versi aplikasi
- **Quick Stats** - Metrik ringkas (Audit Universe, Findings, dll)
- **Quick Actions** - Akses cepat ke fitur utama
- **Risk Heat Map** - Visualisasi risiko per kategori
- **KRI Alerts** - Peringatan indikator risiko
- **Recent Activity** - Aktivitas terbaru
- **System Health** - Status kesehatan sistem

### 3.2 Navigasi

Gunakan **sidebar** di sebelah kiri untuk navigasi antar modul:
- Klik menu untuk berpindah halaman
- Gunakan toggle tema (🌙/☀️) untuk dark/light mode
- Pilih LLM provider di bagian bawah sidebar

---

## 4. Document Management

### 4.1 Upload Dokumen

1. Buka modul **📁 Documents**
2. Klik area upload atau drag-and-drop file
3. Pilih **Document Category**:
   - Audit Reports
   - SOP/Policies
   - Regulations
   - Working Papers
   - Risk Assessment
   - Financial Data
   - Compliance Documents
4. Tambahkan **Tags** (opsional, pisahkan dengan koma)
5. Klik **📥 Upload & Process**

### 4.2 Format yang Didukung

| Format | Ekstensi | Deskripsi |
|--------|----------|-----------|
| PDF | .pdf | Laporan, regulasi |
| Word | .docx | SOP, kebijakan |
| Excel | .xlsx | Data keuangan |
| CSV | .csv | Data tabular |
| Text | .txt | Catatan, log |

### 4.3 Manajemen Dokumen

- **Filter** - Berdasarkan kategori
- **Search** - Cari berdasarkan nama
- **View** - Preview konten dokumen
- **Delete** - Hapus dokumen

---

## 5. PTCF Builder

### 5.1 Apa itu PTCF?

PTCF (Persona-Task-Context-Format) adalah framework prompt engineering profesional untuk menghasilkan output AI yang berkualitas tinggi.

### 5.2 Komponen PTCF

| Komponen | Deskripsi | Contoh |
|----------|-----------|--------|
| **Persona** | Peran AI | Internal Audit Manager |
| **Task** | Tugas spesifik | Buat prosedur audit kredit |
| **Context** | Konteks tambahan | Untuk bank dengan NPL 5% |
| **Format** | Format output | Checklist dengan 10 langkah |

### 5.3 Cara Menggunakan

1. **Pilih Template** atau mulai dari awal
2. **Isi Persona** - Pilih dari dropdown atau custom
3. **Definisikan Task** - Jelaskan tugas dengan detail
4. **Tambahkan Context** - Informasi pendukung
5. **Tentukan Format** - Output yang diinginkan
6. **Generate** - Klik untuk menghasilkan prompt
7. **Copy/Export** - Gunakan prompt di AI Chat

### 5.4 Template Tersedia

- Credit Risk Assessment
- Operational Risk Review
- IT Audit Checklist
- Compliance Testing
- Fraud Investigation
- Dan lainnya...

---

## 6. Risk Assessment

### 6.1 Metodologi

Platform menggunakan matriks risiko 5x5 dengan dimensi:
- **Likelihood** (1-5): Kemungkinan terjadinya risiko
- **Impact** (1-5): Dampak jika risiko terjadi

### 6.2 Risk Score

| Score | Level | Warna | Aksi |
|-------|-------|-------|------|
| 15-25 | HIGH | 🔴 Merah | Immediate action required |
| 8-14 | MEDIUM | 🟡 Kuning | Monitor closely |
| 1-7 | LOW | 🟢 Hijau | Accept/periodic review |

### 6.3 Membuat Assessment

1. Buka **⚖️ Risk Assessment**
2. Pilih tab **➕ New Assessment**
3. Isi detail:
   - Risk Area (dari Audit Universe)
   - Risk Description
   - Likelihood (1-5)
   - Impact (1-5)
   - Current Controls
   - Mitigating Actions
4. Klik **Save Assessment**

### 6.4 Audit Universe

Platform mencakup 36 area audit dalam 6 kategori:
- Credit Risk
- Operational Risk
- Compliance Risk
- IT/Cyber Risk
- Financial Risk
- Strategic Risk

---

## 7. Findings Tracker

### 7.1 Metodologi 5Cs

Setiap finding didokumentasikan dengan framework 5Cs:

| C | Nama | Deskripsi |
|---|------|-----------|
| 1 | **Condition** | Apa yang ditemukan (fakta) |
| 2 | **Criteria** | Standar/regulasi yang dilanggar |
| 3 | **Cause** | Penyebab kondisi terjadi |
| 4 | **Consequence** | Dampak/risiko dari kondisi |
| 5 | **Corrective Action** | Rekomendasi perbaikan |

### 7.2 Membuat Finding

1. Buka **📋 Findings Tracker**
2. Pilih tab **➕ New Finding**
3. Isi informasi:
   - Finding Title
   - Audit Area
   - Severity (Critical/High/Medium/Low)
   - Due Date
   - 5Cs Details
4. Klik **Save Finding**

### 7.3 Status Finding

| Status | Deskripsi |
|--------|-----------|
| Open | Baru dibuat, belum ditindaklanjuti |
| In Progress | Sedang dalam proses perbaikan |
| Closed | Sudah selesai dan diverifikasi |
| Overdue | Melewati due date |

### 7.4 AI Generate Finding

Gunakan fitur **AI Generate** untuk:
- Mengisi 5Cs secara otomatis dari deskripsi
- Mendapatkan rekomendasi severity
- Menyarankan corrective action

---

## 8. Continuous Audit

### 8.1 Konsep

Continuous Audit memungkinkan monitoring real-time dengan:
- **Rules** - Aturan yang mendefinisikan kondisi alert
- **Alerts** - Notifikasi saat rule terpicu
- **Dashboard** - Visualisasi status monitoring

### 8.2 Tipe Rule

| Tipe | Deskripsi | Contoh |
|------|-----------|--------|
| Threshold | Nilai melebihi batas | NPL > 5% |
| Pattern | Pola tertentu terdeteksi | Transaksi berulang |
| Anomaly | Deviasi dari normal | Lonjakan tidak wajar |
| Comparison | Perbandingan periode | MoM increase > 20% |
| Sequence | Urutan kejadian | Login -> Transfer -> Delete |

### 8.3 Membuat Rule

1. Buka **🔄 Continuous Audit**
2. Pilih tab **➕ Create Rule**
3. Konfigurasi:
   - Rule Name
   - Category
   - Rule Type
   - Threshold/Condition
   - Severity
   - Notification Channel
4. Klik **Save Rule**

### 8.4 Mengelola Alert

- **Review** - Tandai alert sudah direview
- **Escalate** - Eskalasi ke level lebih tinggi
- **Close** - Tutup alert yang sudah ditangani
- **Create Finding** - Konversi ke formal finding

---

## 9. KRI Dashboard

### 9.1 Key Risk Indicators

KRI adalah metrik yang mengindikasikan tingkat risiko. Platform memantau 20+ KRI dalam 6 kategori:

### 9.2 Kategori KRI

| Kategori | Contoh Indikator |
|----------|------------------|
| Credit Risk | NPL Ratio, LTV, Concentration |
| Liquidity Risk | LCR, NSFR, Funding Gap |
| Operational Risk | System Downtime, Error Rate |
| Compliance Risk | Violation Count, Training Completion |
| IT/Cyber Risk | Incident Count, Patch Compliance |
| Market Risk | VaR Breach, Interest Rate Gap |

### 9.3 Status Indikator

| Status | Kondisi | Aksi |
|--------|---------|------|
| 🟢 Healthy | Di bawah threshold | Monitor rutin |
| 🟡 Warning | Mendekati threshold | Perhatian khusus |
| 🔴 Breached | Melebihi threshold | Tindakan segera |

### 9.4 Trend Analysis

- Lihat tren 12 bulan terakhir
- Identifikasi pola seasonal
- Bandingkan dengan threshold
- Update nilai KRI secara manual

---

## 10. Fraud Detection

### 10.1 Red Flag Scanner

Tool untuk menganalisis transaksi/aktivitas terhadap indikator fraud:

1. Input detail transaksi
2. Checklist red flags yang terdeteksi
3. Sistem menghitung risk score
4. Buat case jika diperlukan

### 10.2 Kategori Red Flags

| Kategori | Jumlah Flags |
|----------|--------------|
| Financial Statement Fraud | 12 flags |
| Asset Misappropriation | 10 flags |
| Procurement Fraud | 8 flags |
| Credit Fraud | 10 flags |
| AML Red Flags | 15 flags |

### 10.3 Case Management

- **Open** - Case baru
- **Under Investigation** - Sedang diinvestigasi
- **Escalated** - Dieskalasi ke manajemen
- **Closed - Confirmed** - Fraud terkonfirmasi
- **Closed - False Positive** - Bukan fraud

### 10.4 Risk Score

| Score | Level | Interpretasi |
|-------|-------|--------------|
| 0-30 | Low | Risiko rendah |
| 31-69 | Medium | Perlu investigasi |
| 70-100 | High | Prioritas tinggi |

---

## 11. Regulatory Compliance

### 11.1 Regulasi yang Dicover

| Regulator | Regulasi |
|-----------|----------|
| OJK | POJK terkait perbankan, asuransi |
| Bank Indonesia | PBI tentang sistem pembayaran |
| BPKH | Regulasi pengelolaan haji |
| ISO | ISO 27001, ISO 31000 |

### 11.2 Compliance Status

| Status | Deskripsi |
|--------|-----------|
| Compliant | Memenuhi semua requirement |
| Partial | Memenuhi sebagian |
| Non-Compliant | Tidak memenuhi |
| Under Review | Sedang direview |

### 11.3 Compliance Score

Score 0-100% menunjukkan tingkat kepatuhan:
- **90-100%**: Excellent
- **80-89%**: Good
- **70-79%**: Acceptable
- **60-69%**: Needs Improvement
- **<60%**: Critical

### 11.4 Review Calendar

- Lihat jadwal review regulasi
- Filter berdasarkan periode
- Identifikasi yang overdue
- Plan upcoming reviews

---

## 12. AI Chat

### 12.1 Fitur Chat

- Tanya jawab tentang audit
- Generate dokumen
- Analisis risiko
- Bantuan regulasi
- Panduan prosedur

### 12.2 Persona AI

| Persona | Keahlian |
|---------|----------|
| Internal Audit Manager | Strategi dan perencanaan audit |
| Compliance Officer | Kepatuhan regulasi |
| Risk Analyst | Analisis dan penilaian risiko |
| IT Auditor | Audit sistem dan cybersecurity |
| Fraud Examiner | Investigasi fraud |

### 12.3 Tips Efektif

1. **Be Specific** - Jelaskan konteks dengan detail
2. **Use PTCF** - Gunakan prompt dari PTCF Builder
3. **Iterate** - Minta perbaikan jika perlu
4. **Verify** - Selalu validasi output AI

### 12.4 Quick Prompts

Template cepat untuk tugas umum:
- "Buat prosedur audit untuk..."
- "Jelaskan risiko terkait..."
- "Apa requirement regulasi..."
- "Identifikasi red flags pada..."

---

## 13. Analytics

### 13.1 Performance Analytics

- Audit completion rate
- Average audit duration
- Resource utilization
- Documentation quality

### 13.2 Coverage Analytics

- Coverage by audit universe
- Risk-based coverage
- Audit cycle compliance
- Gap identification

### 13.3 Trend Analytics

- Monthly audit activity
- Year-over-year comparison
- Finding trends
- KRI trends

### 13.4 Reports

**Standard Reports:**
- Quarterly Audit Report
- Annual Risk Assessment
- Finding Status Report
- Compliance Summary
- KRI Performance Report

**Custom Reports:**
- Pilih periode
- Pilih sections
- Export ke Excel/PDF

---

## 14. Settings

### 14.1 AI Provider

1. Pilih provider dari daftar
2. Masukkan API key
3. Pilih model
4. Test connection

### 14.2 Appearance

- **Theme**: Dark / Light mode
- **Language**: Indonesia / English
- **Compact Mode**: Tampilan lebih padat
- **Tooltips**: Tampilkan bantuan

### 14.3 General

- Auto-save interval
- Notifications
- Session info
- Keyboard shortcuts

### 14.4 Data & Export

- Default export format
- Data retention
- Backup & restore
- Clear all data

---

## 15. Troubleshooting

### 15.1 Masalah Umum

**Aplikasi tidak bisa diakses**
```bash
# Pastikan port 8501 tidak digunakan
lsof -i :8501
# Jalankan di port lain
streamlit run streamlit_app.py --server.port 8502
```

**Import error**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**AI tidak merespons**
- Periksa API key di Settings
- Test connection
- Cek kuota/limit provider

### 15.2 Error Messages

| Error | Solusi |
|-------|--------|
| "Module not found" | `pip install <module>` |
| "API key invalid" | Periksa kembali API key |
| "Connection timeout" | Cek koneksi internet |
| "Rate limit exceeded" | Tunggu atau ganti provider |

### 15.3 Kontak Support

- **GitHub**: https://github.com/mshadianto
- **Email**: sopian.hadianto@gmail.com
- **Documentation**: https://docs.aurix.id

---

## 📋 Appendix

### A. Keyboard Shortcuts

| Shortcut | Fungsi |
|----------|--------|
| `Ctrl + K` | Quick search |
| `Ctrl + S` | Save current work |
| `Ctrl + /` | Toggle sidebar |
| `Ctrl + D` | Toggle dark mode |
| `Esc` | Close modal |

### B. Glossary

| Term | Definisi |
|------|----------|
| KRI | Key Risk Indicator |
| PTCF | Persona-Task-Context-Format |
| 5Cs | Condition, Criteria, Cause, Consequence, Corrective Action |
| NPL | Non-Performing Loan |
| LCR | Liquidity Coverage Ratio |
| RAG | Retrieval-Augmented Generation |

### C. Version History

| Version | Date | Highlights |
|---------|------|------------|
| 4.0.0 | Dec 2024 | Complete redesign, new modules |
| 3.0.0 | Nov 2024 | PostgreSQL, visitor analytics |
| 2.0.0 | Oct 2024 | RAG implementation |
| 1.0.0 | Sep 2024 | Initial release |

---

**© 2025 MS Hadianto. All Rights Reserved.**

*AURIX - Intelligent Audit. Elevated Assurance.*
