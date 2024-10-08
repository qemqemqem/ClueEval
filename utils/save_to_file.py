import os
import json
from datetime import datetime
from enum import Enum
from story.story import Story
from story.evidence import StoryElement, TypeOfEvidence, WhenInTime
import hashlib

class StoryEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)

def create_simple_data(story: Story):
    return {
        "question": f"{story.full_prose}\n\n{story.question}",
        "choices": list(story.question_options.values()),
        "answer": list(story.question_options.values()).index(story.killer)
    }

def save_story_to_file(story: Story, creation_steps: str = ""):
    """
    Save a Story object to a Markdown file and append a JSON object to all_questions.jsonl.
    
    Args:
    story (Story): The Story object to be saved.
    """
    # Create directories
    os.makedirs("generated_questions", exist_ok=True)
    os.makedirs("story_creation_logs", exist_ok=True)

    # Save to Markdown file
    filename = f"generated_questions/{story.title.replace(' ', '_')}.md"
    
    # Save full creation steps to a separate file
    creation_steps_filename = f"story_creation_logs/{story.title.replace(' ', '_')}.md"
    with open(creation_steps_filename, 'w') as f:
        f.write(creation_steps)
    
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
        for reason in story.reasons_for_guilt_and_innocence:
            f.write(f"- {reason}\n")
        f.write("\n")
        
        f.write("## Story Details\n\n")
        f.write("```jsonl\n")
        for element in story.new_story_details:
            f.write(json.dumps(element.__dict__, cls=StoryEncoder) + "\n")
        f.write("```\n\n")

        f.write("## Story Configuration\n\n")
        f.write("```python\n")
        for key, value in vars(story.config).items():
            f.write(f"{key} = {value}\n")
        f.write("```\n\n")

        f.write("## Creation Steps\n\n")
        f.write(f"Full creation steps can be found in: {creation_steps_filename}\n\n")

    print(f"Story saved to {filename}")

    # Save JSON object to all_questions.jsonl
    question_data = {
        "title": story.title,
        "full_prose": story.full_prose,
        "question": story.question,
        "options": story.question_options,
        "killer": story.killer,
        "reasoning": [str(reason) for reason in story.reasons_for_guilt_and_innocence],
        "story_details": [element.__dict__ for element in story.new_story_details],
        "story_config": vars(story.config),
        # "full_creation_steps": creation_steps
    }
    
    with open("generated_questions/all_questions.jsonl", "a") as f:
        json.dump(question_data, f, cls=StoryEncoder)
        f.write("\n")

    print("Question added to generated_questions/all_questions.jsonl")

    # Save simple JSON object to simple_questions.jsonl
    simple_data = create_simple_data(story)
    with open("generated_questions/simple_questions.jsonl", "a") as f:
        json.dump(simple_data, f)
        f.write("\n")

    print("Simple question added to generated_questions/simple_questions.jsonl")
