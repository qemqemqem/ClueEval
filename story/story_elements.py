import json

from story.evidence import StoryElement, TypeOfEvidence, WhenInTime
from utils.gpt import prompt_completion_json
import json


def convert_story_to_story_elements(story: str) -> list[StoryElement]:
    prompt = f"""
    Convert the following story into a list of story elements. Each element should be a single fact or event from the story, classified according to its relevance to the mystery and when it occurred in relation to the crime.

    Story:
    {story}

    Please return a JSON array of objects with the following structure:
    [
        {{
            "text": "The fact or event from the story",
            "type_of_evidence": "supports_guilt" | "proves_guilt" | "supports_innocence" | "proves_innocence",
            "target": "The name of the character whose guilt or innocence is being supported or proven. This must be a character named or clearly identified in the story.",
            "when": "before_crime" | "during_crime" | "after_crime"
        }}
    ]

    Classify each element based on how it relates to solving the mystery:
    - "supports_guilt": Suggests but doesn't prove someone's guilt (most common)
    - "proves_guilt": Provides definitive proof of guilt
    - "supports_innocence": Suggests but doesn't prove someone's innocence
    - "proves_innocence": Provides definitive proof of innocence

    The "target" should be the name of the character whose guilt or innocence is being supported by this piece of evidence.

    The "when" field should indicate when the event occurred or the detail was revealed in relation to the crime:
    - "before_crime": If the event happened before the crime (most common)
    - "during_crime": If the event happened during the crime
    - "after_crime": If the event happened after the crime

    If an element doesn't clearly fit into these categories or doesn't have a clear target, omit it from the results.
    """

    json_response = prompt_completion_json([{"role": "user", "content": prompt}])

    if json_response:
        try:
            story_elements = []

            elements = json.loads(json_response)
            if "story_elements" in elements:
                elements = elements["story_elements"]
            for elem in elements:
                text = elem['text']
                type_of_evidence = TypeOfEvidence(elem['type_of_evidence'])
                target = elem['target']
                when = WhenInTime(elem['when'])
                story_elements.append(StoryElement(text=text, type_of_evidence=type_of_evidence, target=target, when=when))

            return story_elements
        except json.JSONDecodeError:
            print("Error: Invalid JSON response")
        except KeyError:
            print("Error: JSON response missing required keys")
        except ValueError:
            print("Error: Invalid type_of_evidence or when value")

    return []


def generate_innocuous_details(story: str, central_character: str) -> list[StoryElement]:
    prompt = f"""
Given the following story, generate 5 innocuous details that don't suggest or prove anything about the crime. These should be minor, unrelated facts that add color to the story but aren't relevant to solving the mystery. Also, indicate when each detail occurred in relation to the crime.

Story:
{story}

Provide the output as a JSON array of objects, where each object has a 'text' field for the innocuous detail and a 'when' field indicating when it occurred.

Example:

```json
{{
    "details": [
        {{"text": "When the detective arrived, it was raining.", "when": "after_crime"}},
        {{"text": "The hot dog stand had a sign that said 'Best in Town'.", "when": "before_crime"}},
    ]
}}

Innocuous details never introduce a new character or location, and they don't involve any significant actions or events related to the crime. They should be simple, everyday observations or background information that doesn't affect the mystery.
""".strip()
    
    response = prompt_completion_json([{"role": "user", "content": prompt}])
    # print(response)
    try:
        details = json.loads(response)
        if "details" in details:
            details = details["details"]
        # print(details)
        return [
            StoryElement(
                text=detail['text'],
                target=central_character,
                type_of_evidence=TypeOfEvidence.INNOCUOUS,
                when=WhenInTime(detail['when'])
            )
            for detail in details
        ]
    except json.JSONDecodeError:
        print("Error decoding JSON response for innocuous details")
        return []
