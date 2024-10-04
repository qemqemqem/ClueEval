from dataclasses import dataclass

from enum import Enum, auto

class TypeOfEvidence(Enum):
    SUGGESTS_GUILT = "supports_guilt"
    PROVES_GUILT = "proves_guilt"
    SUGGESTS_INNOCENCE = "supports_innocence"
    PROVES_INNOCENCE = "proves_innocence"
    INNOCUOUS = "innocuous"

class WhenInTime(Enum):
    UNKNOWN = "unknown"
    BEFORE_CRIME = "before_crime"
    DURING_CRIME = "during_crime"
    AFTER_CRIME = "after_crime"

@dataclass
class StoryElement:
    text: str
    target: str
    type_of_evidence: TypeOfEvidence
    when: WhenInTime = WhenInTime.UNKNOWN
