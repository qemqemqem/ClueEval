import logging
from dataclasses import dataclass, field
from typing import List, Dict
import json

from utils.gpt import prompt_completion_json
from utils.display_interface import display_story_element, display_narrative, display_bullet_points, display_error, \
    display_json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EvidenceCategories:
    proves: List[str] = field(default_factory=list)
    suggests: List[str] = field(default_factory=list)
    suggests_against: List[str] = field(default_factory=list)
    proves_against: List[str] = field(default_factory=list)


@dataclass
class Hypothesis:
    name: str
    evidence: EvidenceCategories = field(default_factory=EvidenceCategories)


@dataclass
class Hypotheses:
    killers: List[Hypothesis] = field(default_factory=list)
    weapons: List[Hypothesis] = field(default_factory=list)
    locations: List[Hypothesis] = field(default_factory=list)


@dataclass
class BulletPointClassification:
    hypothesis_type: str
    hypothesis_name: str
    category: str


@dataclass
class BulletPoint:
    text: str
    classifications: List[BulletPointClassification] = field(default_factory=list)


@dataclass
class EvidenceClassification:
    classified_evidence: List[BulletPoint] = field(default_factory=list)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        evidence_classification = cls()

        for item in data['classified_evidence']:
            bullet_point = BulletPoint(text=item['text'])
            for classification in item['classifications']:
                if classification['hypothesis_type'] == 'none':
                    pass
                    # bullet_point.classifications.append(BulletPointClassification(
                    #     hypothesis_type='none',
                    #     hypothesis_name='None',
                    #     category='unrelated'
                    # ))
                else:
                    bullet_point.classifications.append(BulletPointClassification(**classification))
            evidence_classification.classified_evidence.append(bullet_point)

        return evidence_classification


def classify_evidence(bullet_points: List[str], hypotheses: Hypotheses) -> EvidenceClassification:
    logger.info("Starting evidence classification")
    # Load the prompt template
    with open('config/prompts/classify_evidence.txt', 'r') as f:
        prompt_template = f.read()

    # Prepare the prompt
    bullet_points_text = "\n".join(f"{i+1}. {point}" for i, point in enumerate(bullet_points))
    prompt = prompt_template.format(
        bullet_points=bullet_points_text,
        killers=", ".join(h.name for h in hypotheses.killers),
        weapons=", ".join(h.name for h in hypotheses.weapons),
        locations=", ".join(h.name for h in hypotheses.locations)
    )

    display_narrative(prompt, speaker="Evidence Classification Prompt")

    # Call the LLM
    messages = [{"role": "user", "content": prompt}]
    logger.info("Calling LLM for evidence classification")
    json_response = prompt_completion_json(messages)

    # Print the full JSON response
    display_json(json_response, title="Full JSON Response from LLM")

    # Parse the response
    if json_response:
        logger.info("Successfully received JSON response from LLM")
        return EvidenceClassification.from_json(json_response)
    else:
        logger.error("Failed to get a valid response from the LLM")
        raise Exception("Failed to get a valid response from the LLM")


def display_classified_evidence(evidence_classification):
    logger.info("Displaying classified evidence")
    
    classified_evidence_text = "Classified Evidence:\n\n"
    
    for i, bullet_point in enumerate(evidence_classification.classified_evidence, 1):
        classified_evidence_text += f"{i}. {bullet_point.text}\n"
        # classified_evidence_text += "   Classifications:\n"
        for c in bullet_point.classifications:
            classified_evidence_text += f"   - {c.category} {c.hypothesis_name} as {c.hypothesis_type.capitalize()}\n"
        classified_evidence_text += "\n"
        # logger.info(f"Added classifications for bullet point: {bullet_point.text[:30]}...")

    display_narrative(classified_evidence_text, speaker="Evidence Classification")
    logger.info(f"Displayed classifications for {len(evidence_classification.classified_evidence)} bullet points")


if __name__ == "__main__":
    bullet_points = [
        "John was seen near the kitchen at the time of the murder.",
        "A bloody knife was found in the bedroom.",
        "Mary has an alibi for the time of the murder."
    ]
    hypotheses = Hypotheses(
        killers=[Hypothesis("John"), Hypothesis("Mary")],
        weapons=[Hypothesis("Knife"), Hypothesis("Gun")],
        locations=[Hypothesis("Kitchen"), Hypothesis("Bedroom")]
    )

    try:
        evidence_classification = classify_evidence(bullet_points, hypotheses)
        display_classified_evidence(evidence_classification)
    except Exception as e:
        display_error(str(e))
