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
    random_people = random.sample(person_elements, 5)
    killer, victim = random_people[0], random_people[1]

    random_crimes = random.sample(crime_elements, 3)
    random_places = random.sample(place_elements, 3)

    # Select specific crime weapon, location, and setting
    crime_weapon = random.choice(random_crimes)
    crime_location = random.choice(random_places)
    mystery_setting = random.choice(mystery_settings)

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
        mystery_setting=mystery_setting
    )

    story.summary = f"This is a mystery story in the style of a golden age classic, set in a {story.mystery_setting}, and it features the following elements:"
    for element in story.random_crimes + story.random_places + story.random_people:
        story.summary += f"\n- {element}"

    story.summary += f"\n\nThe central story is that a crime was committed with a {story.crime_weapon} in the {story.crime_location} by {story.killer}, killing {story.victim}. But there's shenanigans going on with the other stuff, too."

    return story
