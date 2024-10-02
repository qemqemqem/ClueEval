import random
from dataclasses import dataclass
import os

@dataclass
class Story:
    diversity_prompt: str
    random_crimes: list[str]
    random_places: list[str]
    random_people: list[str]
    killer: str
    victim: str
    crime_weapon: str
    crime_location: str



def load_elements(filename):
    with open(os.path.join('ClueEval', 'config', filename), 'r') as f:
        return [line.strip() for line in f]

def get_random_details() -> Story:
    # Load elements from files
    crime_elements = load_elements('crime_elements.txt')
    place_elements = load_elements('place_elements.txt')
    person_elements = load_elements('person_elements.txt')

    # Sample random people
    random_people = random.sample(person_elements, 5)
    killer, victim = random_people[0], random_people[1]

    # Select specific crime weapon and location
    crime_weapon = random.choice(crime_elements)
    crime_location = random.choice(place_elements)

    # Create a Story object
    story = Story(
        diversity_prompt="",
        random_crimes=random.sample(crime_elements, 3),
        random_places=random.sample(place_elements, 3),
        random_people=random_people,
        killer=killer,
        victim=victim,
        crime_weapon=crime_weapon,
        crime_location=crime_location
    )

    story.diversity_prompt = f"This is a mystery story in the style of a golden age classic, and it features the following elements:"
    for element in story.random_crimes + story.random_places + story.random_people:
        story.diversity_prompt += f"\n- {element}"

    story.diversity_prompt += f"\n\nThe central story is that a crime was committed with a {story.crime_weapon} in the {story.crime_location} by {story.killer}, killing {story.victim}. But there's shenanigans going on with the other stuff, too."

    return story

def main():
    story = get_random_details()
    print(story.diversity_prompt)

if __name__ == '__main__':
    main()
