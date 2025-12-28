# 🎬 AURIX Demo Guide
## Panduan Demonstrasi Aplikasi

**Durasi Demo: 15-30 menit**

---

## 📋 Persiapan Demo

### Checklist Sebelum Demo

- [ ] Aplikasi berjalan di `localhost:8501`
- [ ] Browser dalam mode fullscreen (F11)
- [ ] Dark mode aktif (lebih profesional)
- [ ] Semua sample data sudah ter-load
- [ ] API key sudah dikonfigurasi (opsional, bisa mock)

### Audience Target

| Audience | Fokus Demo |
|----------|------------|
| Manajemen Audit | Dashboard, Analytics, KRI |
| Staff Auditor | PTCF, Findings, Documents |
| IT/Technical | Architecture, Settings, Integration |
| Regulator/External | Compliance, Risk Assessment |

---

## 🎯 Skenario Demo

### Demo Singkat (5 menit)

1. **Dashboard Overview** (1 menit)
2. **PTCF Builder** - Quick generate (2 menit)
3. **KRI Dashboard** - Visual gauges (1 menit)
4. **AI Chat** - Quick question (1 menit)

### Demo Standard (15 menit)

1. Dashboard Overview (2 menit)
2. Document Upload (2 menit)
3. PTCF Builder (3 menit)
4. Risk Assessment (2 menit)
5. Findings Tracker (2 menit)
6. KRI Dashboard (2 menit)
7. AI Chat (2 menit)

### Demo Lengkap (30 menit)

Semua modul dengan penjelasan detail.

---

## 📍 Step-by-Step Demo Script

### Opening (1 menit)

```
"Selamat pagi/siang. Hari ini saya akan mendemonstrasikan AURIX - 
platform AI untuk Internal Audit yang menggabungkan metodologi 
McKinsey dan Big 4 dengan kecerdasan buatan modern."

"AURIX dirancang khusus untuk industri keuangan Indonesia dengan 
dukungan regulasi OJK, Bank Indonesia, dan standar ISO."
```

---

### 1️⃣ Dashboard (2 menit)

**Narasi:**
```
"Ini adalah Dashboard utama AURIX. Di sini kita bisa melihat 
ringkasan kondisi audit secara real-time."
```

**Tunjukkan:**
- [ ] Welcome banner dengan branding
- [ ] Quick stats (Audit Universe: 36 areas, 6 categories)
- [ ] Risk Heat Map - "Visualisasi risiko per kategori"
- [ ] KRI Alerts - "Peringatan indikator yang perlu perhatian"
- [ ] System Health - "Status kesehatan komponen sistem"

**Highlight:**
```
"Perhatikan Risk Heat Map ini. Setiap bar menunjukkan proporsi 
area dengan risiko High, Medium, dan Low. Ini membantu auditor 
untuk prioritisasi."
```

---

### 2️⃣ Document Management (2 menit)

**Narasi:**
```
"Modul Documents memungkinkan kita upload dan mengelola 
dokumen audit. Dokumen ini nantinya bisa digunakan sebagai 
context untuk AI."
```

**Demo:**
1. Klik **📁 Documents** di sidebar
2. Tunjukkan area upload
3. Demo upload file sample (gunakan file PDF/TXT)
4. Pilih kategori "Audit Reports"
5. Tambahkan tags: "credit, 2024, risk"
6. Klik Upload & Process

**Highlight:**
```
"Platform mendukung berbagai format: PDF, Word, Excel, CSV, 
dan Text. Semua dokumen dikategorikan untuk memudahkan pencarian."
```

---

### 3️⃣ PTCF Builder (3 menit) ⭐ HIGHLIGHT

**Narasi:**
```
"PTCF Builder adalah fitur unggulan AURIX. PTCF adalah framework 
prompt engineering profesional - Persona, Task, Context, Format."
```

**Demo:**
1. Klik **🎭 PTCF Builder**
2. Tunjukkan template library
3. Pilih template "Credit Risk Assessment"
4. Jelaskan setiap komponen:

```
"Persona: Siapa yang akan menjawab - Internal Audit Manager
Task: Apa yang kita minta - Buat prosedur audit kredit
Context: Informasi tambahan - Bank dengan NPL 5%
Format: Bentuk output - Checklist 10 langkah"
```

5. Klik **Generate PTCF Prompt**
6. Tunjukkan hasil prompt yang terstruktur
7. Klik **Copy to Clipboard**

**Highlight:**
```
"Dengan PTCF, output AI menjadi lebih konsisten, relevan, dan 
sesuai dengan konteks audit. Ini membedakan AURIX dari chatbot biasa."
```

---

### 4️⃣ Risk Assessment (2 menit)

**Narasi:**
```
"Modul Risk Assessment menggunakan matriks risiko 5x5 standar 
industri untuk menilai dan memprioritaskan risiko."
```

**Demo:**
1. Klik **⚖️ Risk Assessment**
2. Tunjukkan Risk Matrix
3. Jelaskan scoring:
   - Score 15-25 = HIGH (merah)
   - Score 8-14 = MEDIUM (kuning)
   - Score 1-7 = LOW (hijau)
4. Buat assessment baru (tab New Assessment)
5. Pilih "Credit Risk" > "Loan Origination"
6. Set Likelihood: 4, Impact: 4
7. Tunjukkan risk score otomatis: 16 (HIGH)

**Highlight:**
```
"Audit Universe sudah ter-populate dengan 36 area audit dalam 
6 kategori risiko. Ini memudahkan auditor untuk konsistensi."
```

---

### 5️⃣ Findings Tracker (2 menit)

**Narasi:**
```
"Findings Tracker menggunakan metodologi 5Cs yang merupakan 
best practice dari Big 4 firms."
```

**Demo:**
1. Klik **📋 Findings Tracker**
2. Tunjukkan summary metrics (Total, Open, High Priority, Overdue)
3. Klik tab **➕ New Finding**
4. Jelaskan 5Cs:

```
"5Cs adalah:
- Condition: Fakta yang ditemukan
- Criteria: Standar yang dilanggar
- Cause: Penyebab masalah
- Consequence: Dampak jika tidak diperbaiki
- Corrective Action: Rekomendasi perbaikan"
```

5. Demo input finding singkat
6. Tunjukkan fitur AI Generate (jika waktu cukup)

**Highlight:**
```
"Dengan metodologi 5Cs, finding menjadi well-documented dan 
actionable. Ini meningkatkan kualitas laporan audit."
```

---

### 6️⃣ Continuous Audit (2 menit)

**Narasi:**
```
"Continuous Audit memungkinkan monitoring real-time dengan 
rule-based alerting."
```

**Demo:**
1. Klik **🔄 Continuous Audit**
2. Tunjukkan summary (Active Rules, New Alerts)
3. Tunjukkan Alert Dashboard dengan filter
4. Buka Rule Management
5. Jelaskan tipe rule: Threshold, Pattern, Anomaly
6. Demo create rule singkat (jika waktu)

**Highlight:**
```
"18 rule monitoring sudah pre-configured untuk skenario umum 
seperti threshold breach, unusual patterns, dan sequence detection."
```

---

### 7️⃣ KRI Dashboard (2 menit) ⭐ VISUAL

**Narasi:**
```
"KRI Dashboard memberikan visualisasi Key Risk Indicators 
dengan gauge dan trend analysis."
```

**Demo:**
1. Klik **📈 KRI Dashboard**
2. Tunjukkan summary (Total KRIs, Healthy, Warning, Breached)
3. Klik tab "Credit Risk"
4. Tunjukkan gauge visualizations
5. Jelaskan color coding:
   - Hijau: Di bawah threshold
   - Kuning: Mendekati threshold
   - Merah: Melebihi threshold
6. Pilih KRI untuk trend analysis
7. Tunjukkan 12-month trend chart

**Highlight:**
```
"20+ KRI dipantau secara real-time dalam 6 kategori. 
Visual gauge memudahkan identifikasi masalah sekilas."
```

---

### 8️⃣ Fraud Detection (2 menit)

**Narasi:**
```
"Modul Fraud Detection membantu identifikasi red flags 
dan manajemen kasus investigasi."
```

**Demo:**
1. Klik **🔍 Fraud Detection**
2. Tunjukkan Red Flag Scanner
3. Demo checklist red flags
4. Tunjukkan risk score calculation
5. Buka Case Management
6. Tunjukkan Red Flag Library (60+ flags dalam 5 kategori)

**Highlight:**
```
"Red Flag Library berisi 60+ indikator fraud yang umum 
di industri keuangan, dikategorikan dalam 5 area."
```

---

### 9️⃣ Regulatory Compliance (2 menit)

**Narasi:**
```
"Modul Regulatory Compliance tracking membantu memantau 
kepatuhan terhadap regulasi OJK, BI, dan standar ISO."
```

**Demo:**
1. Klik **📚 Regulations**
2. Tunjukkan summary (Total Regulations, Compliant %)
3. Buka tab OJK atau BI
4. Tunjukkan compliance cards dengan score gauge
5. Buka Calendar untuk upcoming reviews

**Highlight:**
```
"13 regulasi kunci sudah ter-track dengan status kepatuhan 
dan jadwal review. Tidak ada lagi miss review deadline."
```

---

### 🔟 AI Chat (2 menit)

**Narasi:**
```
"AI Chat adalah asisten cerdas yang memahami konteks audit. 
Bisa menjawab pertanyaan, generate dokumen, dan analisis risiko."
```

**Demo:**
1. Klik **🤖 AI Chat**
2. Pilih Persona: "Internal Audit Manager"
3. Pilih Context: Audit Area = "Credit Risk"
4. Ketik pertanyaan:
   ```
   "Apa saja prosedur audit untuk loan origination?"
   ```
5. Tunjukkan respons AI

**Highlight:**
```
"AI memahami konteks audit dan regulasi Indonesia. 
Gunakan bersama PTCF Builder untuk hasil terbaik."
```

---

### 1️⃣1️⃣ Analytics (1 menit)

**Narasi:**
```
"Analytics memberikan insights tentang performa audit 
dan trend finding."
```

**Demo:**
1. Klik **📊 Analytics**
2. Tunjukkan Performance tab
3. Tunjukkan Coverage analysis
4. Tunjukkan Trend charts

---

### Closing (1 menit)

```
"Demikian demo AURIX - platform yang menggabungkan best practices 
audit dengan kekuatan AI.

Keunggulan AURIX:
✅ Metodologi McKinsey & Big 4
✅ AI-powered dengan free providers
✅ Regulasi Indonesia built-in
✅ Enterprise-grade UI
✅ Open source dan customizable

Terima kasih. Ada pertanyaan?"
```

---

## 💡 Tips Demo

### Do's ✅

1. **Gunakan dark mode** - Lebih profesional
2. **Siapkan data sample** - Jangan demo dengan blank screen
3. **Highlight visual** - KRI gauges, Risk Matrix, Charts
4. **Jelaskan value** - Bukan fitur, tapi manfaat
5. **Interaktif** - Ajak audience bertanya

### Don'ts ❌

1. Jangan baca dari script - Natural conversation
2. Jangan terlalu teknis - Sesuaikan audience
3. Jangan terburu-buru - Beri waktu audience memahami
4. Jangan skip error - Handle dengan elegan
5. Jangan lupakan closing - CTA yang jelas

---

## 🔄 Backup Plans

### Jika AI tidak respond:
```
"Untuk demo ini kita menggunakan mock mode. Dalam produksi, 
AI akan memberikan respons real-time dengan provider seperti 
Groq atau Google Gemini."
```

### Jika data kosong:
```
"Ini adalah fresh installation. Dalam penggunaan nyata, 
data akan ter-populate dari aktivitas audit sehari-hari."
```

### Jika ada error:
```
"Ini adalah development version. Error ini sudah 
ter-log dan akan diperbaiki. Mari lanjutkan demo..."
```

---

## 📊 Sample Data untuk Demo

### Sample Finding
```
Title: Inadequate Credit Documentation
Area: Credit Risk > Loan Origination
Severity: HIGH
Condition: 35% of sampled loan files missing required documents
Criteria: Credit Policy Section 4.2 requires complete documentation
Cause: No checklist verification before approval
Consequence: Potential loan losses of Rp 5B
Corrective Action: Implement mandatory checklist with system enforcement
```

### Sample KRI Values
```
NPL Ratio: 4.94% (Threshold: 5%)
LCR: 115.2% (Threshold: 100%)
NSFR: 108.5% (Threshold: 100%)
System Downtime: 2.3 hours (Threshold: 4 hours)
Fraud Cases: 3 (Threshold: 0)
```

### Sample Risk Assessment
```
Area: Credit Risk > Loan Monitoring
Likelihood: 4 (Likely)
Impact: 4 (Major)
Risk Score: 16 (HIGH)
Controls: Monthly portfolio review, Early warning system
Gap: Quarterly review instead of monthly
```

---

## 📝 Q&A Preparation

### Pertanyaan Umum

**Q: Apakah data aman?**
```
A: AURIX bisa di-deploy on-premise. Tidak ada data yang 
dikirim ke cloud kecuali ke LLM provider yang dipilih.
```

**Q: Berapa biaya?**
```
A: Platform gratis dan open source. LLM menggunakan 
free providers seperti Groq, Together AI, atau Google.
```

**Q: Bisa integrasi dengan sistem existing?**
```
A: Ya, AURIX berbasis Python dengan API yang bisa 
dikustomisasi untuk integrasi dengan core banking atau ERP.
```

**Q: Butuh training khusus?**
```
A: User manual lengkap tersedia. Interface dirancang 
intuitif untuk auditor. Training 2-4 jam cukup.
```

**Q: Support regulasi terbaru?**
```
A: Regulasi bisa di-update melalui seed data. 
Tim development bisa membantu update berkala.
```

---

**Happy Demo! 🎉**

*© 2025 MS Hadianto - AURIX Platform*
