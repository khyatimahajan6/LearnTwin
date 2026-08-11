from typing import List, Optional

from pydantic import BaseModel


class MediaUploadResponse(BaseModel):
    lecture_id: str
    source: str
    document_text: Optional[str]
    transcript: str
    timestamps: List[dict]
    combined_text: str
