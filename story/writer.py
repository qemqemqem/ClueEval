from story.story import Story, CharacterStory
from story.random_details import get_random_details
from utils.gpt import prompt_completion_chat
from utils.display_interface import display_story_element, display_narrative, display_bullet_points
from story.bullet_classifier import Hypotheses, classify_evidence, Hypothesis, display_classified_evidence

def parse_crime_story(story_text: str) -> CharacterStory:
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
        means=details['means'],
        motive=details['motive'],
        opportunity=details['opportunity'],
        real_story='\n'.join(details['what happened']),
        story_to_detective='\n'.join(details['explanation to detective'])
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
    story.crime_story = parse_crime_story(crime_story_text)

    display_narrative(crime_story_text, speaker="Crime Story")
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
        distractor_story = parse_crime_story(distractor_story_text)
        story.distractor_stories.append(distractor_story)

        display_narrative(distractor_story_text, speaker=f"Distractor Story {character}")
        display_narrative(distractor_story.__str__(), f"Parsed Story for {character}")

    return story

def convert_story_to_bullet_points(story: Story):
    # Load prompt template
    with open('config/prompts/convert_story_to_bullets.txt', 'r') as f:
        bullet_prompt = f.read()

    # Convert crime story to bullet points
    crime_prompt = bullet_prompt.replace('{{story}}', story.crime_story.real_story)
    crime_bullets = prompt_completion_chat(crime_prompt)
    story.bullet_points.extend([line.strip()[2:] for line in crime_bullets.split('\n') if line.strip().startswith('* ')])

    # Convert distractor stories to bullet points
    for distractor in story.distractor_stories:
        distractor_prompt = bullet_prompt.replace('{{story}}', distractor.real_story)
        distractor_bullets = prompt_completion_chat(distractor_prompt)
        story.bullet_points.extend([line.strip()[2:] for line in distractor_bullets.split('\n') if line.strip().startswith('* ')])

    return story


def main():
    # Get random story details
    story = get_random_details()
    display_story_element(story.summary, title="Story Summary")

    # Write stories
    story = write_stories(story)

    # Convert story to bullet points
    story = convert_story_to_bullet_points(story)
    display_bullet_points(story.bullet_points, title="Story Bullet Points")

    # Create hypotheses based on story details
    hypotheses = Hypotheses(
        killers=[Hypothesis(name) for name in story.random_people],
        weapons=[Hypothesis(weapon) for weapon in story.random_crimes],
        locations=[Hypothesis(location) for location in story.random_places]
    )

    # Classify evidence
    full_story = f"{story.crime_story.real_story}\n\n" + "\n\n".join([ds.real_story for ds in story.distractor_stories])
    evidence_classification = classify_evidence(story.bullet_points, hypotheses)

    # Display classified evidence
    display_classified_evidence(evidence_classification)

if __name__ == '__main__':
    main()
