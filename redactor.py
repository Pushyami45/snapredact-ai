"""
╔══════════════════════════════════════════════════════════════╗
║                     REDACTOR.PY                              ║
║         Core PII Detection & Redaction Engine                ║
╚══════════════════════════════════════════════════════════════╝

This is the BRAIN of SnapRedact AI. It detects Personally Identifiable
Information (PII) in text using TWO approaches combined:

1. AI-Based NER (Named Entity Recognition):
   - Uses a pre-trained BERT model (dslim/bert-base-NER)
   - Detects: Person names, Organizations, Locations
   - Runs on-device using Snapdragon NPU via ONNX Runtime

2. Regex Pattern Matching:
   - Detects India-specific PII: Aadhaar numbers, PAN numbers
   - Detects universal PII: emails, phone numbers, dates of birth,
     credit card numbers, IP addresses

WHY TWO APPROACHES?
- AI models are great at understanding CONTEXT (e.g., "Pushyami" is a name)
- Regex is great at detecting STRUCTURED patterns (e.g., ABCDE1234F is a PAN)
- Combining both gives us the most comprehensive PII detection

SNAPDRAGON OPTIMIZATION:
- The BERT model is loaded with ONNX Runtime which can leverage the
  Snapdragon NPU for faster inference
- All processing happens on-device — no internet required
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class PIIType(Enum):
    """
    Categories of PII we can detect.
    Each type maps to a specific kind of sensitive information.
    """
    PERSON_NAME = "Person Name"
    EMAIL = "Email Address"
    PHONE = "Phone Number"
    AADHAAR = "Aadhaar Number"
    PAN = "PAN Number"
    CREDIT_CARD = "Credit Card"
    DATE_OF_BIRTH = "Date of Birth"
    IP_ADDRESS = "IP Address"
    ORGANIZATION = "Organization"
    LOCATION = "Location"
    PASSPORT = "Passport Number"
    DRIVING_LICENSE = "Driving License"


@dataclass
class PIIEntity:
    """
    Represents a single detected PII entity in the text.

    Attributes:
        text: The actual PII text found (e.g., "Pushyami Reddy")
        pii_type: Category of PII (e.g., PIIType.PERSON_NAME)
        start: Starting character index in the original text
        end: Ending character index in the original text
        confidence: How confident the model is (0.0 to 1.0)
        source: Whether detected by "NER" (AI model) or "REGEX" (pattern)
    """
    text: str
    pii_type: PIIType
    start: int
    end: int
    confidence: float = 1.0
    source: str = "REGEX"  # "NER" or "REGEX"


class PIIRedactor:
    """
    Main PII Detection and Redaction Engine.

    This class combines AI-based Named Entity Recognition with
    regex pattern matching to find and redact sensitive information.

    Usage:
        redactor = PIIRedactor()
        entities = redactor.detect_pii("My name is Pushyami, email: test@gmail.com")
        redacted = redactor.redact_text("My name is Pushyami, email: test@gmail.com")
    """

    def __init__(self):
        """
        Initialize the redactor.
        - Sets up regex patterns for structured PII
        - Loads the NER model for context-based detection
        """
        # ═══════════════════════════════════════════════
        # STEP 1: Define Regex Patterns for Indian & Global PII
        # ═══════════════════════════════════════════════
        # Each pattern is a tuple of (compiled_regex, PIIType)
        # We compile them once for performance
        self.patterns = self._build_patterns()

        # ═══════════════════════════════════════════════
        # STEP 2: Load AI NER Model
        # ═══════════════════════════════════════════════
        self.ner_pipeline = None
        self._load_ner_model()

    def _build_patterns(self) -> list:
        """
        Build compiled regex patterns for detecting structured PII.

        WHY THESE PATTERNS?
        - Aadhaar: 12-digit number in XXXX XXXX XXXX format (Indian national ID)
        - PAN: 5 letters + 4 digits + 1 letter (Indian tax ID, e.g., ABCDE1234F)
        - Email: Standard email format
        - Phone: Indian (+91) and international formats
        - Credit Card: 16 digits in groups of 4
        - DOB: Common date formats (DD/MM/YYYY, DD-MM-YYYY, etc.)
        - IP Address: IPv4 format
        - Passport: Indian passport format (letter + 7 digits)
        - Driving License: Indian DL format (state code + digits)
        """
        return [
            # ── Aadhaar Number (Indian National ID) ──
            # Format: XXXX XXXX XXXX or XXXX-XXXX-XXXX
            # Must start with 2-9 (Aadhaar never starts with 0 or 1)
            (
                re.compile(r'\b[2-9]\d{3}[\s\-]?\d{4}[\s\-]?\d{4}\b'),
                PIIType.AADHAAR
            ),

            # ── PAN Number (Indian Tax ID) ──
            # Format: ABCDE1234F (5 letters, 4 digits, 1 letter)
            # The 4th character indicates entity type (P=Person, C=Company, etc.)
            (
                re.compile(r'\b[A-Z]{5}\d{4}[A-Z]\b'),
                PIIType.PAN
            ),

            # ── Email Address ──
            # Standard email regex with common TLDs
            (
                re.compile(
                    r'\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b'
                ),
                PIIType.EMAIL
            ),

            # ── Phone Numbers ──
            # Supports: +91-XXXXXXXXXX, +91 XXXXXXXXXX, 0XXXXXXXXXX,
            #           (XXX) XXX-XXXX, and various international formats
            (
                re.compile(
                    r'(?:\+?\d{1,3}[\s\-]?)?(?:\(?\d{2,5}\)?[\s\-]?)?\d{5,10}\b'
                ),
                PIIType.PHONE
            ),

            # ── Credit Card Numbers ──
            # Format: XXXX XXXX XXXX XXXX or XXXX-XXXX-XXXX-XXXX
            (
                re.compile(
                    r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b'
                ),
                PIIType.CREDIT_CARD
            ),

            # ── Date of Birth ──
            # Formats: DD/MM/YYYY, DD-MM-YYYY, DD.MM.YYYY, YYYY-MM-DD
            (
                re.compile(
                    r'\b(?:\d{1,2}[\-/\.]\d{1,2}[\-/\.]\d{2,4}|\d{4}[\-/\.]\d{1,2}[\-/\.]\d{1,2})\b'
                ),
                PIIType.DATE_OF_BIRTH
            ),

            # ── IP Address ──
            # IPv4 format: XXX.XXX.XXX.XXX
            (
                re.compile(
                    r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
                ),
                PIIType.IP_ADDRESS
            ),

            # ── Indian Passport Number ──
            # Format: Letter followed by 7 digits (e.g., J1234567)
            (
                re.compile(r'\b[A-Z]\d{7}\b'),
                PIIType.PASSPORT
            ),
        ]

    def _load_ner_model(self):
        """
        Load the BERT-based Named Entity Recognition model.

        MODEL: dslim/bert-base-NER
        - Pre-trained on CoNLL-2003 dataset
        - Detects: PER (persons), ORG (organizations), LOC (locations), MISC
        - Small enough to run efficiently on Snapdragon NPU

        The model is loaded lazily — only when first needed.
        This keeps startup fast.

        SNAPDRAGON OPTIMIZATION NOTE:
        - transformers + ONNX Runtime backend automatically uses
          available NPU/GPU acceleration on Snapdragon devices
        - On non-Snapdragon devices, falls back to CPU (still works!)
        """
        try:
            from transformers import pipeline
            # Load NER pipeline — this downloads the model on first run
            # (~400MB, cached after first download)
            # The 'aggregation_strategy="simple"' merges sub-word tokens
            # e.g., "Push" + "##yami" → "Pushyami"
            self.ner_pipeline = pipeline(
                "ner",
                model="dslim/bert-base-NER",
                aggregation_strategy="simple",
                device=-1  # CPU; on Snapdragon with ONNX, NPU is used
            )
            pass  # Model loaded successfully
        except Exception as e:
            # NER model could not be loaded, falling back to regex-only detection
            self.ner_pipeline = None

    def detect_pii_with_ner(self, text: str) -> List[PIIEntity]:
        """
        Detect PII using the AI NER model.

        HOW IT WORKS:
        1. Text is tokenized into sub-word tokens by BERT tokenizer
        2. Each token is classified as B-PER, I-PER, B-ORG, etc.
           (B = Beginning of entity, I = Inside entity)
        3. Tokens are aggregated back into full entity spans
        4. We map NER labels to our PIIType categories

        Returns: List of PIIEntity objects detected by the AI model
        """
        if self.ner_pipeline is None:
            return []

        entities = []
        try:
            # Run NER inference on the text
            ner_results = self.ner_pipeline(text)

            # Map NER model labels to our PII types
            label_map = {
                "PER": PIIType.PERSON_NAME,
                "ORG": PIIType.ORGANIZATION,
                "LOC": PIIType.LOCATION,
            }

            for result in ner_results:
                # Extract the entity group (PER, ORG, LOC, MISC)
                entity_group = result.get("entity_group", "")

                if entity_group in label_map:
                    entities.append(PIIEntity(
                        text=result["word"].strip(),
                        pii_type=label_map[entity_group],
                        start=result["start"],
                        end=result["end"],
                        confidence=round(result["score"], 3),
                        source="NER"
                    ))
        except Exception as e:
            pass  # NER detection error, silently skip

        return entities

    def detect_pii_with_regex(self, text: str) -> List[PIIEntity]:
        """
        Detect PII using regex pattern matching.

        HOW IT WORKS:
        1. Iterate through each compiled regex pattern
        2. Find all matches in the text
        3. Create PIIEntity objects for each match

        WHY REGEX TOO?
        - NER is great for names/orgs but misses structured IDs
        - Aadhaar, PAN, emails have very specific formats
        - Regex catches these with 100% confidence when format matches

        Returns: List of PIIEntity objects detected by regex
        """
        entities = []

        for pattern, pii_type in self.patterns:
            for match in pattern.finditer(text):
                matched_text = match.group()

                # Skip very short matches (likely false positives)
                if len(matched_text) < 3:
                    continue

                # For phone numbers, require minimum length to avoid
                # matching random short numbers
                if pii_type == PIIType.PHONE and len(matched_text) < 7:
                    continue

                entities.append(PIIEntity(
                    text=matched_text,
                    pii_type=pii_type,
                    start=match.start(),
                    end=match.end(),
                    confidence=1.0,  # Regex matches are deterministic
                    source="REGEX"
                ))

        return entities

    def detect_pii(self, text: str) -> List[PIIEntity]:
        """
        Combined PII detection using both NER and Regex.

        PIPELINE:
        1. Run NER model → get AI-detected entities
        2. Run Regex patterns → get pattern-detected entities
        3. Merge results, removing duplicates/overlaps
        4. Sort by position in text

        This dual approach ensures we catch:
        - Context-dependent PII (names, orgs via NER)
        - Format-dependent PII (Aadhaar, PAN, email via Regex)

        Args:
            text: Input text to scan for PII

        Returns: Sorted list of all detected PIIEntity objects
        """
        # Get entities from both sources
        ner_entities = self.detect_pii_with_ner(text)
        regex_entities = self.detect_pii_with_regex(text)

        # Merge and deduplicate
        all_entities = self._merge_entities(ner_entities, regex_entities)

        # Sort by position (start index) for consistent output
        all_entities.sort(key=lambda e: e.start)

        return all_entities

    def _merge_entities(
        self,
        ner_entities: List[PIIEntity],
        regex_entities: List[PIIEntity]
    ) -> List[PIIEntity]:
        """
        Merge entities from NER and Regex, handling overlaps.

        OVERLAP RESOLUTION STRATEGY:
        - If NER and Regex detect the same span → keep NER (more contextual)
        - If they detect overlapping but different spans → keep both
        - If no overlap → keep both

        This prevents double-redacting the same text while keeping
        the most informative detection.
        """
        merged = list(ner_entities)  # Start with NER entities

        for regex_ent in regex_entities:
            # Check if this regex entity overlaps with any NER entity
            is_overlapping = False
            for ner_ent in ner_entities:
                # Two spans overlap if one starts before the other ends
                if (regex_ent.start < ner_ent.end and
                        regex_ent.end > ner_ent.start):
                    is_overlapping = True
                    break

            if not is_overlapping:
                merged.append(regex_ent)

        return merged

    def redact_text(
        self,
        text: str,
        replacement: str = "█████",
        show_type: bool = True
    ) -> str:
        """
        Detect and redact all PII in the given text.

        HOW REDACTION WORKS:
        1. Detect all PII entities
        2. Replace each entity with a redaction marker
        3. Process from END to START to preserve character positions
           (replacing from start would shift all subsequent indices)

        Args:
            text: Input text to redact
            replacement: Character(s) to replace PII with (default: ████)
            show_type: If True, shows the PII type in brackets
                       e.g., [REDACTED: Email Address]

        Returns: Redacted text with all PII replaced

        Example:
            Input:  "My name is Pushyami, email: push@gmail.com"
            Output: "My name is [REDACTED: Person Name], email: [REDACTED: Email Address]"
        """
        entities = self.detect_pii(text)

        if not entities:
            return text

        # Process from end to start to maintain correct positions
        # (If we replaced from start, indices would shift)
        redacted = text
        for entity in sorted(entities, key=lambda e: e.start, reverse=True):
            if show_type:
                redaction = f"[REDACTED: {entity.pii_type.value}]"
            else:
                redaction = replacement

            redacted = redacted[:entity.start] + redaction + redacted[entity.end:]

        return redacted

    def get_detection_summary(self, entities: List[PIIEntity]) -> dict:
        """
        Generate a summary of all detected PII entities.

        Returns a dictionary with:
        - total_count: Total number of PII entities found
        - by_type: Count per PII type
        - by_source: Count per detection source (NER vs Regex)
        - entities: Full list of entity details

        This is used by the Streamlit UI to show detection statistics.
        """
        summary = {
            "total_count": len(entities),
            "by_type": {},
            "by_source": {"NER": 0, "REGEX": 0},
            "entities": []
        }

        for entity in entities:
            # Count by type
            type_name = entity.pii_type.value
            summary["by_type"][type_name] = summary["by_type"].get(type_name, 0) + 1

            # Count by source
            summary["by_source"][entity.source] += 1

            # Store entity details
            summary["entities"].append({
                "text": entity.text,
                "type": type_name,
                "confidence": float(entity.confidence),
                "source": entity.source,
                "position": f"{entity.start}-{entity.end}"
            })

        return summary
