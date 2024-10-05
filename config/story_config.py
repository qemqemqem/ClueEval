from dataclasses import dataclass

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
        return (f"StoryConfig(interactive_mode={self.interactive_mode}, "
                f"num_suspicious_elements={self.num_suspicious_elements}, "
                f"num_proving_innocence_elements={self.num_proving_innocence_elements}, "
                f"num_distracting_elements={self.num_distracting_elements}, "
                f"num_random_people={self.num_random_people}, "
                f"num_random_items={self.num_random_items}, "
                f"num_random_places={self.num_random_places})")
