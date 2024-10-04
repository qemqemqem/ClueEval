import json

from story.evidence import StoryElement, TypeOfEvidence
from utils.gpt import prompt_completion_json
import json


def convert_story_to_story_elements(story: str) -> list[StoryElement]:
    prompt = f"""
    Convert the following story into a list of story elements. Each element should be a single fact or event from the story, classified according to its relevance to the mystery.

    Story:
    {story}

    Please return a JSON array of objects with the following structure:
    [
        {{
            "text": "The fact or event from the story",
            "type_of_evidence": "supports_guilt" | "proves_guilt" | "supports_innocence" | "proves_innocence",
            "target": "The name of the character whose guilt or innocence is being supported or proven. This must be a character named or clearly identified in the story."
        }}
    ]

    Classify each element based on how it relates to solving the mystery:
    - "supports_guilt": Suggests but doesn't prove someone's guilt
    - "proves_guilt": Provides definitive proof of guilt
    - "supports_innocence": Suggests but doesn't prove someone's innocence
    - "proves_innocence": Provides definitive proof of innocence

    The "target" should be the name of the character whose guilt or innocence is being supported by this piece of evidence.

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
                story_elements.append(StoryElement(text=text, type_of_evidence=type_of_evidence, target=target))

            return story_elements
        except json.JSONDecodeError:
            print("Error: Invalid JSON response")
        except KeyError:
            print("Error: JSON response missing required keys")
        except ValueError:
            print("Error: Invalid type_of_evidence value")

    return []


def generate_innocuous_details(story: str, central_character: str) -> list[StoryElement]:
    prompt = f"""
    Given the following story, generate 5 innocuous details that don't suggest or prove anything about the crime. These should be minor, unrelated facts that add color to the story but aren't relevant to solving the mystery.

    Story:
    {story}

    Provide the output as a JSON array of objects, where each object has a 'text' field for the innocuous detail.
    
    Example:
    
    ```json
    {{
        "details": [
            {{"text": "When the detective arrived, it was raining."}},
            {{"text": "The hot dog stand had a sign that said 'Best in Town'."}},
        ]
    }}
    """
    
    response = prompt_completion_json([{"role": "user", "content": prompt}])
    print(response)
    try:
        details = json.loads(response)
        if "details" in details:
            details = details["details"]
        print(details)
        return [
            StoryElement(
                text=detail['text'],
                target=central_character,
                type_of_evidence=TypeOfEvidence.INNOCUOUS
            )
            for detail in details
        ]
    except json.JSONDecodeError:
        print("Error decoding JSON response for innocuous details")
        return []
