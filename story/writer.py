import random
from dataclasses import dataclass, field
import os
from utils.gpt import prompt_completion_chat
from utils.display_interface import show_narrative_text, show_situation

@dataclass
class Story:
    # This is generated without an LLM, for diversity prompting reasons
    summary: str

    # The story has these elements, which are part of the story description
    random_crimes: list[str]
    random_places: list[str]
    random_people: list[str]
    killer: str
    victim: str
    crime_weapon: str
    crime_location: str

    # These are narratives within the story
    crime_story: str = ""
    distractor_stories: list[str] = field(default_factory=list)

    # This is an attempt to summarize the facts of the story
    bullet_points: list[str] = field(default_factory=list)


def load_elements(filename):
    with open(os.path.join('config', filename), 'r') as f:
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
        summary="",
        random_crimes=random.sample(crime_elements, 3),
        random_places=random.sample(place_elements, 3),
        random_people=random_people,
        killer=killer,
        victim=victim,
        crime_weapon=crime_weapon,
        crime_location=crime_location
    )

    story.summary = f"This is a mystery story in the style of a golden age classic, and it features the following elements:"
    for element in story.random_crimes + story.random_places + story.random_people:
        story.summary += f"\n- {element}"

    story.summary += f"\n\nThe central story is that a crime was committed with a {story.crime_weapon} in the {story.crime_location} by {story.killer}, killing {story.victim}. But there's shenanigans going on with the other stuff, too."

    return story

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
    story.crime_story = prompt_completion_chat(central_prompt)

    # Generate distractor stories for other characters
    other_characters = [char for char in story.random_people if char not in [story.killer, story.victim]]
    # murder_summary = f"{story.killer} killed {story.victim} with a {story.crime_weapon} in the {story.crime_location}."
    murder_summary = story.crime_story
    
    for character in other_characters:
        other_prompt = other_story_prompt.replace('{{summary}}', story.summary)
        other_prompt = other_prompt.replace('{{murder_summary}}', murder_summary)
        other_prompt = other_prompt.replace('{{character}}', character)
        other_prompt = other_prompt.replace('{{other_stories}}', "\n".join(story.distractor_stories))
        
        distractor_story = prompt_completion_chat(other_prompt)
        story.distractor_stories.append(distractor_story)

    return story

def convert_story_to_bullet_points(story: Story):
    # Load prompt template
    with open('config/prompts/convert_story_to_bullets.txt', 'r') as f:
        bullet_prompt = f.read()

    # Convert crime story to bullet points
    crime_prompt = bullet_prompt.replace('{{story}}', story.crime_story)
    crime_bullets = prompt_completion_chat(crime_prompt)
    story.bullet_points.extend([line.strip() for line in crime_bullets.split('\n') if line.strip().startswith('* ')])

    # Convert distractor stories to bullet points
    for distractor in story.distractor_stories:
        distractor_prompt = bullet_prompt.replace('{{story}}', distractor)
        distractor_bullets = prompt_completion_chat(distractor_prompt)
        story.bullet_points.extend([line.strip() for line in distractor_bullets.split('\n') if line.strip().startswith('* ')])

    return story

def main():
    story = get_random_details()
    show_situation(story.summary, title="Story Summary")
    story = write_stories(story)
    story = convert_story_to_bullet_points(story)
    show_narrative_text(story.crime_story, speaker="Crime Story")
    for i, distractor in enumerate(story.distractor_stories, 1):
        show_narrative_text(distractor, speaker=f"Distractor Story {i}")
    show_situation("\n".join(story.bullet_points), title="Bullet Points")

if __name__ == '__main__':
    main()
