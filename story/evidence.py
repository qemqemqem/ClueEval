from dataclasses import dataclass

from enum import Enum, auto

class TypeOfEvidence(Enum):
    SUGGESTS_GUILT = "supports_guilt"
    PROVES_GUILT = "proves_guilt"
    SUGGESTS_INNOCENCE = "supports_innocence"
    PROVES_INNOCENCE = "proves_innocence"
    INNOCUOUS = "innocuous"
    NARRATIVE = "narrative"


class WhenInTime(Enum):
    UNKNOWN = "unknown"
    NARRATIVE = "narrative"
    BEFORE_CRIME = "before_crime"
    DURING_CRIME = "during_crime"
    AFTER_CRIME = "after_crime"


class MurderElement(Enum):
    MOTIVE = "motive"
    OPPORTUNITY = "opportunity"
    MEANS = "means"


@dataclass
class StoryElement:
    text: str  # Prose
    target: str  # Who the evidence is about
    speaker: str = ""  # Whose story does this belong to?
    type_of_evidence: TypeOfEvidence = TypeOfEvidence.NARRATIVE
    when: WhenInTime = WhenInTime.UNKNOWN
    murder_element: MurderElement = None

    def __str__(self):
        if self.type_of_evidence == TypeOfEvidence.NARRATIVE:
            return f"[{self.when.name.upper()}]\t{self.text}"
        me_txt = f"{self.murder_element.name} -- " if self.murder_element else ""
        return f"[{self.when.name.upper()}]\t{self.text} ({me_txt}{self.type_of_evidence.name} for {self.target})"
