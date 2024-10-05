from dataclasses import dataclass, fields

@dataclass
class StoryConfig:
    interactive_mode: bool = False
    num_suspicious_elements: int = 3  # For each suspect, we include this many clues which suggest their guilt
    num_proving_innocence_elements: int = 1  # For each bystander, we include one clue which proves their innocence, such as a clear alibi
    num_distracting_elements: int = 5  # For each bystander, we include random comments about the scene to distract the reader
    num_random_people: int = 3  # This many bystanders, plus the killer and the victim and the detective, will be in the story
    num_random_items: int = 3  # Items. One of them will be the murder weapon
    num_random_places: int = 3
    # Add more configurable parameters here

    def __str__(self):
        return "StoryConfig(" + ", ".join(f"{field.name}={getattr(self, field.name)}" for field in fields(self)) + ")"
