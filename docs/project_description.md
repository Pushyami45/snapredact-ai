# SnapRedact AI — Brief Project Description

## Project Title
**SnapRedact AI — On-Device PII Redaction & Document Privacy Tool**

## Overview
SnapRedact AI is an on-device AI-powered application that automatically detects and redacts Personally Identifiable Information (PII) from documents — including text files, PDFs, images, and DOCX files. Built specifically for Snapdragon-powered HP PCs, all processing occurs entirely on-device using the Snapdragon NPU, ensuring that sensitive data never leaves the user's laptop.

## Problem
Organizations across sectors — healthcare, finance, education, HR — handle sensitive documents daily. Before these documents can be shared, PII such as names, Aadhaar numbers, PAN numbers, email addresses, and phone numbers must be identified and removed. Current redaction solutions either:
- Send data to cloud servers, creating significant privacy and compliance risks
- Require tedious manual redaction, which is slow and error-prone

This is particularly critical in India where the Digital Personal Data Protection Act (DPDPA 2023) mandates strict handling of personal data.

## Solution
SnapRedact AI combines two complementary AI approaches:

1. **AI-Based Named Entity Recognition (NER)**: A BERT model (`dslim/bert-base-NER`) running through ONNX Runtime detects context-dependent PII — person names, organizations, and locations — by understanding natural language context.

2. **Intelligent Pattern Matching**: Compiled regex patterns detect India-specific structured PII (Aadhaar: 12-digit format, PAN: ABCDE1234F format) and universal identifiers (emails, phone numbers, credit cards, IP addresses, dates of birth).

3. **OCR Integration**: Tesseract OCR with image preprocessing extracts text from scanned documents and images, enabling PII detection even in non-digital documents.

## Snapdragon Optimization
- **NPU Acceleration**: ONNX Runtime leverages the Snapdragon Neural Processing Unit for efficient BERT model inference
- **100% On-Device**: Zero network dependency — works in airplane mode, in remote areas, anywhere
- **Low Latency**: NPU-accelerated inference provides near real-time PII detection
- **Model Caching**: `@st.cache_resource` ensures the model loads once and persists across sessions for instant subsequent operations

## Technical Stack
- Python 3.11+ with Streamlit web framework
- Hugging Face Transformers (BERT NER) + ONNX Runtime
- Tesseract OCR + PIL for image processing
- PyMuPDF for PDF handling
- python-docx for DOCX support

## Key Features
- Detects 11+ types of PII including India-specific identifiers
- Supports text, PDF, DOCX, and image file formats
- OCR for scanned documents
- Side-by-side original vs. redacted view
- Export as TXT, DOCX, or JSON detection report
- Beautiful, interactive Streamlit dashboard with real-time statistics

## Impact
SnapRedact AI demonstrates how on-device AI on Snapdragon-powered PCs can solve a real-world privacy challenge — enabling organizations to comply with data protection regulations while keeping sensitive data completely private and secure.

---
*Author: A V U Pushyami Reddy | pushyamireddy4533@gmail.com*
*Built for the Snapdragon® AI Lab Build & Present Challenge 2026*
