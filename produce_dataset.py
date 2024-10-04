import argparse
import json
from story.writer import create_story

def generate_stories(num_stories, output_file):
    stories = []
    for _ in range(num_stories):
        story = create_story()
        story_data = {
            "summary": story.summary,
            "full_prose": story.full_prose,
            "question": story.question,
            "options": story.question_options,
            "correct_answer": story.killer
        }
        stories.append(story_data)
    
    with open(output_file, 'w') as f:
        json.dump(stories, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Generate mystery stories dataset")
    parser.add_argument("num_stories", type=int, help="Number of stories to generate")
    parser.add_argument("output_file", type=str, help="Output file path for the dataset")
    args = parser.parse_args()

    generate_stories(args.num_stories, args.output_file)
    print(f"Generated {args.num_stories} stories and saved to {args.output_file}")

if __name__ == "__main__":
    main()
