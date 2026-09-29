"""
╔══════════════════════════════════════════════════════════════╗
║                        APP.PY                                ║
║           SnapRedact AI — Main Streamlit Application         ║
╚══════════════════════════════════════════════════════════════╝

This is the MAIN FILE of SnapRedact AI — the entry point.
Run with: streamlit run app.py

WHAT THIS FILE DOES:
1. Creates a beautiful, modern web interface using Streamlit
2. Handles file uploads (text, images, PDFs, DOCX)
3. Orchestrates the PII detection + redaction pipeline
4. Displays results with visual highlighting
5. Provides redacted document download

ARCHITECTURE:
┌─────────────────────────────────────────────┐
│              Streamlit UI (app.py)           │
│  ┌─────────┐  ┌──────────┐  ┌───────────┐  │
│  │ Upload  │→ │ Process  │→ │ Display   │  │
│  │ File    │  │ File     │  │ Results   │  │
│  └─────────┘  └──────────┘  └───────────┘  │
│       │            │                         │
│       ▼            ▼                         │
│  ┌─────────┐  ┌──────────────┐              │
│  │ utils.py│  │ redactor.py  │              │
│  │ (file   │  │ (NER+Regex)  │              │
│  │  I/O)   │  │              │              │
│  └─────────┘  └──────────────┘              │
│                    │                         │
│               ┌────┴────┐                    │
│               │ocr_engine│                   │
│               │  (.py)   │                   │
│               └─────────┘                    │
└─────────────────────────────────────────────┘
"""

import streamlit as st
from PIL import Image
import io

# ═══════════════════════════════════════════════
# PAGE CONFIGURATION
# Must be the FIRST Streamlit command in the file
# ═══════════════════════════════════════════════
st.set_page_config(
    page_title="SnapRedact AI — On-Device PII Redaction",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════
# CUSTOM CSS — Making the UI look premium
# ═══════════════════════════════════════════════
st.markdown("""
<style>
    /* ── Main App Theme ── */
    .main {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
    }

    /* ── Header Styling ── */
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00d2ff 0%, #7b2ff7 50%, #ff0080 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
        letter-spacing: -1px;
    }
    .hero-subtitle {
        text-align: center;
        color: #8892b0;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        margin-bottom: 2rem;
    }

    /* ── Stat Cards ── */
    .stat-card {
        background: linear-gradient(135deg, #1e1e30 0%, #2a2a40 100%);
        border: 1px solid rgba(123, 47, 247, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(123, 47, 247, 0.2);
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: #7b2ff7;
    }
    .stat-label {
        color: #8892b0;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }

    /* ── PII Entity Tags ── */
    .pii-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 3px;
    }
    .pii-tag-name { background: rgba(255, 0, 128, 0.2); color: #ff0080; border: 1px solid #ff0080; }
    .pii-tag-email { background: rgba(0, 210, 255, 0.2); color: #00d2ff; border: 1px solid #00d2ff; }
    .pii-tag-phone { background: rgba(0, 255, 136, 0.2); color: #00ff88; border: 1px solid #00ff88; }
    .pii-tag-aadhaar { background: rgba(255, 165, 0, 0.2); color: #ffa500; border: 1px solid #ffa500; }
    .pii-tag-pan { background: rgba(255, 215, 0, 0.2); color: #ffd700; border: 1px solid #ffd700; }
    .pii-tag-other { background: rgba(123, 47, 247, 0.2); color: #7b2ff7; border: 1px solid #7b2ff7; }

    /* ── Badge ── */
    .snapdragon-badge {
        background: linear-gradient(135deg, #e53935 0%, #d32f2f 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }

    /* ── Feature Cards ── */
    .feature-card {
        background: rgba(30, 30, 48, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
    }

    /* ── Redacted text highlight ── */
    .redacted-highlight {
        background: rgba(229, 57, 53, 0.3);
        color: #ff6b6b;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
    }

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# CACHING: Load models once, reuse across sessions
# ═══════════════════════════════════════════════
# @st.cache_resource ensures the model is loaded ONLY ONCE
# even when multiple users access the app or the page refreshes
@st.cache_resource
def load_redactor():
    """Load the PII Redactor engine (cached for performance)."""
    from redactor import PIIRedactor
    return PIIRedactor()


@st.cache_resource
def load_ocr():
    """Load the OCR engine (cached for performance)."""
    from ocr_engine import OCREngine
    return OCREngine()


# ═══════════════════════════════════════════════
# HELPER: Get CSS class for PII type tag
# ═══════════════════════════════════════════════
def get_pii_tag_class(pii_type: str) -> str:
    """Map PII type to CSS class for colored tags."""
    type_map = {
        "Person Name": "name",
        "Email Address": "email",
        "Phone Number": "phone",
        "Aadhaar Number": "aadhaar",
        "PAN Number": "pan",
    }
    return type_map.get(pii_type, "other")


# ═══════════════════════════════════════════════
# HELPER: Process uploaded file and extract text
# ═══════════════════════════════════════════════
def process_uploaded_file(uploaded_file) -> str:
    """
    Extract text from an uploaded file based on its type.

    Supports:
    - Text files (.txt, .csv, .log, .md) → read directly
    - Images (.png, .jpg, etc.) → OCR extraction
    - PDFs (.pdf) → text extraction or OCR
    - DOCX (.docx) → XML parsing

    Args:
        uploaded_file: Streamlit UploadedFile object

    Returns: Extracted text content
    """
    from utils import get_file_type, extract_text_from_docx

    file_type = get_file_type(uploaded_file.name)

    if file_type == "text":
        # Text files — read directly
        return uploaded_file.read().decode('utf-8', errors='ignore')

    elif file_type == "image":
        # Images — use OCR
        ocr = load_ocr()
        image = Image.open(uploaded_file)
        text = ocr.extract_text_from_image_object(image)
        return text if text else "⚠️ Could not extract text from image. Ensure Tesseract OCR is installed."

    elif file_type == "pdf":
        # PDFs — try direct text extraction first (no Tesseract needed)
        try:
            import fitz  # PyMuPDF
            pdf_bytes = uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            all_text = []
            for page_num, page in enumerate(doc):
                text = page.get_text()
                if text.strip():
                    all_text.append(f"--- Page {page_num + 1} ---\n{text}")
            doc.close()
            if all_text:
                return "\n\n".join(all_text)
            # If no text found, try OCR as fallback (for scanned PDFs)
            ocr = load_ocr()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = ocr.extract_text_from_pdf_bytes(pdf_bytes)
            return text if text else "Could not extract text from PDF. It may be a scanned PDF and Tesseract OCR is not installed."
        except Exception as e:
            return f"Could not extract text from PDF: {e}"

    elif file_type == "docx":
        # DOCX — parse XML
        text = extract_text_from_docx(uploaded_file.read())
        return text if text else "⚠️ Could not extract text from DOCX."

    else:
        return "❌ Unsupported file type."


# ╔══════════════════════════════════════════════════════════════╗
# ║                    MAIN APPLICATION UI                       ║
# ╚══════════════════════════════════════════════════════════════╝

def main():
    """Main application function — builds the entire UI."""

    # ── Hero Section ──
    st.markdown('<div class="snapdragon-badge">⚡ Powered by Snapdragon NPU</div>',
                unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">🛡️ SnapRedact AI</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-subtitle">'
        'On-Device PII Redaction — Your documents never leave your laptop'
        '</p>',
        unsafe_allow_html=True
    )

    # ── Sidebar ──
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        st.markdown("---")

        # Redaction style options
        show_type = st.toggle("Show PII type labels", value=True,
                              help="Show what type of PII was redacted")
        redact_char = st.selectbox(
            "Redaction character",
            ["█████", "●●●●●", "XXXXX", "*****"],
            help="Character used to replace PII"
        )

        st.markdown("---")
        st.markdown("## 🔍 Detectable PII Types")
        pii_types = [
            "👤 Person Names", "📧 Email Addresses",
            "📱 Phone Numbers", "🆔 Aadhaar Numbers",
            "📋 PAN Numbers", "💳 Credit Cards",
            "📅 Dates of Birth", "🌐 IP Addresses",
            "🏢 Organizations", "📍 Locations",
            "🛂 Passport Numbers"
        ]
        for pii in pii_types:
            st.markdown(f"- {pii}")

        st.markdown("---")
        st.markdown("## 🏗️ Architecture")
        st.markdown("""
        ```
        Input → OCR → NER + Regex → Redact → Export
        ```
        - **NER**: BERT-based AI model
        - **Regex**: Pattern matching
        - **OCR**: Tesseract
        - **Runtime**: ONNX / Snapdragon NPU
        """)

        st.markdown("---")
        st.caption("Built for Snapdragon® AI Lab Challenge")
        st.caption("© 2026 SnapRedact AI | All processing on-device")

    # ── Main Content Area ──
    # Two input modes: File Upload or Paste Text
    tab1, tab2, tab3 = st.tabs(["📁 Upload File", "✍️ Paste Text", "🎯 Try Demo"])

    extracted_text = None

    with tab1:
        st.markdown("### Upload a document to scan for PII")
        from utils import get_supported_extensions
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=[ext.lstrip('.') for ext in get_supported_extensions()],
            help="Supported: TXT, PDF, DOCX, PNG, JPG, BMP, TIFF"
        )

        if uploaded_file:
            st.info(f"📄 **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")
            with st.spinner("🔍 Extracting text from file..."):
                extracted_text = process_uploaded_file(uploaded_file)

    with tab2:
        st.markdown("### Paste text to scan for PII")
        pasted_text = st.text_area(
            "Enter text containing PII",
            height=200,
            placeholder="Paste any text here... e.g., employee records, customer data, emails..."
        )
        if pasted_text:
            extracted_text = pasted_text

    with tab3:
        st.markdown("### Try with sample data")
        st.markdown("Click below to see SnapRedact AI in action with sample employee records.")
        if st.button("🚀 Load Sample Data", type="primary", use_container_width=True):
            from utils import get_sample_text
            extracted_text = get_sample_text()
            st.text_area("Sample Data Loaded", value=extracted_text, height=200, disabled=True)

    # ── Process and Display Results ──
    if extracted_text and extracted_text.strip():
        st.markdown("---")

        # Load the redactor
        redactor = load_redactor()

        with st.spinner("🔍 Scanning for PII using AI + Pattern Matching..."):
            # Detect PII
            entities = redactor.detect_pii(extracted_text)
            summary = redactor.get_detection_summary(entities)

            # Redact text
            redacted_text = redactor.redact_text(
                extracted_text,
                replacement=redact_char,
                show_type=show_type
            )

        # ── Statistics Cards ──
        st.markdown("## 📊 Detection Results")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{summary['total_count']}</div>
                <div class="stat-label">Total PII Found</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{summary['by_source'].get('NER', 0)}</div>
                <div class="stat-label">AI Detected</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{summary['by_source'].get('REGEX', 0)}</div>
                <div class="stat-label">Pattern Detected</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(summary['by_type'])}</div>
                <div class="stat-label">PII Categories</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")

        # ── Detected Entities Detail ──
        if entities:
            with st.expander("🔎 View Detected Entities", expanded=True):
                # Show PII type tags
                tags_html = ""
                for pii_type, count in summary['by_type'].items():
                    tag_class = get_pii_tag_class(pii_type)
                    tags_html += f'<span class="pii-tag pii-tag-{tag_class}">{pii_type}: {count}</span> '
                st.markdown(tags_html, unsafe_allow_html=True)

                st.markdown("")

                # Detailed entity table
                entity_data = []
                for ent in summary['entities']:
                    entity_data.append({
                        "🏷️ Type": ent['type'],
                        "📝 Text": ent['text'],
                        "🎯 Confidence": f"{ent['confidence']:.0%}",
                        "🔧 Source": ent['source'],
                        "📍 Position": ent['position']
                    })
                st.dataframe(entity_data, use_container_width=True)

        # ── Side-by-side comparison ──
        st.markdown("## 📄 Original vs Redacted")
        col_orig, col_redact = st.columns(2)

        with col_orig:
            st.markdown("### 📋 Original Text")
            st.text_area(
                "Original",
                value=extracted_text,
                height=400,
                disabled=True,
                label_visibility="collapsed"
            )

        with col_redact:
            st.markdown("### 🛡️ Redacted Text")
            st.text_area(
                "Redacted",
                value=redacted_text,
                height=400,
                disabled=True,
                label_visibility="collapsed"
            )

        # ── Download Options ──
        st.markdown("## 💾 Export Redacted Document")
        col_dl1, col_dl2, col_dl3 = st.columns(3)

        with col_dl1:
            st.download_button(
                label="📄 Download as TXT",
                data=redacted_text,
                file_name="redacted_document.txt",
                mime="text/plain",
                use_container_width=True
            )

        with col_dl2:
            from utils import create_redacted_docx
            docx_bytes = create_redacted_docx(extracted_text, redacted_text)
            if docx_bytes:
                st.download_button(
                    label="📝 Download as DOCX",
                    data=docx_bytes,
                    file_name="redacted_document.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )

        with col_dl3:
            # Export detection report as JSON
            import json
            report_json = json.dumps(summary, indent=2)
            st.download_button(
                label="📊 Download Report (JSON)",
                data=report_json,
                file_name="pii_detection_report.json",
                mime="application/json",
                use_container_width=True
            )

    # ── Footer ──
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #4a4a6a; padding: 2rem 0;">
        <p style="font-size: 0.9rem;">
            🛡️ <strong>SnapRedact AI</strong> — All processing happens on-device using Snapdragon NPU
        </p>
        <p style="font-size: 0.8rem;">
            No data is transmitted to any server • Built with Qualcomm AI Hub • Optimized for Snapdragon-powered HP PCs
        </p>
        <p style="font-size: 0.75rem; color: #3a3a5a;">
            Built for the Snapdragon® AI Lab Build & Present Challenge 2026
        </p>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════
if __name__ == "__main__":
    main()
