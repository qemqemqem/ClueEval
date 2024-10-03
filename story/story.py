from dataclasses import dataclass, field


@dataclass
class Story:
    # This is generated without an LLM, for diversity prompting reasons
    summary: str

    # The story has these elements, which are part of the story description
    random_crimes: list[str]
    random_places: list[str]
    random_people: list[str]
    killer: str
    victim: str
    crime_weapon: str
    crime_location: str
    mystery_setting: str

    # These are narratives within the story
    crime_story: str = ""
    distractor_stories: list[str] = field(default_factory=list)

    # This is an attempt to summarize the facts of the story
    bullet_points: list[str] = field(default_factory=list)
