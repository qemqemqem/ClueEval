from dataclasses import dataclass, field
from typing import List, Dict
import json

from utils.gpt import prompt_completion_json


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
    hypotheses: Hypotheses = field(default_factory=Hypotheses)
    bullet_points: List[BulletPoint] = field(default_factory=list)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        evidence_classification = cls()

        for hypothesis_type in ['killers', 'weapons', 'locations']:
            for hyp in data['hypotheses'][hypothesis_type]:
                hypothesis = Hypothesis(hyp['name'], EvidenceCategories(**hyp['evidence']))
                getattr(evidence_classification.hypotheses, hypothesis_type).append(hypothesis)

        for bp in data['bullet_points']:
            bullet_point = BulletPoint(bp['text'])
            for classification in bp['classifications']:
                bullet_point.classifications.append(BulletPointClassification(**classification))
            evidence_classification.bullet_points.append(bullet_point)

        return evidence_classification


def classify_evidence(bullet_points: List[str], hypotheses: Hypotheses) -> EvidenceClassification:
    # Load the prompt template
    with open('config/prompts/classify_evidence.txt', 'r') as f:
        prompt_template = f.read()

    # Prepare the prompt
    prompt = prompt_template.format(
        bullet_points="\n".join(f"- {bp}" for bp in bullet_points),
        killers=", ".join(h.name for h in hypotheses.killers),
        weapons=", ".join(h.name for h in hypotheses.weapons),
        locations=", ".join(h.name for h in hypotheses.locations)
    )

    # Call the LLM
    messages = [{"role": "user", "content": prompt}]
    json_response = prompt_completion_json(messages)

    # Parse the response
    if json_response:
        return EvidenceClassification.from_json(json_response)
    else:
        raise Exception("Failed to get a valid response from the LLM")


def display_classified_evidence(evidence_classification):
    print("\n=== Classified Evidence ===")

    for hypothesis_type in ['killers', 'weapons', 'locations']:
        print(f"\n{hypothesis_type.capitalize()}:")
        for hypothesis in getattr(evidence_classification.hypotheses, hypothesis_type):
            print(f"  {hypothesis.name}:")
            for category in ['proves', 'suggests', 'suggests_against', 'proves_against']:
                if getattr(hypothesis.evidence, category):
                    print(f"    {category.replace('_', ' ').capitalize()}:")
                    for evidence in getattr(hypothesis.evidence, category):
                        print(f"      - {evidence}")

    print("\nBullet Points Classifications:")
    for bullet_point in evidence_classification.bullet_points:
        print(f"  - {bullet_point.text}")
        for classification in bullet_point.classifications:
            print(
                f"    {classification.hypothesis_type.capitalize()} ({classification.hypothesis_name}): {classification.category}")


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

    evidence_classification = classify_evidence(bullet_points, hypotheses)
    print(evidence_classification.to_json())
