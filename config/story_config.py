from dataclasses import dataclass

@dataclass
class StoryConfig:
    num_stories: int = 5
    interactive_mode: bool = False
    num_suspicious_elements: int = 3
    num_proving_innocence_elements: int = 1
    num_distracting_elements: int = 5
    num_random_people: int = 5
    num_random_crimes: int = 3
    num_random_places: int = 3
    # Add more configurable parameters here
