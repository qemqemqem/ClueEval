from dataclasses import dataclass

@dataclass
class StoryConfig:
    num_stories: int = 5
    interactive_mode: bool = False
    num_suspicious_elements: int = 3
    num_proving_innocence_elements: int = 1
    num_distracting_elements: int = 5
    max_distractor_stories: int = 3
    # Add more configurable parameters here
