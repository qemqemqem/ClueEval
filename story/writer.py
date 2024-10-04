from story.story import Story, CharacterStory
from story.random_details import get_random_details
from story.story_assembler import assemble_details
from story.story_elements import convert_story_to_story_elements, generate_innocuous_details
from utils.gpt import prompt_completion_chat
from utils.display_interface import display_story_element, display_narrative, display_story_elements, display_bullet_points
import random


def parse_crime_story(character_name: str, story_text: str) -> CharacterStory:
    lines = story_text.strip().split('\n')
    details = {}
    current_section = None

    for line in lines:
        line = line.replace('**', '')  # Remove all instances of "**"
        if line.startswith('# '):
            current_section = line[2:].lower()
            details[current_section] = []
        elif line.startswith('Motive:'):
            details['motive'] = line.split(':', 1)[1].strip()
        elif line.startswith('Means:'):
            details['means'] = line.split(':', 1)[1].strip()
        elif line.startswith('Opportunity:'):
            details['opportunity'] = line.split(':', 1)[1].strip()
        elif current_section:
            details[current_section].append(line)

    return CharacterStory(
        character_name=character_name,
        means=details['means'],
        motive=details['motive'],
        opportunity=details['opportunity'],
        real_story='\n'.join(details['what happened']),
        story_to_detective='\n'.join(details['explanation to detective']),
        clues_that_prove_innocence='\n'.join(details.get('clues that prove innocence', []))
    )

def write_stories(story: Story):
    # Load prompt templates
    with open('config/prompts/central_story.txt', 'r') as f:
        central_story_prompt = f.read()
    with open('config/prompts/other_story.txt', 'r') as f:
        other_story_prompt = f.read()

    # Generate the central crime story
    central_prompt = central_story_prompt.replace('{{summary}}', story.summary)
    central_prompt = central_prompt.replace('{{killer}}', story.killer)
    central_prompt = central_prompt.replace('{{victim}}', story.victim)
    crime_story_text = prompt_completion_chat(central_prompt)
    story.crime_story = parse_crime_story(story.killer, crime_story_text)

    # Generate distractor stories for other characters
    other_characters = [char for char in story.random_people if char not in [story.killer, story.victim]]
    murder_summary = story.crime_story.real_story
    
    for character in other_characters:
        other_prompt = other_story_prompt.replace('{{summary}}', story.summary)
        other_prompt = other_prompt.replace('{{murder_summary}}', murder_summary)
        other_prompt = other_prompt.replace('{{character}}', character)
        other_prompt = other_prompt.replace('{{other_stories}}', "\n".join([ds.real_story for ds in story.distractor_stories]))
        
        distractor_story_text = prompt_completion_chat(other_prompt)
        distractor_story = parse_crime_story(character, distractor_story_text)
        story.distractor_stories.append(distractor_story)

    return story


def stories_to_elements(story: Story):
    story.crime_story.real_story_elements = convert_story_to_story_elements(story.crime_story.real_story)
    story.crime_story.story_to_detective_elements = convert_story_to_story_elements(
        story.crime_story.story_to_detective)
    
    if story.crime_story.clues_that_prove_innocence:
        story.crime_story.clues_that_prove_innocence_elements = convert_story_to_story_elements(
            story.crime_story.clues_that_prove_innocence)
    
    # Generate innocuous details for the crime story
    story.crime_story.innocuous_elements = generate_innocuous_details(story.crime_story.real_story, story.killer)
    
    for distractor_story in story.distractor_stories:
        distractor_story.real_story_elements = convert_story_to_story_elements(distractor_story.real_story)
        distractor_story.story_to_detective_elements = convert_story_to_story_elements(
            distractor_story.story_to_detective)
        
        if distractor_story.clues_that_prove_innocence:
            distractor_story.clues_that_prove_innocence_elements = convert_story_to_story_elements(
                distractor_story.clues_that_prove_innocence)
        
        # Generate innocuous details for each distractor story
        distractor_story.innocuous_elements = generate_innocuous_details(distractor_story.real_story, distractor_story.character_name)


def write_prose(story: Story):
    # Load the full prose prompt
    with open('config/prompts/full_prose.txt', 'r') as f:
        full_prose_prompt = f.read()

    # Prepare the notes and outline
    notes = story.summary + "\n\n" + "\n\n".join([f"{cs.character_name}'s Story to the Detective: \n\n{cs.story_to_detective}" for cs in [story.crime_story] + story.distractor_stories])

    outline = f"- The setting: {story.mystery_setting}\n"
    outline += f"- The victim, {story.victim}, lies dead on the floor!\n"
    outline += f"- Detective Detecto arrives at the scene of the crime. (Detecto is {story.detective_details})\n"
    characters = story.get_living_character_names_random()
    outline += f"- There are only {len(characters)} people present: {', '.join(characters)}\n"
    outline += f"- No one else could possibly have been here.\n"
    outline += f"- The detective begins to poke around and ask questions.\n"
    outline += f"- And this is what the detective learns, from clues and from talking to the people present:\n"
    outline += "\n".join([f"- {element.text}" for element in story.new_story_details])
    outline += "\n- It must be one of these suspects, and Detecto knows just who it is.\n"

    # Fill in the prompt template
    prompt = full_prose_prompt.replace("{notes}", notes.strip()).replace("{outline}", outline.strip())

    # Generate the full prose
    story.full_prose = prompt_completion_chat(prompt, model="gpt-4o")


def create_question(story: Story):
    characters = [story.killer] + [ds.character_name for ds in story.distractor_stories]
    random.shuffle(characters)
    
    story.question = f"Given the story you have just read, who is guilty of killing {story.victim}?"
    story.question_options = {chr(65 + i): character for i, character in enumerate(characters)}

def present_question(story: Story):
    while True:
        user_input = input("Enter your answer (A, B, C, or D): ").upper()
        if user_input in story.question_options:
            if story.question_options[user_input] == story.killer:
                return "Correct! You've identified the killer."
            else:
                return f"Incorrect. The killer was {story.killer}."
        else:
            print("Invalid input. Please enter A, B, C, or D.")

def create_story(interactive: bool = False) -> Story:
    """
    Create a mystery story.

    This function generates a complete mystery story, including details, prose, and a question.
    
    Args:
        interactive (bool, optional): If True, displays story elements to the console
                                      and presents an interactive question. 
                                      If False, silently generates the story.
                                      Defaults to False.

    Returns:
        Story: The complete generated story object.
    """
    # Get random story details
    story = get_random_details()
    if interactive:
        display_story_element(story.summary, title="Story Summary")

    # Write stories
    story = write_stories(story)
    if interactive:
        display_narrative(story.crime_story.__str__(), speaker="Parsed Crime Story")
        for distractor_story in story.distractor_stories:
            display_narrative(distractor_story.__str__(), f"Parsed Story for {distractor_story.character_name}")

    # Convert stories to story elements and display them
    stories_to_elements(story)
    if interactive:
        display_story_elements(story.crime_story.real_story_elements, title="Crime Story Real Story Elements")
        display_story_elements(story.crime_story.story_to_detective_elements, title="Crime Story Detective Story Elements")
        if story.crime_story.clues_that_prove_innocence:
            display_story_elements(story.crime_story.clues_that_prove_innocence_elements, 
                                   title="Crime Story Clues that Prove Innocence")
        display_story_elements(story.crime_story.innocuous_elements, title="Crime Story Innocuous Details")
        
        for distractor_story in story.distractor_stories:
            display_story_elements(distractor_story.real_story_elements,
                                   title=f"{distractor_story.character_name}'s Story, Real Story Elements")
            display_story_elements(distractor_story.story_to_detective_elements,
                                   title=f"{distractor_story.character_name}'s Story, Detective Story Elements")
            if distractor_story.clues_that_prove_innocence:
                display_story_elements(distractor_story.clues_that_prove_innocence_elements,
                                       title=f"{distractor_story.character_name}'s Story, Clues that Prove Innocence")
            display_story_elements(distractor_story.innocuous_elements, 
                                   title=f"{distractor_story.character_name}'s Story, Innocuous Details")

    # Assemble all details
    assemble_details(story)

    # Write full prose
    write_prose(story)
    if interactive:
        display_narrative(story.full_prose, speaker="Full Prose")

    # Create the question
    create_question(story)

    if interactive:
        # Present the question only in interactive mode
        display_story_element(story.question, title="Question")
        options = [f"{key}: {value}" for key, value in story.question_options.items()]
        display_bullet_points(options, title="Suspects")
        result = present_question(story)
        display_narrative(result)
        display_bullet_points([str(rfi) for rfi in story.reasons_for_innocence], title="Reasoning")
    
    return story

if __name__ == '__main__':
    create_story()
