"""
╔══════════════════════════════════════════════════════════════╗
║                       UTILS.PY                               ║
║              Utility Functions & Helpers                      ║
╚══════════════════════════════════════════════════════════════╝

This module provides utility functions used across the application:
- File type detection
- Text file reading
- Redacted document export
- Sample data generation for testing

These are helper functions that keep the main code clean and focused.
"""

import os
from typing import Optional, Tuple


# ═══════════════════════════════════════════════
# FILE TYPE DETECTION
# ═══════════════════════════════════════════════

# Supported file extensions grouped by type
SUPPORTED_IMAGE_TYPES = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif'}
SUPPORTED_PDF_TYPES = {'.pdf'}
SUPPORTED_TEXT_TYPES = {'.txt', '.csv', '.log', '.md', '.json', '.xml'}
SUPPORTED_DOC_TYPES = {'.docx'}


def get_file_type(filename: str) -> str:
    """
    Determine the file type category from its extension.

    Args:
        filename: Name of the file (with extension)

    Returns: One of "image", "pdf", "text", "docx", or "unsupported"
    """
    ext = os.path.splitext(filename)[1].lower()

    if ext in SUPPORTED_IMAGE_TYPES:
        return "image"
    elif ext in SUPPORTED_PDF_TYPES:
        return "pdf"
    elif ext in SUPPORTED_TEXT_TYPES:
        return "text"
    elif ext in SUPPORTED_DOC_TYPES:
        return "docx"
    else:
        return "unsupported"


def get_supported_extensions() -> list:
    """
    Get all supported file extensions as a flat list.
    Used by the Streamlit file uploader to filter files.
    """
    all_types = (
        SUPPORTED_IMAGE_TYPES |
        SUPPORTED_PDF_TYPES |
        SUPPORTED_TEXT_TYPES |
        SUPPORTED_DOC_TYPES
    )
    return sorted(list(all_types))


# ═══════════════════════════════════════════════
# TEXT EXTRACTION FROM DOCX
# ═══════════════════════════════════════════════

def extract_text_from_docx(file_bytes: bytes) -> Optional[str]:
    """
    Extract text from a .docx file.

    HOW IT WORKS:
    - .docx files are actually ZIP files containing XML
    - python-docx parses the XML and extracts paragraph text
    - We join all paragraphs with newlines

    Args:
        file_bytes: Raw bytes of the .docx file

    Returns: Extracted text, or None on failure
    """
    try:
        from docx import Document
        import io

        doc = Document(io.BytesIO(file_bytes))
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n".join(paragraphs)

    except Exception as e:
        pass  # Error reading .docx, return None
        return None


# ═══════════════════════════════════════════════
# SAMPLE DATA FOR TESTING
# ═══════════════════════════════════════════════

def get_sample_text() -> str:
    """
    Generate sample text containing various types of PII.

    This is used for:
    - Demo mode in the app
    - Testing the PII detection pipeline
    - Showing users what the tool can detect

    The sample includes Indian-specific PII (Aadhaar, PAN) and
    universal PII (email, phone, credit card, etc.)
    """
    return """
EMPLOYEE RECORD — CONFIDENTIAL

Name: Pushyami Reddy
Employee ID: EMP-2024-4533
Department: Engineering

Personal Information:
- Email: pushyami.reddy@techcorp.com
- Phone: +91-9876543210
- Alternate Phone: 040-25678901
- Date of Birth: 15/06/1998
- Address: Flat 402, Cyber Towers, Hitech City, Hyderabad, Telangana 500081

Government ID Numbers:
- Aadhaar Number: 4532 8765 1234
- PAN Number: ABCPR1234K
- Passport: J4567890

Emergency Contact:
- Name: Ravi Kumar
- Phone: +91-8765432109
- Relationship: Father
- Email: ravi.kumar@gmail.com

Bank Details:
- Account Holder: Pushyami Reddy
- Credit Card: 4111 1222 3333 4444
- IFSC: SBIN0001234

IT Information:
- Work IP: 192.168.1.105
- VPN IP: 10.0.0.42

Notes: Pushyami joined our Hyderabad office in January 2024.
Performance review scheduled for March 2025 at the Bangalore campus.
Contact HR Manager Sneha Sharma for any updates.
""".strip()


# ═══════════════════════════════════════════════
# EXPORT FUNCTIONS
# ═══════════════════════════════════════════════

def create_redacted_docx(
    original_text: str,
    redacted_text: str
) -> Optional[bytes]:
    """
    Create a .docx file containing the redacted text.

    The exported document includes:
    1. A header stating it's been redacted by SnapRedact AI
    2. The redacted text with formatting preserved
    3. A footer with detection statistics

    Args:
        original_text: The original unredacted text
        redacted_text: The redacted version

    Returns: Bytes of the .docx file, or None on failure
    """
    try:
        from docx import Document
        from docx.shared import Pt, RGBColor
        import io

        doc = Document()

        # Title
        title = doc.add_heading('Redacted Document', level=1)
        title.runs[0].font.color.rgb = RGBColor(0xE5, 0x39, 0x35)

        # Subtitle
        doc.add_paragraph(
            'Processed by SnapRedact AI — On-Device PII Redaction Tool'
        ).runs[0].font.size = Pt(10)

        doc.add_paragraph('─' * 50)

        # Redacted content
        for line in redacted_text.split('\n'):
            para = doc.add_paragraph(line)
            para.runs[0].font.size = Pt(11) if para.runs else None

        doc.add_paragraph('─' * 50)

        # Footer
        footer = doc.add_paragraph(
            '⚠️ This document has been automatically redacted. '
            'All PII has been replaced with [REDACTED] markers. '
            'Original document processed on-device — no data was transmitted.'
        )
        footer.runs[0].font.size = Pt(9)
        footer.runs[0].font.color.rgb = RGBColor(0x75, 0x75, 0x75)

        # Save to bytes
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer.getvalue()

    except Exception as e:
        pass  # Error creating .docx, return None
        return None


def format_file_size(size_bytes: int) -> str:
    """Convert bytes to human-readable file size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"
