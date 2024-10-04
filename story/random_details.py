import random
import os
import string
from story.story import Story

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

    story.summary = f"This is a mystery story in the style of a golden age classic, set in a {story.mystery_setting}, and it features the following elements:"
    for element in story.random_crimes + story.random_places + story.random_people:
        if element in character_details:
            element = f"{element} ({character_details[element]})"
        story.summary += f"\n- {element}"

    story.summary += f"\n\nThe central story is that a crime was committed with a {story.crime_weapon} in the {story.crime_location} by {story.killer}, killing {story.victim}. But there's shenanigans going on with the other stuff, too. The mystery is being investigated by detective Detecto."

    return story


def random_character_details():
    gender = random.choice(["man", "woman"])
    age = random.randint(18, 75)
    adjectives = random.sample(
        ["tall", "short", "fat", "thin", "friendly", "blonde", "brunette", "redhead", "stuttering", "elegant", "clumsy",
         "cheerful", "grumpy", "shy", "outgoing"], 2)
    description = f"a {age}-year-old {gender}, {adjectives[0]} and {adjectives[1]}"
    return description
