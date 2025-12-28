# 🚀 AURIX Installation Guide
## Quick Start untuk Windows, Mac, dan Linux

---

## 📋 Persyaratan

### Minimum
- **OS:** Windows 10+, macOS 10.15+, Ubuntu 20.04+
- **Python:** 3.10 atau lebih tinggi
- **RAM:** 4GB
- **Storage:** 500MB
- **Browser:** Chrome, Firefox, Edge (terbaru)

### Recommended
- **RAM:** 8GB+
- **Internet:** Stabil untuk akses LLM API

---

## 🪟 Windows Installation

### Step 1: Install Python

1. Download Python dari https://www.python.org/downloads/
2. Jalankan installer
3. ✅ **PENTING:** Centang "Add Python to PATH"
4. Klik "Install Now"
5. Verifikasi:
   ```cmd
   python --version
   pip --version
   ```

### Step 2: Extract dan Setup

```cmd
# Extract file zip
# Buka folder hasil extract

# Buka Command Prompt di folder tersebut
# (Shift + Right Click → Open PowerShell/Command Prompt here)

# Buat virtual environment (opsional tapi direkomendasikan)
python -m venv venv

# Aktifkan virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Jalankan Aplikasi

```cmd
streamlit run streamlit_app.py
```

Browser akan terbuka otomatis di `http://localhost:8501`

---

## 🍎 macOS Installation

### Step 1: Install Python (via Homebrew)

```bash
# Install Homebrew jika belum ada
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11

# Verifikasi
python3 --version
pip3 --version
```

### Step 2: Extract dan Setup

```bash
# Extract file zip
unzip aurix_v4.zip
cd aurix_v4

# Buat virtual environment
python3 -m venv venv

# Aktifkan virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Jalankan Aplikasi

```bash
streamlit run streamlit_app.py
```

---

## 🐧 Linux (Ubuntu/Debian) Installation

### Step 1: Install Python

```bash
# Update package list
sudo apt update

# Install Python dan pip
sudo apt install python3.11 python3.11-venv python3-pip -y

# Verifikasi
python3 --version
pip3 --version
```

### Step 2: Extract dan Setup

```bash
# Extract file zip
unzip aurix_v4.zip
cd aurix_v4

# Buat virtual environment
python3 -m venv venv

# Aktifkan virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Jalankan Aplikasi

```bash
streamlit run streamlit_app.py
```

---

## 🐳 Docker Installation (Advanced)

### Step 1: Install Docker

- Windows/Mac: https://www.docker.com/products/docker-desktop
- Linux: `sudo apt install docker.io docker-compose`

### Step 2: Build dan Run

```bash
cd aurix_v4

# Build image
docker-compose build

# Run container
docker-compose up -d

# Akses di browser
# http://localhost:8501
```

### Step 3: Stop Container

```bash
docker-compose down
```

---

## ⚙️ Konfigurasi

### Environment Variables (Opsional)

Buat file `.env` dari template:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# LLM Provider (groq, together, google, openrouter, ollama, mock)
LLM_PROVIDER=groq

# API Keys
GROQ_API_KEY=your_groq_api_key_here
TOGETHER_API_KEY=your_together_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Database (opsional)
DATABASE_URL=postgresql://user:password@localhost:5432/aurix

# App Settings
DEBUG=false
LOG_LEVEL=INFO
```

### Mendapatkan API Key Gratis

| Provider | Link | Steps |
|----------|------|-------|
| Groq | https://console.groq.com | Sign up → API Keys → Create |
| Together | https://api.together.xyz | Sign up → Settings → API Keys |
| Google | https://aistudio.google.com | Sign in → Get API Key |
| OpenRouter | https://openrouter.ai | Sign up → Keys → Create Key |

---

## 🔧 Troubleshooting

### Error: "Module not found"

```bash
# Pastikan virtual environment aktif
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Reinstall
pip install -r requirements.txt --force-reinstall
```

### Error: "Port already in use"

```bash
# Gunakan port lain
streamlit run streamlit_app.py --server.port 8502
```

### Error: "Python not found"

- Windows: Pastikan Python di-add ke PATH saat install
- Mac/Linux: Gunakan `python3` instead of `python`

### Browser tidak terbuka otomatis

Buka manual: http://localhost:8501

### AI tidak merespons

1. Buka Settings (⚙️)
2. Cek API Key sudah benar
3. Klik "Test Connection"
4. Jika gagal, coba provider lain

---

## 📱 Akses dari Device Lain

Untuk akses dari device lain dalam jaringan:

```bash
streamlit run streamlit_app.py --server.address 0.0.0.0
```

Akses dari device lain: `http://[IP_KOMPUTER]:8501`

---

## 🔄 Update Aplikasi

1. Backup folder `data/` jika ada data penting
2. Download versi baru
3. Extract ke folder baru
4. Copy file `.env` dari versi lama
5. Install dependencies lagi
6. Jalankan aplikasi

---

## 📞 Support

- **GitHub Issues:** github.com/mshadianto/aurix/issues
- **Documentation:** docs.aurix.id
- **Email:** sopian.hadianto@gmail.com

---

## ✅ Quick Verification

Setelah instalasi, pastikan:

- [ ] Aplikasi berjalan di browser
- [ ] Dapat berpindah antar menu
- [ ] Theme toggle (dark/light) berfungsi
- [ ] Tidak ada error di console

**Selamat menggunakan AURIX! 🎉**

---

*© 2025 MS Hadianto - AURIX Platform*
