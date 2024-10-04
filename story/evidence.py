from dataclasses import dataclass

from enum import Enum, auto

class TypeOfEvidence(Enum):
    SUGGESTS_GUILT = "supports_guilt"
    PROVES_GUILT = "proves_guilt"
    SUGGESTS_INNOCENCE = "supports_innocence"
    PROVES_INNOCENCE = "proves_innocence"

@dataclass
class StoryElement:
    # This replaces the BulletPoint class from story/bullet_classifier.py
    text: str
    type_of_evidence: TypeOfEvidence
