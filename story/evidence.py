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
    concealed: bool = False  # True if it's an element that shows up in the true story, False if it's in the story told to the detective

    def __str__(self):
        concealed_txt = "[CONCEALED] " if self.concealed else ""
        if self.type_of_evidence == TypeOfEvidence.NARRATIVE:
            return f"{concealed_txt}[{self.when.name.upper()}]\t{self.text}"
        me_txt = f"{self.murder_element.name} -- " if self.murder_element else ""
        return f"{concealed_txt}[{self.when.name.upper()}]\t{self.text} ({me_txt}{self.type_of_evidence.name} for {self.target})"

    def __post_init__(self):
        if self.type_of_evidence == TypeOfEvidence.NARRATIVE:
            self.target = ""
            self.speaker = ""
            self.when = WhenInTime.NARRATIVE
            self.murder_element = None
            self.concealed = False
