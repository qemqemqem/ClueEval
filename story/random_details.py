import random
import os
import string
import re
from story.story import Story
from utils.display_interface import display_narrative
from utils.str_utils import unindent
from utils.gpt import prompt_completion_chat


def load_elements(filename):
    with open(os.path.join('config', filename), 'r') as f:
        return [line.strip() for line in f]


def get_random_details() -> Story:
    # Load elements from files
    crime_elements = [string.capwords(elem) for elem in load_elements('crime_elements.txt')]
    place_elements = [string.capwords(elem) for elem in load_elements('place_elements.txt')]
    person_elements = [string.capwords(elem) for elem in load_elements('person_elements.txt')]
    mystery_settings = load_elements('mystery_settings.txt')

    # Sample random people
    random_people = random.sample(person_elements, 5)  # The first two are the killer and victim
    killer, victim = random_people[0], random_people[1]

    random_crimes = random.sample(crime_elements, 3)
    random_places = random.sample(place_elements, 3)

    # Select specific crime weapon, location, and setting
    crime_weapon = random.choice(random_crimes)
    crime_location = random.choice(random_places)
    mystery_setting = random.choice(mystery_settings)

    # Create character details
    character_details = {}
    for character in random_people:
        description = random_character_details()
        character_details[character] = description

    # Create a Story object
    story = Story(
        summary="",
        random_crimes=random_crimes,
        random_places=random_places,
        random_people=random_people,
        killer=killer,
        victim=victim,
        crime_weapon=crime_weapon,
        crime_location=crime_location,
        mystery_setting=mystery_setting,
        character_details=character_details,
        detective_details=random_character_details(),
    )

    bystanders = [person for person in story.random_people if person not in [story.killer, story.victim]]
    other_places = [place for place in story.random_places if place != story.crime_location]
    other_items = [crime for crime in story.random_crimes if crime != story.crime_weapon]

    story.summary = unindent(f"""
        This is a mystery story in the style of a golden age classic. The story features the following elements:

        Victim: {story.victim} ({character_details[story.victim]})
        Killer: {story.killer} ({character_details[story.killer]})
        The Detective: Detecto ({story.detective_details})

        Other Characters:
        {', '.join([f"{person} ({character_details[person]})" for person in bystanders])}

        It Takes Place In: {story.mystery_setting}
        The Crime Happened In: {story.crime_location}
        Other Locations in the Story: {', '.join(other_places)}

        The Murder Weapon: {story.crime_weapon}
        Other Suspicious Items: {', '.join(other_items)}
        
        The central story is that a crime was committed with a {story.crime_weapon} in the {story.crime_location} by {story.killer}, killing {story.victim}. But there's shenanigans going on with the other stuff, too. Detective Detecto is on the case!
    """).strip()

    display_narrative(story.summary, "Story summary before edit")

    # Refine the story summary using GPT
    refined_summary = refine_story_summary(story)

    # Parse the title and synopsis
    title_match = re.search(r"Title: (.+)", refined_summary)
    synopsis_match = re.search(r"Synopsis: (.+)", refined_summary, re.DOTALL)

    if title_match:
        story.title = title_match.group(1).strip()
    if synopsis_match:
        story.synopsis = synopsis_match.group(1).strip()

    display_narrative(f"Title: {story.title}\n\nSynopsis: {story.synopsis}", "Refined Story Details")

    return story


def refine_story_summary(story: Story) -> str:
    prompt = unindent(f"""
        I'm going to show you the summary for my mystery story. I want you to help me choose a title and a synopsis. 
        
        Here's the current summary:
    
        {story.summary}
    
        Please fill out the Title and Synopsis. Use the format I'm showing you, with "Title: ..." and "Synopsis: ...", and no extra new lines.
        
        Title: Your Title Here
        Synopsis: Your 2-3 sentence synopsis here.
    """)

    refined_summary = prompt_completion_chat(
        question=prompt,
        model="gpt-4",
        temperature=0.7,
        max_tokens=1000
    )

    return refined_summary


def random_character_details():
    gender = random.choice(["man", "woman", "non-binary person"])
    age = random.randint(18, 70)
    physical_traits = [
        "tall", "short", "average height", "fat", "thin", "muscular", "lanky",
        "blonde", "brunette", "redhead", "grey-haired", "curly-haired",
        "freckled", "pale", "tanned", "scarred"
    ]
    personality_traits = [
        "friendly", "stuttering", "elegant", "clumsy", "cheerful", "grumpy", "shy",
        "outgoing", "mean", "awkward", "confident", "nervous", "eccentric", "charming",
        "suspicious", "absent-minded", "meticulous", "laid-back", "energetic", "stoic"
    ]
    speaking_styles = [
        "eloquent", "blunt", "verbose", "terse", "sarcastic", "formal", "casual",
        "dramatic", "monotone", "enthusiastic", "whispered", "booming", "rapid-fire",
        "drawling", "articulate", "mumbling", "sing-song", "gravelly", "squeaky"
    ]

    physical_trait = random.choice(physical_traits)
    personality_trait = random.choice(personality_traits)
    speaking_style = random.choice(speaking_styles)
    
    description = f"a {age}-year-old {gender}, {physical_trait} and {personality_trait}, who speaks in a {speaking_style} manner"
    return description
