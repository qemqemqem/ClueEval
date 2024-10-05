from story.evidence import TypeOfEvidence, StoryElement, WhenInTime, MurderElement
from story.story import Story
from utils.display_interface import display_story_elements
from collections import defaultdict
import random

def assemble_details(story: Story, num_sus: int = 3, num_proving_innocence: int = 1, num_distracting: int = 5):
    all_elements = []
    characters = [story.killer] + [ds.character_name for ds in story.distractor_stories]

    # Collect all elements
    all_elements.extend(story.crime_story.real_story_elements)
    all_elements.extend(story.crime_story.story_to_detective_elements)
    all_elements.extend(story.crime_story.innocuous_elements)
    for ds in story.distractor_stories:
        all_elements.extend(ds.real_story_elements)
        all_elements.extend(ds.story_to_detective_elements)
        all_elements.extend(ds.clues_that_prove_innocence_elements)
        all_elements.extend(ds.innocuous_elements)

    # Categorize elements
    suggests_guilt = defaultdict(list)
    proves_innocence = defaultdict(list)
    distracting = []

    for element in all_elements:
        if element.type_of_evidence == TypeOfEvidence.SUGGESTS_GUILT:
            suggests_guilt[element.target].append(element)
        elif element.type_of_evidence == TypeOfEvidence.PROVES_INNOCENCE:
            proves_innocence[element.target].append(element)
        elif element.type_of_evidence == TypeOfEvidence.INNOCUOUS:
            distracting.append(element)

    # Assemble the final list of elements
    final_elements = []

    # Add suspicious elements for each character
    for character in characters:
        final_elements.extend(random.sample(suggests_guilt[character], min(num_sus, len(suggests_guilt[character]))))

    # Add elements proving innocence for non-guilty characters
    for character in characters:
        if character != story.killer:
            innocence_proving_details: list[StoryElement] = random.sample(proves_innocence[character], min(num_proving_innocence, len(proves_innocence[character])))
            story.reasons_for_guilt_and_innocence.extend(innocence_proving_details)
            final_elements.extend(innocence_proving_details)

    # Add the means, motive, and opportunity for all characters
    killer_elements = []
    for character in characters:
        character_story = story.crime_story if character == story.killer else next((ds for ds in story.distractor_stories if ds.character_name == character), None)
        if character_story:
            character_elements = [element for element in character_story.real_story_elements 
                                  if element.target == character and element.murder_element is not None]
            final_elements.extend(character_elements)
            if character == story.killer:
                killer_elements = character_elements

    # Add note about killer's means, motive, and opportunity
    note = "Note: Only one character had a means, motive, and opportunity. Here are the details for the killer:"
    story.reasons_for_guilt_and_innocence.append(note)
    for element in killer_elements:
        story.reasons_for_guilt_and_innocence.append(str(element))

    # Add distracting elements
    final_elements.extend(random.sample(distracting, min(num_distracting, len(distracting))))

    # Sort the final elements by their WhenInTime value and then by speaker
    final_elements.sort(key=lambda x: ([WhenInTime.UNKNOWN, WhenInTime.BEFORE_CRIME, WhenInTime.DURING_CRIME, WhenInTime.AFTER_CRIME].index(x.when), x.speaker))

    # Display the final list of elements
    display_story_elements(final_elements, title="Assembled Story Elements")

    story.new_story_details = final_elements
