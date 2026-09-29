"""
Script to convert the project description markdown to PDF.
Run: python generate_pdf.py

Uses markdown2 + pdfkit (or weasyprint) to create a styled PDF.
If those aren't available, creates a simple text-based PDF using reportlab.
"""

import os


def generate_pdf_from_markdown():
    """Generate project description PDF from markdown."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.colors import HexColor
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import inch
    except ImportError:
        print("Installing reportlab...")
        os.system("pip install reportlab")
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.colors import HexColor
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import inch

    output_path = os.path.join("docs", "SnapRedact_AI_Description.pdf")
    os.makedirs("docs", exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=HexColor('#7b2ff7'),
        spaceAfter=20,
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=HexColor('#1a1a2e'),
        spaceAfter=10,
        spaceBefore=16,
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        spaceAfter=8,
    )

    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        spaceAfter=4,
        leftIndent=20,
        bulletIndent=10,
    )

    elements = []

    # Title
    elements.append(Paragraph("🛡️ SnapRedact AI", title_style))
    elements.append(Paragraph(
        "On-Device PII Redaction & Document Privacy Tool",
        ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=14,
                       textColor=HexColor('#666666'), spaceAfter=20)
    ))
    elements.append(Spacer(1, 12))

    # Overview
    elements.append(Paragraph("Overview", heading_style))
    elements.append(Paragraph(
        "SnapRedact AI is an on-device AI-powered application that automatically detects and "
        "redacts Personally Identifiable Information (PII) from documents — including text files, "
        "PDFs, images, and DOCX files. Built specifically for Snapdragon-powered HP PCs, all "
        "processing occurs entirely on-device using the Snapdragon NPU, ensuring that sensitive "
        "data never leaves the user's laptop.",
        body_style
    ))
    elements.append(Spacer(1, 8))

    # Problem
    elements.append(Paragraph("Problem Statement", heading_style))
    elements.append(Paragraph(
        "Organizations across sectors — healthcare, finance, education, HR — handle sensitive "
        "documents daily. Before these documents can be shared, PII such as names, Aadhaar numbers, "
        "PAN numbers, email addresses, and phone numbers must be identified and removed.",
        body_style
    ))
    elements.append(Paragraph("Current solutions have critical limitations:", body_style))
    elements.append(Paragraph("• Cloud-based tools send data to external servers, creating privacy risks", bullet_style))
    elements.append(Paragraph("• Manual redaction is slow, expensive, and error-prone", bullet_style))
    elements.append(Paragraph("• Most tools don't support India-specific PII (Aadhaar, PAN)", bullet_style))
    elements.append(Paragraph(
        "This is particularly critical as India's Digital Personal Data Protection Act (DPDPA 2023) "
        "mandates strict handling of personal data.",
        body_style
    ))
    elements.append(Spacer(1, 8))

    # Solution
    elements.append(Paragraph("Solution", heading_style))
    elements.append(Paragraph("SnapRedact AI combines two complementary AI approaches:", body_style))
    elements.append(Paragraph(
        "• <b>AI-Based Named Entity Recognition (NER)</b>: A BERT model (dslim/bert-base-NER) "
        "running through ONNX Runtime detects context-dependent PII — person names, organizations, "
        "and locations — by understanding natural language context.",
        bullet_style
    ))
    elements.append(Paragraph(
        "• <b>Intelligent Pattern Matching</b>: Compiled regex patterns detect India-specific "
        "structured PII (Aadhaar: 12-digit format, PAN: ABCDE1234F format) and universal "
        "identifiers (emails, phone numbers, credit cards, IP addresses, dates of birth).",
        bullet_style
    ))
    elements.append(Paragraph(
        "• <b>OCR Integration</b>: Tesseract OCR with image preprocessing extracts text from "
        "scanned documents and images, enabling PII detection even in non-digital documents.",
        bullet_style
    ))
    elements.append(Spacer(1, 8))

    # Snapdragon Optimization
    elements.append(Paragraph("Snapdragon NPU Optimization", heading_style))
    elements.append(Paragraph("• NPU Acceleration: ONNX Runtime leverages Snapdragon NPU for BERT inference", bullet_style))
    elements.append(Paragraph("• 100% On-Device: Zero network dependency — works anywhere, even offline", bullet_style))
    elements.append(Paragraph("• Low Latency: NPU-accelerated inference for near real-time PII detection", bullet_style))
    elements.append(Paragraph("• Model Caching: Model loads once and persists across sessions", bullet_style))
    elements.append(Spacer(1, 8))

    # Technical Stack
    elements.append(Paragraph("Technical Stack", heading_style))
    elements.append(Paragraph("• Python 3.11+ with Streamlit web framework", bullet_style))
    elements.append(Paragraph("• Hugging Face Transformers (BERT NER) + ONNX Runtime", bullet_style))
    elements.append(Paragraph("• Tesseract OCR + PIL for image processing", bullet_style))
    elements.append(Paragraph("• PyMuPDF for PDF handling, python-docx for DOCX support", bullet_style))
    elements.append(Spacer(1, 8))

    # Key Features
    elements.append(Paragraph("Key Features", heading_style))
    elements.append(Paragraph("• Detects 11+ types of PII including India-specific identifiers", bullet_style))
    elements.append(Paragraph("• Supports text, PDF, DOCX, and image file formats", bullet_style))
    elements.append(Paragraph("• OCR for scanned documents with image preprocessing", bullet_style))
    elements.append(Paragraph("• Side-by-side original vs. redacted view", bullet_style))
    elements.append(Paragraph("• Export as TXT, DOCX, or JSON detection report", bullet_style))
    elements.append(Paragraph("• Beautiful, interactive Streamlit dashboard with real-time statistics", bullet_style))
    elements.append(Spacer(1, 8))

    # Impact
    elements.append(Paragraph("Impact", heading_style))
    elements.append(Paragraph(
        "SnapRedact AI demonstrates how on-device AI on Snapdragon-powered PCs can solve a "
        "real-world privacy challenge — enabling organizations to comply with data protection "
        "regulations (DPDPA 2023, GDPR) while keeping sensitive data completely private and secure.",
        body_style
    ))
    elements.append(Spacer(1, 20))

    # Footer
    elements.append(Paragraph(
        "Author: A V U Pushyami Reddy | pushyamireddy4533@gmail.com",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=10,
                       textColor=HexColor('#888888'))
    ))
    elements.append(Paragraph(
        "Built for the Snapdragon® AI Lab Build & Present Challenge 2026",
        ParagraphStyle('Footer2', parent=styles['Normal'], fontSize=10,
                       textColor=HexColor('#888888'))
    ))

    doc.build(elements)
    print(f"✅ Project Description PDF saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_pdf_from_markdown()
