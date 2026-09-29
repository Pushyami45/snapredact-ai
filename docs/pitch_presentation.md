# SnapRedact AI — Pitch Presentation Content

*Use this content to create the PPT and PDF pitch presentation.*
*Suggested: 8-10 slides*

---

## Slide 1: Title Slide

### 🛡️ SnapRedact AI
**On-Device PII Redaction & Document Privacy Tool**

*Powered by Snapdragon NPU*

A V U Pushyami Reddy
Snapdragon® AI Lab Build & Present Challenge 2026

---

## Slide 2: The Problem

### 📋 The PII Challenge

- Organizations handle **thousands of sensitive documents** daily
  - Employee records, customer data, medical forms, financial docs
- Before sharing, **PII must be identified and removed**
- Current solutions have **critical flaws**:
  - ☁️ Cloud-based tools → **Data leaves your device** → Privacy risk
  - ✋ Manual redaction → **Slow, expensive, error-prone**
  - 🇮🇳 Most tools don't support **Indian PII** (Aadhaar, PAN)

**India's DPDPA 2023 mandates strict personal data handling.**

---

## Slide 3: Our Solution

### 🛡️ SnapRedact AI

**AI-powered PII detection & redaction that runs 100% on your Snapdragon laptop**

- 🔒 **Zero data leakage** — nothing leaves your device
- 🤖 **Dual AI engine** — BERT NER + Smart Regex
- 🇮🇳 **India-first** — detects Aadhaar, PAN, Indian phone numbers
- 📄 **Multi-format** — text, PDF, images, DOCX
- ⚡ **Fast** — NPU-accelerated inference

---

## Slide 4: How It Works

### 🏗️ Architecture

```
Document Upload → Text Extraction → PII Detection → Redaction → Export
                  (OCR if image)    (NER + Regex)
```

**Two Detection Methods:**

| Method | What it Detects | How |
|--------|----------------|-----|
| BERT NER (AI) | Names, Organizations, Locations | Understands language context |
| Regex Patterns | Aadhaar, PAN, Email, Phone, Credit Card | Matches structured formats |

**Result:** Comprehensive PII detection with near-zero false negatives

---

## Slide 5: Snapdragon NPU Optimization

### ⚡ Why Snapdragon?

- **ONNX Runtime** → Automatically leverages Snapdragon NPU
- **On-device BERT inference** → No cloud API calls needed
- **Low latency** → Near real-time detection even for large documents
- **Works offline** → Airplane mode, remote areas, anywhere

**Privacy + Performance = Snapdragon's Unique Value**

---

## Slide 6: Indian PII Detection

### 🇮🇳 Built for India

| PII Type | Format | Example |
|----------|--------|---------|
| Aadhaar | XXXX XXXX XXXX | 4532 8765 1234 |
| PAN | ABCDE1234F | ABCPR1234K |
| Indian Phone | +91-XXXXXXXXXX | +91-9876543210 |
| Passport | X1234567 | J4567890 |
| Plus | Email, Credit Card, DOB, IP Address... |

**11+ PII types detected automatically**

---

## Slide 7: Demo / Screenshots

### 🖥️ Application Interface

*(Include screenshots of):*
1. Main dashboard with file upload
2. PII detection results with stat cards
3. Side-by-side original vs. redacted comparison
4. Export options (TXT, DOCX, JSON)

---

## Slide 8: Technical Stack

### 🔧 Tech Stack

| Component | Technology |
|-----------|-----------|
| **AI Model** | BERT NER (dslim/bert-base-NER) |
| **Runtime** | ONNX Runtime + Snapdragon NPU |
| **OCR** | Tesseract + PIL preprocessing |
| **UI** | Streamlit (Python web framework) |
| **PDF** | PyMuPDF (fitz) |
| **DOCX** | python-docx |
| **Language** | Python 3.11+ |

---

## Slide 9: Impact & Future

### 🔮 Impact

- **Compliance**: Helps organizations comply with DPDPA 2023, GDPR
- **Privacy**: Demonstrates power of on-device AI for sensitive tasks
- **Accessibility**: Simple installation, no cloud account needed

### Future Roadmap
- Image PII redaction (visual masking on images)
- Multi-language support (Hindi, Telugu)
- Batch processing for enterprise use
- ONNX model export via Qualcomm AI Hub for direct NPU execution

---

## Slide 10: Thank You

### 🛡️ SnapRedact AI

**Your documents, your device, your privacy.**

- 🌐 GitHub: github.com/YOUR_USERNAME/snapredact-ai
- 📧 pushyamireddy4533@gmail.com
- 👤 A V U Pushyami Reddy

*Built with ❤️ for the Snapdragon® AI Lab Build & Present Challenge 2026*
