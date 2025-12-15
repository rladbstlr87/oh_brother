import re
from pathlib import Path
from typing import Optional

from events.models import SourceDocument

try:
    from PyPDF2 import PdfReader
except ImportError:  # pragma: no cover - optional dependency guard
    PdfReader = None

try:
    import docx
except ImportError:  # pragma: no cover - optional dependency guard
    docx = None

try:
    from PIL import Image
    import pytesseract
except ImportError:  # pragma: no cover - optional dependency guard
    Image = None
    pytesseract = None


def extract_info_from_text(text: str) -> dict:
    """
    주어진 텍스트에서 이벤트 관련 정보를 추출하여 딕셔너리로 반환합니다.
    """
    extracted_data = {}
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    if not lines:
        return {}

    # 1. 제목 추출 (가장 첫 줄을 제목으로 가정)
    extracted_data["title"] = lines[0]

    # 2. 주최 교회/단체 추출 (가장 마지막 줄을 주최로 가정)
    potential_host = lines[-1]
    if "교회" in potential_host or "선교회" in potential_host:
        extracted_data["host_church_name"] = potential_host

    # 3. URL 추출 (정규표현식 활용)
    url_pattern = r"https?://[^\s/$.?#].[^\s]*"
    url_match = re.search(url_pattern, text)
    if url_match:
        extracted_data["url"] = url_match.group(0)

    # 4. 상세 설명 (전체 텍스트를 일단 저장)
    extracted_data["description"] = text

    # --- 앞으로 추가될 로직 ---
    # TODO: 날짜/시간 (start_datetime, end_datetime) 추출
    # TODO: 장소 (location) 추출
    # TODO: 강사 (speakers) 추출
    # TODO: 주제 (topic) 추출

    return extracted_data


class FileProcessor:
    """
    SourceDocument를 안전하게 읽어 텍스트를 추출하고 상태를 갱신합니다.
    필수 외부 도구(OCR 등)가 없을 수 있으므로 실패를 삼켜 두고 상태만 기록합니다.
    """

    def __init__(self, document_id: int):
        self.document_id = document_id

    def process(self) -> Optional[dict]:
        doc = SourceDocument.objects.get(id=self.document_id)
        if not doc.original_file:
            doc.status = "처리완료"
            doc.save(update_fields=["status"])
            return None

        try:
            file_path = Path(doc.original_file.path)
            text = self._extract_text(file_path)

            if text:
                doc.extracted_text = text
                parsed = extract_info_from_text(text)
            else:
                parsed = None

            doc.status = "처리완료"
            doc.save(update_fields=["extracted_text", "status"])
            return parsed
        except Exception:
            doc.status = "처리실패"
            doc.save(update_fields=["status"])
            raise

    def _extract_text(self, path: Path) -> str:
        ext = path.suffix.lower()
        if ext == ".pdf":
            return self._extract_pdf(path)
        if ext in {".txt", ".text"}:
            return path.read_text(encoding="utf-8", errors="ignore")
        if ext == ".docx":
            return self._extract_docx(path)
        if ext in {".png", ".jpg", ".jpeg", ".webp"}:
            return self._extract_image(path)
        # 기타 확장자는 현재 처리 대상에서 제외
        return ""

    def _extract_pdf(self, path: Path) -> str:
        if PdfReader is None:
            return ""
        try:
            reader = PdfReader(str(path))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            return text.strip()
        except Exception:
            return ""

    def _extract_docx(self, path: Path) -> str:
        if docx is None:
            return ""
        try:
            document = docx.Document(str(path))
            return "\n".join(p.text for p in document.paragraphs).strip()
        except Exception:
            return ""

    def _extract_image(self, path: Path) -> str:
        if Image is None or pytesseract is None:
            return ""
        try:
            with Image.open(path) as img:
                return pytesseract.image_to_string(img).strip()
        except Exception:
            return ""
