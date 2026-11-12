"""
Document Ingestion Engine for HALO RAG Studio.

Enforces strict allowlist validation against data/corpus_baseline_hashes.sha256.
Guarantees 0 modifications to source knowledge files.
"""

import hashlib
import os
import re
from typing import Any, Dict, List, Optional


class DocumentMetadata:
    def __init__(
        self,
        doc_id: str,
        filename: str,
        filepath: str,
        sha256_hash: str,
        title: str,
        uuid: Optional[str] = None,
        ownership: Optional[str] = None,
        source_count: Optional[int] = None,
        verification_status: Optional[str] = None,
        category: str = "General",
        headers: Optional[List[str]] = None
    ):
        self.doc_id = doc_id
        self.filename = filename
        self.filepath = filepath
        self.sha256_hash = sha256_hash
        self.title = title
        self.uuid = uuid
        self.ownership = ownership
        self.source_count = source_count
        self.verification_status = verification_status
        self.category = category
        self.headers = headers or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "filename": self.filename,
            "filepath": self.filepath,
            "sha256_hash": self.sha256_hash,
            "title": self.title,
            "uuid": self.uuid,
            "ownership": self.ownership,
            "source_count": self.source_count,
            "verification_status": self.verification_status,
            "category": self.category,
            "headers": self.headers
        }


class IngestedDocument:
    def __init__(self, metadata: DocumentMetadata, raw_text: str):
        self.metadata = metadata
        self.raw_text = raw_text

    @property
    def filename(self) -> str:
        return self.metadata.filename

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metadata": self.metadata.to_dict(),
            "raw_text_length": len(self.raw_text)
        }


def compute_sha256(filepath: str) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


class IngestionEngine:
    """
    Ingests and validates the 15 verified notebook Markdown documents.
    """

    CATEGORY_MAP = {
        "01": "Cognitive & Neuroscience",
        "02": "Enterprise AI Transformation",
        "03": "Autonomous OS & Systems",
        "04": "Antigravity IDE & Tooling",
        "05": "Deterministic RAG Architecture",
        "06": "Behavioral Psychology",
        "07": "NotebookLM & Prompt Engineering",
        "08": "Autonomous Social Agents",
        "09": "LLM Prompting Protocols",
        "10": "Neuroplasticity & Performance",
        "11": "Spatial Computing & UI 2026",
        "12": "Deep Learning Foundations",
        "13": "Strategic Decision Making",
        "14": "Brand & Marketing Strategy",
        "15": "Strategic Communications"
    }

    def __init__(
        self,
        corpus_dir: str = ".",
        manifest_path: str = "data/corpus_baseline_hashes.sha256"
    ):
        self.corpus_dir = corpus_dir
        self.manifest_path = manifest_path
        self.baseline_hashes: Dict[str, str] = {}
        self._load_manifest()

    def _load_manifest(self) -> None:
        if not os.path.exists(self.manifest_path):
            raise FileNotFoundError(f"Baseline hash manifest not found: {self.manifest_path}")

        with open(self.manifest_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(None, 1)
                if len(parts) == 2:
                    h, name = parts
                    self.baseline_hashes[name.strip()] = h.strip()

    def verify_corpus_integrity(self) -> Dict[str, bool]:
        """
        Verifies every file in the baseline manifest against its current disk hash.
        """
        results: Dict[str, bool] = {}
        for fname, expected_hash in self.baseline_hashes.items():
            fpath = os.path.join(self.corpus_dir, fname)
            if not os.path.exists(fpath):
                results[fname] = False
                continue
            actual_hash = compute_sha256(fpath)
            results[fname] = (actual_hash == expected_hash)
        return results

    def ingest_all(self) -> List[IngestedDocument]:
        """
        Parses all allowlisted source documents, verifying checksums.
        """
        documents: List[IngestedDocument] = []
        integrity = self.verify_corpus_integrity()
        failed = [f for f, ok in integrity.items() if not ok]
        if failed:
            raise ValueError(f"Corpus integrity check failed for files: {failed}")

        for fname, expected_hash in sorted(self.baseline_hashes.items()):
            fpath = os.path.join(self.corpus_dir, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()

            prefix = fname[:2]
            category = self.CATEGORY_MAP.get(prefix, "General Knowledge")

            # Extract title
            title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else fname

            # Extract UUID
            uuid_match = re.search(r"UUID:\s*`([^`]+)`", content)
            uuid_str = uuid_match.group(1).strip() if uuid_match else None

            # Extract ownership
            owner_match = re.search(r"Vlasništvo:\s*`([^`]+)`", content)
            ownership = owner_match.group(1).strip() if owner_match else None

            # Extract headers
            headers = [h.strip() for h in re.findall(r"^#{1,3}\s+(.+)$", content, re.MULTILINE)]

            meta = DocumentMetadata(
                doc_id=prefix,
                filename=fname,
                filepath=fpath,
                sha256_hash=expected_hash,
                title=title,
                uuid=uuid_str,
                ownership=ownership,
                category=category,
                headers=headers
            )

            documents.append(IngestedDocument(metadata=meta, raw_text=content))

        return documents
