"""
Script to generate the Pitch Presentation as PPTX file.
Run: python generate_ppt.py

This creates a professional 10-slide presentation for the
Snapdragon AI Lab Build & Present Challenge submission.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import os


def add_styled_slide(prs, title_text, content_items, is_title_slide=False):
    """Add a slide with consistent dark theme styling."""

    if is_title_slide:
        layout = prs.slide_layouts[6]  # Blank layout
    else:
        layout = prs.slide_layouts[6]  # Blank layout for full control

    slide = prs.slides.add_slide(layout)

    # Background color (dark navy)
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(0x0F, 0x0F, 0x1A)

    if is_title_slide:
        # Title slide styling
        # Main title
        txBox = slide.shapes.add_textbox(Inches(1), Inches(1.5), Inches(8), Inches(1.5))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = "🛡️ SnapRedact AI"
        p.font.size = Pt(44)
        p.font.bold = True
        p.font.color.rgb = RGBColor(0x7B, 0x2F, 0xF7)
        p.alignment = PP_ALIGN.CENTER

        # Subtitle
        p2 = tf.add_paragraph()
        p2.text = title_text
        p2.font.size = Pt(20)
        p2.font.color.rgb = RGBColor(0x88, 0x92, 0xB0)
        p2.alignment = PP_ALIGN.CENTER

        # Author info
        txBox2 = slide.shapes.add_textbox(Inches(1), Inches(3.2), Inches(8), Inches(2.2))
        tf2 = txBox2.text_frame
        tf2.word_wrap = True
        for line in content_items:
            p = tf2.add_paragraph()
            p.text = line
            p.font.size = Pt(14)
            p.font.color.rgb = RGBColor(0xA0, 0xA0, 0xC0)
            p.alignment = PP_ALIGN.CENTER

        # Snapdragon badge
        txBox3 = slide.shapes.add_textbox(Inches(1), Inches(6.0), Inches(8), Inches(0.5))
        tf3 = txBox3.text_frame
        p = tf3.paragraphs[0]
        p.text = "⚡ Powered by Snapdragon NPU | Qualcomm AI Hub"
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(0xE5, 0x39, 0x35)
        p.alignment = PP_ALIGN.CENTER
    else:
        # Regular slide
        # Title bar
        txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = RGBColor(0x7B, 0x2F, 0xF7)

        # Accent line
        line_shape = slide.shapes.add_shape(
            1, Inches(0.5), Inches(1.1), Inches(2), Pt(3)
        )
        line_shape.fill.solid()
        line_shape.fill.fore_color.rgb = RGBColor(0x7B, 0x2F, 0xF7)
        line_shape.line.fill.background()

        # Content
        txBox2 = slide.shapes.add_textbox(Inches(0.5), Inches(1.4), Inches(9), Inches(5.5))
        tf2 = txBox2.text_frame
        tf2.word_wrap = True
        for i, item in enumerate(content_items):
            p = tf2.add_paragraph()
            p.text = item
            if item.startswith("##"):
                p.text = item.replace("## ", "")
                p.font.size = Pt(18)
                p.font.bold = True
                p.font.color.rgb = RGBColor(0x00, 0xD2, 0xFF)
                p.space_before = Pt(12)
            elif item.startswith("• "):
                p.font.size = Pt(14)
                p.font.color.rgb = RGBColor(0xE0, 0xE0, 0xE0)
                p.space_before = Pt(6)
                p.level = 1
            elif item.startswith("  - "):
                p.font.size = Pt(12)
                p.font.color.rgb = RGBColor(0xA0, 0xA0, 0xC0)
                p.space_before = Pt(3)
                p.level = 2
            elif item == "---":
                p.text = ""
                p.space_before = Pt(8)
            else:
                p.font.size = Pt(14)
                p.font.color.rgb = RGBColor(0xC0, 0xC0, 0xD0)
                p.space_before = Pt(4)

    return slide


def generate_presentation():
    """Generate the full pitch deck."""
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # ══════════════════════════════════════════
    # SLIDE 1: Title
    # ══════════════════════════════════════════
    add_styled_slide(prs,
        "On-Device PII Redaction & Document Privacy Tool",
        [
            "A V U Pushyami Reddy",
            "pushyamireddy4533@gmail.com",
            "",
            "Snapdragon® AI Lab Build & Present Challenge 2026"
        ],
        is_title_slide=True
    )

    # ══════════════════════════════════════════
    # SLIDE 2: The Problem
    # ══════════════════════════════════════════
    add_styled_slide(prs, "📋 The Problem", [
        "## The PII Challenge",
        "• Organizations handle thousands of sensitive documents daily",
        "  - Employee records, customer data, medical forms, financial docs",
        "---",
        "• Before sharing, PII must be identified and removed",
        "---",
        "## Current Solutions Have Critical Flaws",
        "• ☁️  Cloud-based tools → Data leaves your device → Privacy risk",
        "• ✋  Manual redaction → Slow, expensive, error-prone",
        "• 🇮🇳  Most tools don't support Indian PII (Aadhaar, PAN)",
        "---",
        "India's DPDPA 2023 mandates strict personal data handling."
    ])

    # ══════════════════════════════════════════
    # SLIDE 3: Our Solution
    # ══════════════════════════════════════════
    add_styled_slide(prs, "🛡️ Our Solution: SnapRedact AI", [
        "## AI-powered PII detection & redaction — 100% on your Snapdragon laptop",
        "---",
        "• 🔒  Zero data leakage — nothing leaves your device",
        "• 🤖  Dual AI engine — BERT NER + Smart Regex patterns",
        "• 🇮🇳  India-first — detects Aadhaar, PAN, Indian phone numbers",
        "• 📄  Multi-format — handles TXT, PDF, DOCX, PNG, JPG files",
        "• ⚡  Fast — Snapdragon NPU-accelerated inference",
        "• 🖼️  OCR — reads scanned documents and images",
        "• 📊  Visual dashboard with real-time detection statistics",
        "• 💾  Export redacted docs in multiple formats"
    ])

    # ══════════════════════════════════════════
    # SLIDE 4: Architecture
    # ══════════════════════════════════════════
    add_styled_slide(prs, "🏗️ How It Works", [
        "## Pipeline: Document → Text → PII Detection → Redaction → Export",
        "---",
        "## Two Detection Methods Combined:",
        "---",
        "• 🤖  BERT NER (AI Model) — dslim/bert-base-NER",
        "  - Understands language context",
        "  - Detects: Person Names, Organizations, Locations",
        "  - Confidence scores for each detection",
        "---",
        "• 🔍  Regex Pattern Engine",
        "  - Matches structured PII formats",
        "  - Detects: Aadhaar, PAN, Email, Phone, Credit Card, DOB, IP",
        "---",
        "Results merged and deduplicated for comprehensive coverage"
    ])

    # ══════════════════════════════════════════
    # SLIDE 5: Snapdragon NPU
    # ══════════════════════════════════════════
    add_styled_slide(prs, "⚡ Snapdragon NPU Optimization", [
        "## Why On-Device AI on Snapdragon?",
        "---",
        "• ONNX Runtime → Automatically leverages Snapdragon NPU",
        "• On-device BERT inference → Zero cloud API calls",
        "• Low latency → Near real-time detection for large documents",
        "• Works completely offline → No internet dependency",
        "---",
        "## Privacy + Performance = Snapdragon's Unique Value",
        "---",
        "• Process sensitive documents on a flight ✈️",
        "• Work in remote areas with no connectivity 🏔️",
        "• Comply with data localization requirements 🔒",
        "---",
        "Model loaded once, cached across sessions for instant operations"
    ])

    # ══════════════════════════════════════════
    # SLIDE 6: Indian PII
    # ══════════════════════════════════════════
    add_styled_slide(prs, "🇮🇳 Indian PII Detection", [
        "## Built for India — 11+ PII Types Detected",
        "---",
        "• Aadhaar Number → Format: XXXX XXXX XXXX (12 digits)",
        "• PAN Number → Format: ABCDE1234F (5 letters + 4 digits + 1 letter)",
        "• Indian Phone → +91-XXXXXXXXXX, 0XX-XXXXXXXX",
        "• Indian Passport → Format: X1234567 (letter + 7 digits)",
        "---",
        "## Plus Universal PII:",
        "• Email addresses",
        "• Credit card numbers (16-digit)",
        "• Dates of birth (DD/MM/YYYY, YYYY-MM-DD)",
        "• IP Addresses (IPv4)",
        "• Organization names, Person names, Locations (via NER)"
    ])

    # ══════════════════════════════════════════
    # SLIDE 7: Technical Stack
    # ══════════════════════════════════════════
    add_styled_slide(prs, "🔧 Technical Stack", [
        "## Core AI",
        "• AI Model: BERT NER (dslim/bert-base-NER) — 110M parameters",
        "• Runtime: ONNX Runtime with Snapdragon NPU acceleration",
        "• NLP: Hugging Face Transformers library",
        "---",
        "## Document Processing",
        "• OCR: Tesseract OCR + PIL image preprocessing",
        "• PDF: PyMuPDF (text extraction + image rendering)",
        "• DOCX: python-docx (XML parsing)",
        "---",
        "## Application",
        "• UI: Streamlit (Python web framework)",
        "• Language: Python 3.11+",
        "• Deployment: pip install + streamlit run (2 commands)"
    ])

    # ══════════════════════════════════════════
    # SLIDE 8: Demo Screenshots
    # ══════════════════════════════════════════
    add_styled_slide(prs, "🖥️ Application Demo", [
        "## Beautiful, Interactive Dashboard",
        "---",
        "• 📁 Upload files via drag-and-drop or paste text directly",
        "• 📊 Real-time statistics: Total PII found, AI vs Pattern counts",
        "• 🔎 Detailed entity table with type, confidence, and source",
        "• 📄 Side-by-side: Original vs Redacted comparison",
        "• 💾 One-click export: TXT, DOCX, or JSON report",
        "---",
        "## Premium Dark Theme UI",
        "• Gradient accents and animated hover effects",
        "• Color-coded PII type tags for instant visual scanning",
        "• Responsive layout works on any screen size",
        "---",
        "(See live demo or screenshots in GitHub repository)"
    ])

    # ══════════════════════════════════════════
    # SLIDE 9: Impact & Future
    # ══════════════════════════════════════════
    add_styled_slide(prs, "🔮 Impact & Future Roadmap", [
        "## Impact",
        "• Compliance: Helps organizations comply with DPDPA 2023, GDPR",
        "• Privacy: Demonstrates on-device AI for sensitive data tasks",
        "• Accessibility: Zero cost, no cloud account, works offline",
        "---",
        "## Future Roadmap",
        "• 🖼️  Image PII redaction — visual masking on scanned documents",
        "• 🌐  Multi-language support — Hindi, Telugu, Tamil NER models",
        "• 📦  Batch processing for enterprise document workflows",
        "• 🔄  ONNX model export via Qualcomm AI Hub for direct NPU execution",
        "• 🔌  FastAPI endpoint for integration with enterprise tools",
        "• 📱  Snapdragon mobile deployment for on-the-go redaction"
    ])

    # ══════════════════════════════════════════
    # SLIDE 10: Thank You
    # ══════════════════════════════════════════
    add_styled_slide(prs,
        "Your documents, your device, your privacy.",
        [
            "A V U Pushyami Reddy",
            "pushyamireddy4533@gmail.com",
            "",
            "Snapdragon® AI Lab Build & Present Challenge 2026",
            "",
            "🛡️ SnapRedact AI — 100% On-Device PII Redaction"
        ],
        is_title_slide=True
    )

    # Save the presentation
    output_path = os.path.join("docs", "SnapRedact_AI_Pitch.pptx")
    os.makedirs("docs", exist_ok=True)
    prs.save(output_path)
    print(f"[OK] Presentation saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_presentation()
