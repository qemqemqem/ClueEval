import random
from dataclasses import dataclass, field
from typing import List, Optional

from story.evidence import StoryElement


@dataclass
class CharacterStory:
    character_name: str

    means: str
    motive: str
    opportunity: str
    real_story: str
    story_to_detective: str
    clues_that_prove_innocence: str = ""

    real_story_elements: list[StoryElement] = field(default_factory=list)
    story_to_detective_elements: list[StoryElement] = field(default_factory=list)
    clues_that_prove_innocence_elements: list[StoryElement] = field(default_factory=list)
    innocuous_elements: list[StoryElement] = field(default_factory=list)

    def __str__(self):
        return f"Means: {self.means}\nMotive: {self.motive}\nOpportunity: {self.opportunity}\n\nReal Story: \n\n{self.real_story}\n\nStory to Detective: \n\n{self.story_to_detective}"


@dataclass
class Story:
    # This is generated without an LLM, for diversity prompting reasons
    summary: str

    # The story has these elements, which are part of the story description
    random_crimes: List[str]
    random_places: List[str]
    random_people: List[str]
    killer: str
    victim: str
    crime_weapon: str
    crime_location: str
    mystery_setting: str

    # Flavor
    character_details: dict[str, str] = field(default_factory=dict)
    detective_details: str = ""

    title: str = ""
    synopsis: str = ""

    # These are narratives within the story
    crime_story: Optional[CharacterStory] = None
    distractor_stories: List[CharacterStory] = field(default_factory=list)

    # This is an attempt to summarize the facts of the story
    bullet_points: List[str] = field(default_factory=list)

    # This is for converting the story into prose
    new_story_details: list[StoryElement] = field(default_factory=list)
    reasons_for_innocence: list[StoryElement] = field(default_factory=list)
    full_prose: str = ""

    question: str = ""
    question_options: dict = field(default_factory=dict)

    def get_living_character_names_random(self):
        characters = [charo for charo in self.random_people if charo not in [self.victim]]
        random.shuffle(characters)
        return characters
