"""
Convert the pitch presentation text into a themed, aligned PDF.
Uses reportlab with styling matching the PPTX dark theme.
"""
import os

def generate_pitch_pdf():
    from reportlab.lib.pagesizes import landscape, A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.colors import HexColor, white
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas

    output_path = os.path.join("docs", "SnapRedact_AI_Pitch.pdf")
    os.makedirs("docs", exist_ok=True)

    def dark_theme_bg(canvas_obj, doc_obj):
        canvas_obj.saveState()
        canvas_obj.setFillColor(HexColor('#0F0F1A'))
        canvas_obj.rect(0, 0, landscape(A4)[0], landscape(A4)[1], stroke=0, fill=1)
        canvas_obj.restoreState()

    doc = SimpleDocTemplate(output_path, pagesize=landscape(A4),
                            rightMargin=60, leftMargin=60,
                            topMargin=50, bottomMargin=50)

    # Added explicit `leading` values to prevent text overlapping!
    title_s = ParagraphStyle('T', fontSize=40, leading=48, textColor=HexColor('#7b2ff7'),
                             alignment=1, spaceAfter=20, fontName='Helvetica-Bold')
    sub_s = ParagraphStyle('S', fontSize=18, leading=24, textColor=HexColor('#8892B0'),
                           alignment=1, spaceAfter=10)
    head_s = ParagraphStyle('H', fontSize=26, leading=32, textColor=HexColor('#7b2ff7'),
                            spaceAfter=20, spaceBefore=40, fontName='Helvetica-Bold')
    body_s = ParagraphStyle('B', fontSize=16, leading=22, textColor=HexColor('#C0C0D0'), spaceAfter=10)
    bullet_s = ParagraphStyle('BL', fontSize=15, leading=22, textColor=HexColor('#E0E0E0'), spaceAfter=8, leftIndent=25)
    subbullet_s = ParagraphStyle('SBL', fontSize=13, leading=18, textColor=HexColor('#A0A0C0'), spaceAfter=6, leftIndent=50)

    els = []

    # Slide 1
    els += [Spacer(1, 100), Paragraph("SnapRedact AI", title_s),
            Paragraph("On-Device PII Redaction &amp; Document Privacy Tool", sub_s),
            Spacer(1, 40),
            Paragraph("A V U Pushyami Reddy", sub_s),
            Paragraph("pushyamireddy4533@gmail.com", sub_s),
            Spacer(1, 15),
            Paragraph("Snapdragon AI Lab Build &amp; Present Challenge 2026", sub_s),
            Spacer(1, 30),
            Paragraph("Powered by Snapdragon NPU | Qualcomm AI Hub", ParagraphStyle('X', fontSize=12, leading=16, textColor=HexColor('#e53935'), alignment=1)),
            PageBreak()]

    # Slide 2
    els += [Paragraph("The Problem", head_s),
            Paragraph("<b>The PII Challenge</b>", ParagraphStyle('H2', fontSize=18, leading=24, textColor=HexColor('#00D2FF'), spaceAfter=10, spaceBefore=10)),
            Paragraph("- Organizations handle thousands of sensitive documents daily", bullet_s),
            Paragraph("- Employee records, customer data, medical forms, financial docs", subbullet_s),
            Spacer(1, 10),
            Paragraph("- Before sharing, PII must be identified and removed", bullet_s),
            Spacer(1, 12),
            Paragraph("<b>Current Solutions Have Critical Flaws</b>", ParagraphStyle('H2', fontSize=18, leading=24, textColor=HexColor('#00D2FF'), spaceAfter=10, spaceBefore=10)),
            Paragraph("- Cloud-based tools -> Data leaves your device -> Privacy risk", bullet_s),
            Paragraph("- Manual redaction -> Slow, expensive, error-prone", bullet_s),
            Paragraph("- Most tools don't support Indian PII (Aadhaar, PAN)", bullet_s),
            Spacer(1, 15),
            Paragraph("India's DPDPA 2023 mandates strict personal data handling.", body_s),
            PageBreak()]

    # Slide 3
    els += [Paragraph("Our Solution: SnapRedact AI", head_s),
            Paragraph("AI-powered PII detection &amp; redaction - 100% on your Snapdragon laptop", ParagraphStyle('H2', fontSize=18, leading=24, textColor=HexColor('#00D2FF'), spaceAfter=15, spaceBefore=10)),
            Paragraph("- Zero data leakage - nothing leaves your device", bullet_s),
            Paragraph("- Dual AI engine - BERT NER + Smart Regex patterns", bullet_s),
            Paragraph("- India-first - detects Aadhaar, PAN, Indian phone numbers", bullet_s),
            Paragraph("- Multi-format - handles TXT, PDF, DOCX, PNG, JPG files", bullet_s),
            Paragraph("- Fast - Snapdragon NPU-accelerated inference", bullet_s),
            Paragraph("- OCR - reads scanned documents and images", bullet_s),
            Paragraph("- Visual dashboard with real-time detection statistics", bullet_s),
            Paragraph("- Export redacted docs in multiple formats", bullet_s),
            PageBreak()]

    # Slide 4
    els += [Paragraph("How It Works", head_s),
            Paragraph("<b>Pipeline: Document -> Text -> PII Detection -> Redaction -> Export</b>", ParagraphStyle('H2', fontSize=18, leading=24, textColor=HexColor('#00D2FF'), spaceAfter=15, spaceBefore=10)),
            Paragraph("<b>Two Detection Methods Combined:</b>", body_s),
            Spacer(1, 10),
            Paragraph("- BERT NER (AI Model) - dslim/bert-base-NER", bullet_s),
            Paragraph("- Understands language context", subbullet_s),
            Paragraph("- Detects: Person Names, Organizations, Locations", subbullet_s),
            Spacer(1, 10),
            Paragraph("- Regex Pattern Engine", bullet_s),
            Paragraph("- Matches structured PII formats", subbullet_s),
            Paragraph("- Detects: Aadhaar, PAN, Email, Phone, Credit Card, DOB, IP", subbullet_s),
            Spacer(1, 10),
            Paragraph("Results merged and deduplicated for comprehensive coverage.", body_s),
            PageBreak()]

    # Slide 5
    els += [Paragraph("Snapdragon NPU Optimization", head_s),
            Paragraph("<b>Why On-Device AI on Snapdragon?</b>", ParagraphStyle('H2', fontSize=18, leading=24, textColor=HexColor('#00D2FF'), spaceAfter=10, spaceBefore=10)),
            Paragraph("- ONNX Runtime -> Automatically leverages Snapdragon NPU", bullet_s),
            Paragraph("- On-device BERT inference -> Zero cloud API calls", bullet_s),
            Paragraph("- Low latency -> Near real-time detection for large documents", bullet_s),
            Paragraph("- Works completely offline -> No internet dependency", bullet_s),
            Spacer(1, 15),
            Paragraph("<b>Privacy + Performance = Snapdragon's Unique Value</b>", ParagraphStyle('H2', fontSize=18, leading=24, textColor=HexColor('#00D2FF'), spaceAfter=10, spaceBefore=10)),
            Paragraph("- Process sensitive documents on a flight", bullet_s),
            Paragraph("- Work in remote areas with no connectivity", bullet_s),
            Paragraph("- Comply with data localization requirements", bullet_s),
            PageBreak()]

    # Slide 6
    els += [Paragraph("Indian PII Detection", head_s),
            Paragraph("<b>Built for India - 11+ PII Types Detected</b>", ParagraphStyle('H2', fontSize=18, leading=24, textColor=HexColor('#00D2FF'), spaceAfter=10, spaceBefore=10)),
            Paragraph("- Aadhaar Number -> XXXX XXXX XXXX (12 digits)", bullet_s),
            Paragraph("- PAN Number -> ABCDE1234F (5 letters + 4 digits + 1 letter)", bullet_s),
            Paragraph("- Indian Phone -> +91-XXXXXXXXXX, 0XX-XXXXXXXX", bullet_s),
            Paragraph("- Indian Passport -> X1234567 (letter + 7 digits)", bullet_s),
            Spacer(1, 15),
            Paragraph("<b>Plus Universal PII:</b>", ParagraphStyle('H2', fontSize=18, leading=24, textColor=HexColor('#00D2FF'), spaceAfter=10, spaceBefore=10)),
            Paragraph("- Email addresses, Credit card numbers (16-digit)", bullet_s),
            Paragraph("- Dates of birth (DD/MM/YYYY), IP Addresses (IPv4)", bullet_s),
            Paragraph("- Organization names, Person names, Locations (via NER)", bullet_s),
            PageBreak()]

    # Slide 7
    els += [Paragraph("Technical Stack", head_s),
            Paragraph("<b>Core AI</b>", ParagraphStyle('H2', fontSize=18, leading=24, textColor=HexColor('#00D2FF'), spaceAfter=10, spaceBefore=10)),
            Paragraph("- AI Model: BERT NER (dslim/bert-base-NER) - 110M params", bullet_s),
            Paragraph("- Runtime: ONNX Runtime with Snapdragon NPU acceleration", bullet_s),
            Paragraph("- NLP: Hugging Face Transformers library", bullet_s),
            Spacer(1, 10),
            Paragraph("<b>Document Processing</b>", ParagraphStyle('H2', fontSize=18, leading=24, textColor=HexColor('#00D2FF'), spaceAfter=10, spaceBefore=10)),
            Paragraph("- OCR: Tesseract OCR + PIL image preprocessing", bullet_s),
            Paragraph("- PDF: PyMuPDF (text extraction + image rendering)", bullet_s),
            Paragraph("- DOCX: python-docx (XML parsing)", bullet_s),
            Spacer(1, 10),
            Paragraph("<b>Application</b>", ParagraphStyle('H2', fontSize=18, leading=24, textColor=HexColor('#00D2FF'), spaceAfter=10, spaceBefore=10)),
            Paragraph("- UI: Streamlit (Python web framework)", bullet_s),
            Paragraph("- Language: Python 3.11+", bullet_s),
            Paragraph("- Deployment: pip install + streamlit run (2 commands)", bullet_s),
            PageBreak()]

    # Slide 8
    els += [Paragraph("Application Demo", head_s),
            Paragraph("<b>Beautiful, Interactive Dashboard</b>", ParagraphStyle('H2', fontSize=18, leading=24, textColor=HexColor('#00D2FF'), spaceAfter=10, spaceBefore=10)),
            Paragraph("- Upload files via drag-and-drop or paste text directly", bullet_s),
            Paragraph("- Real-time statistics: Total PII found, AI vs Pattern counts", bullet_s),
            Paragraph("- Detailed entity table with type, confidence, and source", bullet_s),
            Paragraph("- Side-by-side: Original vs Redacted comparison", bullet_s),
            Paragraph("- One-click export: TXT, DOCX, or JSON report", bullet_s),
            Spacer(1, 15),
            Paragraph("<b>Premium Dark Theme UI</b>", ParagraphStyle('H2', fontSize=18, leading=24, textColor=HexColor('#00D2FF'), spaceAfter=10, spaceBefore=10)),
            Paragraph("- Gradient accents and animated hover effects", bullet_s),
            Paragraph("- Color-coded PII type tags for instant visual scanning", bullet_s),
            Paragraph("- Responsive layout works on any screen size", bullet_s),
            Spacer(1, 10),
            Paragraph("<i>(See live demo or screenshots in GitHub repository)</i>", body_s),
            PageBreak()]

    # Slide 9
    els += [Paragraph("Impact &amp; Future Roadmap", head_s),
            Paragraph("<b>Impact</b>", ParagraphStyle('H2', fontSize=18, leading=24, textColor=HexColor('#00D2FF'), spaceAfter=10, spaceBefore=10)),
            Paragraph("- Compliance: Helps organizations comply with DPDPA 2023, GDPR", bullet_s),
            Paragraph("- Privacy: Demonstrates on-device AI for sensitive data tasks", bullet_s),
            Paragraph("- Accessibility: Zero cost, no cloud account, works offline", bullet_s),
            Spacer(1, 15),
            Paragraph("<b>Future Roadmap</b>", ParagraphStyle('H2', fontSize=18, leading=24, textColor=HexColor('#00D2FF'), spaceAfter=10, spaceBefore=10)),
            Paragraph("- Image PII redaction - visual masking on scanned documents", bullet_s),
            Paragraph("- Multi-language support - Hindi, Telugu, Tamil NER models", bullet_s),
            Paragraph("- Batch processing for enterprise document workflows", bullet_s),
            Paragraph("- ONNX model export via Qualcomm AI Hub for direct NPU execution", bullet_s),
            Paragraph("- FastAPI endpoint for integration with enterprise tools", bullet_s),
            Paragraph("- Snapdragon mobile deployment for on-the-go redaction", bullet_s),
            PageBreak()]

    # Slide 10 - Thank you
    els += [Spacer(1, 120),
            Paragraph("SnapRedact AI", title_s),
            Paragraph("Your documents, your device, your privacy.", sub_s),
            Spacer(1, 40),
            Paragraph("A V U Pushyami Reddy", sub_s),
            Paragraph("pushyamireddy4533@gmail.com", sub_s),
            Spacer(1, 20),
            Paragraph("Snapdragon AI Lab Build &amp; Present Challenge 2026", sub_s)]

    # Important: Apply the background using onFirstPage and onLaterPages
    doc.build(els, onFirstPage=dark_theme_bg, onLaterPages=dark_theme_bg)
    print(f"Pitch PDF saved to: {output_path}")

if __name__ == "__main__":
    generate_pitch_pdf()
