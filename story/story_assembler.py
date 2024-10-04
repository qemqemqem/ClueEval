from story.evidence import TypeOfEvidence, StoryElement
from story.story import Story
from utils.display_interface import display_story_elements


def assemble_details(story: Story, num_sus: int = 3, num_proving_innocence: int = 1, num_distracting: int = 5) -> list[StoryElement]:
    # Collect all proving elements
    proving_elements = []
    # From crime story
    proving_elements.extend([
        element for element in story.crime_story.real_story_elements + story.crime_story.story_to_detective_elements
        if element.type_of_evidence in [TypeOfEvidence.PROVES_GUILT, TypeOfEvidence.PROVES_INNOCENCE]
    ])
    # From distractor stories
    for distractor_story in story.distractor_stories:
        proving_elements.extend([
            element for element in distractor_story.real_story_elements + distractor_story.story_to_detective_elements + distractor_story.clues_that_prove_innocence_elements
            if element.type_of_evidence in [TypeOfEvidence.PROVES_GUILT, TypeOfEvidence.PROVES_INNOCENCE]
        ])
    # Print out the proving elements
    display_story_elements(proving_elements, title="Proving Elements (Guilt or Innocence)")
