"""
╔══════════════════════════════════════════════════════════════╗
║                     OCR_ENGINE.PY                            ║
║         Optical Character Recognition Module                 ║
╚══════════════════════════════════════════════════════════════╝

This module handles extracting text from IMAGES and PDF files.

WHY OCR IS NEEDED:
- Many documents with PII are scanned images or PDFs
- PII can exist in:
  - Scanned ID cards (Aadhaar, PAN)
  - Screenshots of forms
  - Photographed documents
- We need to extract text FIRST, then detect PII in that text

PIPELINE: Image/PDF → OCR → Raw Text → PII Detection → Redaction

TOOLS USED:
- Tesseract OCR (via pytesseract) — open-source OCR engine by Google
- PyMuPDF (fitz) — for extracting text and images from PDF files
- Pillow (PIL) — for image preprocessing before OCR

SNAPDRAGON OPTIMIZATION:
- Tesseract uses CPU, but preprocessing (image enhancement) can
  leverage hardware acceleration
- For production, OCR models from Qualcomm AI Hub could replace
  Tesseract for NPU-accelerated text recognition
"""

import os
from typing import Optional
from PIL import Image


class OCREngine:
    """
    OCR Engine for extracting text from images and PDFs.

    Supports:
    - Image files: PNG, JPG, JPEG, BMP, TIFF
    - PDF files: both text-based and scanned PDFs

    Usage:
        engine = OCREngine()
        text = engine.extract_text_from_image("scan.png")
        text = engine.extract_text_from_pdf("document.pdf")
    """

    def __init__(self):
        """
        Initialize OCR engine and check for Tesseract availability.

        Tesseract must be installed separately:
        - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
        - The installer adds Tesseract to PATH automatically
        """
        self.tesseract_available = self._check_tesseract()

    def _check_tesseract(self) -> bool:
        """
        Check if Tesseract OCR is installed and accessible.

        WHY CHECK?
        - Tesseract is a system dependency (not a pip package)
        - If not installed, we gracefully degrade to text-only mode
        """
        try:
            import pytesseract
            # Try to get Tesseract version — fails if not installed
            pytesseract.get_tesseract_version()
            return True
        except Exception:
            return False

    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image to improve OCR accuracy.

        PREPROCESSING STEPS:
        1. Convert to grayscale — removes color noise
        2. Resize if too small — ensures text is large enough for OCR
        3. Enhance contrast — makes text stand out from background

        WHY PREPROCESS?
        - Raw photos/scans often have poor lighting, skew, or low contrast
        - These issues drastically reduce OCR accuracy
        - Simple preprocessing can improve accuracy by 20-40%

        Args:
            image: PIL Image object

        Returns: Preprocessed PIL Image
        """
        # Step 1: Convert to grayscale
        # Color information is irrelevant for text — grayscale is faster
        gray = image.convert('L')

        # Step 2: Resize if image is too small
        # Tesseract works best with ~300 DPI equivalent
        width, height = gray.size
        if width < 1000:
            scale_factor = 1000 / width
            new_size = (int(width * scale_factor), int(height * scale_factor))
            gray = gray.resize(new_size, Image.LANCZOS)

        # Step 3: Enhance contrast using simple thresholding
        # This makes text darker and background lighter
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(gray)
        enhanced = enhancer.enhance(2.0)  # Double the contrast

        return enhanced

    def extract_text_from_image(self, image_path: str) -> Optional[str]:
        """
        Extract text from an image file using OCR.

        PIPELINE:
        1. Open image with Pillow
        2. Preprocess for better OCR accuracy
        3. Run Tesseract OCR
        4. Return extracted text

        Args:
            image_path: Path to the image file

        Returns: Extracted text, or None if OCR fails
        """
        if not self.tesseract_available:
            return None

        try:
            import pytesseract

            # Open and preprocess the image
            image = Image.open(image_path)
            processed = self.preprocess_image(image)

            # Run Tesseract OCR
            # '--oem 3' = Use the best available OCR engine (LSTM + Legacy)
            # '--psm 6' = Assume a single uniform block of text
            text = pytesseract.image_to_string(
                processed,
                config='--oem 3 --psm 6'
            )

            return text.strip()

        except Exception as e:
            print(f"[ERROR] OCR error for image: {e}")
            return None

    def extract_text_from_image_object(self, image: Image.Image) -> Optional[str]:
        """
        Extract text from a PIL Image object (for uploaded files in Streamlit).

        Same as extract_text_from_image but takes an Image object directly
        instead of a file path.

        Args:
            image: PIL Image object

        Returns: Extracted text, or None if OCR fails
        """
        if not self.tesseract_available:
            return None

        try:
            import pytesseract

            processed = self.preprocess_image(image)
            text = pytesseract.image_to_string(
                processed,
                config='--oem 3 --psm 6'
            )
            return text.strip()

        except Exception as e:
            print(f"[ERROR] OCR error: {e}")
            return None

    def extract_text_from_pdf(self, pdf_path: str) -> Optional[str]:
        """
        Extract text from a PDF file.

        HANDLES TWO TYPES OF PDFs:
        1. Text-based PDFs (normal PDFs created digitally)
           → Text is extracted directly from the PDF structure
           → Very fast and accurate

        2. Scanned PDFs (images embedded in PDF)
           → First extracts images from each page
           → Then runs OCR on each image
           → Slower but handles physical document scans

        PIPELINE:
        1. Try direct text extraction (fast path)
        2. If no text found → extract images → run OCR (slow path)
        3. Combine text from all pages

        Args:
            pdf_path: Path to the PDF file

        Returns: Extracted text from all pages
        """
        try:
            import fitz  # PyMuPDF

            doc = fitz.open(pdf_path)
            all_text = []

            for page_num, page in enumerate(doc):
                # First try: Extract text directly
                text = page.get_text()

                if text.strip():
                    # Text-based PDF — direct extraction worked!
                    all_text.append(f"--- Page {page_num + 1} ---\n{text}")
                elif self.tesseract_available:
                    # Scanned PDF — need OCR
                    # Render PDF page to image at 300 DPI for good quality
                    pix = page.get_pixmap(dpi=300)
                    img = Image.frombytes(
                        "RGB",
                        [pix.width, pix.height],
                        pix.samples
                    )
                    ocr_text = self.extract_text_from_image_object(img)
                    if ocr_text:
                        all_text.append(
                            f"--- Page {page_num + 1} (OCR) ---\n{ocr_text}"
                        )

            doc.close()
            return "\n\n".join(all_text) if all_text else None

        except Exception as e:
            print(f"[ERROR] PDF extraction error: {e}")
            return None

    def extract_text_from_pdf_bytes(self, pdf_bytes: bytes) -> Optional[str]:
        """
        Extract text from PDF bytes (for uploaded files in Streamlit).

        Same as extract_text_from_pdf but works with raw bytes
        instead of a file path.

        Args:
            pdf_bytes: Raw bytes of the PDF file

        Returns: Extracted text from all pages
        """
        try:
            import fitz

            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            all_text = []

            for page_num, page in enumerate(doc):
                text = page.get_text()

                if text.strip():
                    all_text.append(f"--- Page {page_num + 1} ---\n{text}")
                elif self.tesseract_available:
                    pix = page.get_pixmap(dpi=300)
                    img = Image.frombytes(
                        "RGB",
                        [pix.width, pix.height],
                        pix.samples
                    )
                    ocr_text = self.extract_text_from_image_object(img)
                    if ocr_text:
                        all_text.append(
                            f"--- Page {page_num + 1} (OCR) ---\n{ocr_text}"
                        )

            doc.close()
            return "\n\n".join(all_text) if all_text else None

        except Exception as e:
            print(f"[ERROR] PDF extraction error: {e}")
            return None
