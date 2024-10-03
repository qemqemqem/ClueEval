import logging
from dataclasses import dataclass, field
from typing import List, Dict
import json

from utils.gpt import prompt_completion_json
from utils.display_interface import display_story_element, display_narrative, display_bullet_points, display_error

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
    id: str
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
            bullet_point = BulletPoint(id=item['id'])
            for classification in item['classifications']:
                if classification['hypothesis_type'] == 'none':
                    bullet_point.classifications.append(BulletPointClassification(
                        hypothesis_type='none',
                        hypothesis_name='None',
                        category='unrelated'
                    ))
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
    bullet_points_text = "\n".join(bullet_points)
    prompt = prompt_template.format(
        bullet_points=bullet_points_text,
        killers=", ".join(h.name for h in hypotheses.killers),
        weapons=", ".join(h.name for h in hypotheses.weapons),
        locations=", ".join(h.name for h in hypotheses.locations)
    )

    print(prompt)

    # Call the LLM
    messages = [{"role": "user", "content": prompt}]
    logger.info("Calling LLM for evidence classification")
    json_response = prompt_completion_json(messages)

    # Print the full JSON response
    display_story_element(json_response, title="Full JSON Response from LLM")

    # Parse the response
    if json_response:
        logger.info("Successfully received JSON response from LLM")
        return EvidenceClassification.from_json(json_response)
    else:
        logger.error("Failed to get a valid response from the LLM")
        raise Exception("Failed to get a valid response from the LLM")


def display_classified_evidence(evidence_classification):
    logger.info("Displaying classified evidence")
    display_story_element("Classified Evidence", title="Evidence Classification")

    for bullet_point in evidence_classification.classified_evidence:
        display_narrative(f"{bullet_point.id}", speaker="Bullet Point")
        classifications = []
        for c in bullet_point.classifications:
            classifications.append(f"{c.hypothesis_type.capitalize()} ({c.hypothesis_name}): {c.category}")
        display_bullet_points(classifications, title="Classifications")
        logger.info(f"Displayed classifications for bullet point: {bullet_point.id[:30]}...")

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
