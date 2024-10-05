from dataclasses import dataclass

@dataclass
class StoryConfig:
    num_stories: int = 5
    interactive_mode: bool = False
    num_suspicious_elements: int = 3
    num_proving_innocence_elements: int = 1
    num_distracting_elements: int = 5
    num_random_people: int = 3  # This many bystanders, plus the killer and the victim and the detective, will be in the story
    num_random_items: int = 3  # Items. One of them will be the murder weapon
    num_random_places: int = 3
    # Add more configurable parameters here
