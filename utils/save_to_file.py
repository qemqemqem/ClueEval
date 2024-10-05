import os
import json
from enum import Enum
from story.story import Story
from story.evidence import StoryElement, TypeOfEvidence, WhenInTime

class StoryEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)

def save_story_to_file(story: Story):
    """
    Save a Story object to a Markdown file.
    
    Args:
    story (Story): The Story object to be saved.
    """
    filename = f"generated_questions/{story.title.replace(' ', '_')}.md"
    
    with open(filename, 'w') as f:
        f.write(f"# {story.title}\n\n")
        
        f.write("## Full Story\n\n")
        f.write(story.full_prose)
        f.write("\n\n")
        
        f.write("## Question\n\n")
        f.write(story.question)
        f.write("\n\n")
        
        f.write("## Choices\n\n")
        for key, value in story.question_options.items():
            f.write(f"- {key}: {value}\n")
        f.write("\n")
        
        f.write("## Correct Answer\n\n")
        f.write(f"The killer is {story.killer}\n\n")
        
        f.write("## Reasoning\n\n")
        for reason in story.reasons_for_innocence:
            f.write(f"- {reason}\n")
        f.write("\n")
        
        f.write("## Story Details\n\n")
        f.write("```json\n")
        f.write(json.dumps([element.__dict__ for element in story.new_story_details], indent=4, cls=StoryEncoder))
        f.write("\n```")

    print(f"Story saved to {filename}")
