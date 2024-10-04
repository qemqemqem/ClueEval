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

    # display_narrative(crime_story_text, speaker="Crime Story")
    display_narrative(story.crime_story.__str__(), speaker="Parsed Crime Story")

    # Generate distractor stories for other characters
    other_characters = [char for char in story.random_people if char not in [story.killer, story.victim]]
    # other_characters = []  # Disabling for Development! TODO Reenable
    # murder_summary = f"{story.killer} killed {story.victim} with a {story.crime_weapon} in the {story.crime_location}."
    murder_summary = story.crime_story.real_story
    
    for character in other_characters:
        other_prompt = other_story_prompt.replace('{{summary}}', story.summary)
        other_prompt = other_prompt.replace('{{murder_summary}}', murder_summary)
        other_prompt = other_prompt.replace('{{character}}', character)
        other_prompt = other_prompt.replace('{{other_stories}}', "\n".join([ds.real_story for ds in story.distractor_stories]))
        
        distractor_story_text = prompt_completion_chat(other_prompt)
        distractor_story = parse_crime_story(character, distractor_story_text)
        story.distractor_stories.append(distractor_story)

        # display_narrative(distractor_story_text, speaker=f"Distractor Story {character}")
        display_narrative(distractor_story.__str__(), f"Parsed Story for {character}")

    return story


def stories_to_elements(story: Story):
    story.crime_story.real_story_elements = convert_story_to_story_elements(story.crime_story.real_story)
    display_story_elements(story.crime_story.real_story_elements, title="Crime Story Real Story Elements")
    story.crime_story.story_to_detective_elements = convert_story_to_story_elements(
        story.crime_story.story_to_detective)
    display_story_elements(story.crime_story.story_to_detective_elements, title="Crime Story Detective Story Elements")
    
    if story.crime_story.clues_that_prove_innocence:
        story.crime_story.clues_that_prove_innocence_elements = convert_story_to_story_elements(
            story.crime_story.clues_that_prove_innocence)
        display_story_elements(story.crime_story.clues_that_prove_innocence_elements, 
                               title="Crime Story Clues that Prove Innocence")
    
    # Generate innocuous details for the crime story
    story.crime_story.innocuous_elements = generate_innocuous_details(story.crime_story.real_story, story.killer)
    display_story_elements(story.crime_story.innocuous_elements, title="Crime Story Innocuous Details")
    
    for i, distractor_story in enumerate(story.distractor_stories):
        distractor_story.real_story_elements = convert_story_to_story_elements(distractor_story.real_story)
        display_story_elements(distractor_story.real_story_elements,
                               title=f"Distractor Story {i + 1} Real Story Elements")

        distractor_story.story_to_detective_elements = convert_story_to_story_elements(
            distractor_story.story_to_detective)
        display_story_elements(distractor_story.story_to_detective_elements,
                               title=f"Distractor Story {i + 1} Detective Story Elements")
        
        if distractor_story.clues_that_prove_innocence:
            distractor_story.clues_that_prove_innocence_elements = convert_story_to_story_elements(
                distractor_story.clues_that_prove_innocence)
            display_story_elements(distractor_story.clues_that_prove_innocence_elements,
                                   title=f"Distractor Story {i + 1} Clues that Prove Innocence")
        
        # Generate innocuous details for each distractor story
        distractor_story.innocuous_elements = generate_innocuous_details(distractor_story.real_story, distractor_story.character_name)
        display_story_elements(distractor_story.innocuous_elements, 
                               title=f"Distractor Story {i + 1} Innocuous Details")


def write_prose(story: Story):
    # Load the full prose prompt
    with open('config/prompts/full_prose.txt', 'r') as f:
        full_prose_prompt = f.read()

    # Prepare the notes and outline
    notes = story.summary + "\n\n" + "\n\n".join([f"{cs.character_name}'s Story to the Detective: \n\n{cs.story_to_detective}" for cs in [story.crime_story] + story.distractor_stories])

    outline = f"- The setting: {story.mystery_setting}"
    outline += f"- The victim, {story.victim}, lies dead on the floor!"
    outline += f"- Detective Detecto arrives at the scene of the crime."
    characters = story.get_living_character_names_random()
    outline += f"- There are only {len(characters)} people present: {', '.join(characters)}"
    outline += f"- The detective begins to poke around and ask questions."
    outline += f"- And this is what the detective learns, from clues and from talking to the people present:"
    outline += "\n".join([f"- {element.text}" for element in story.new_story_details])

    # Fill in the prompt template
    prompt = full_prose_prompt.replace("{notes}", notes).replace("{outline}", outline)

    # Print the full prompt
    display_narrative(prompt, speaker="Full Prose Prompt")

    # Generate the full prose
    story.full_prose = prompt_completion_chat(prompt, model="gpt-4o")

    # Display the full prose
    display_narrative(story.full_prose, speaker="Full Prose")


def create_question(story: Story):
    characters = [story.killer] + [ds.character_name for ds in story.distractor_stories]
    random.shuffle(characters)
    
    story.question = f"Given the story you have just read, who is guilty of killing {story.victim}?"
    story.question_options = {chr(65 + i): character for i, character in enumerate(characters)}

def present_question(story: Story):
    display_story_element(story.question, title="Question")
    options = [f"{key}: {value}" for key, value in story.question_options.items()]
    display_bullet_points(options, title="Suspects")
    
    while True:
        user_input = input("Enter your answer (A, B, C, or D): ").upper()
        if user_input in story.question_options:
            if story.question_options[user_input] == story.killer:
                display_narrative("Correct! You've identified the killer.")
            else:
                display_narrative(f"Incorrect. The killer was {story.killer}.")
            break
        else:
            display_narrative("Invalid input. Please enter A, B, C, or D.")

def main():
    # Get random story details
    story = get_random_details()
    display_story_element(story.summary, title="Story Summary")

    # Write stories
    story = write_stories(story)

    # Convert stories to story elements and display them
    stories_to_elements(story)

    # Assemble all details
    assemble_details(story)

    # Write full prose
    write_prose(story)

    # Create and present the question
    create_question(story)
    present_question(story)


if __name__ == '__main__':
    main()
