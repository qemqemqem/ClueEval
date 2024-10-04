import os
from story.story import Story
from story.evidence import StoryElement

def save_story_to_file(story: Story):
    """
    Save a Story object to a Markdown file.
    
    Args:
    story (Story): The Story object to be saved.
    """
    filename = f"{story.title.replace(' ', '_')}.md"
    
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
            f.write(f"- {reason.text}\n")
        f.write("\n")
        
        f.write("## Story Details\n\n")
        for detail in story.new_story_details:
            f.write(f"- {detail.text} (Type: {detail.type_of_evidence.value}, Target: {detail.target}, When: {detail.when.value})\n")
        
    print(f"Story saved to {filename}")
