from dataclasses import dataclass
from typing import List, Optional

@dataclass
class SlideContent:
    slide_number: int
    text: List[str]
    tables: List[List[List[str]]]
    images: List[str]  # paths to extracted images

@dataclass
class Inconsistency:
    id: str
    type: str
    description: str
    slides: List[int]
    evidence: List[str]
    confidence: float
