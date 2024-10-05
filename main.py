import argparse
from story.writer import create_story
from config.story_config import StoryConfig

def main():
    parser = argparse.ArgumentParser(description="Create mystery stories.")
    parser.add_argument("num_stories", type=int, nargs="?", default=5,
                        help="Number of stories to create (default: 5)")
    parser.add_argument("--interactive_mode", action="store_true")
    parser.add_argument("--num_suspicious", type=int, default=3,
                        help="Number of suspicious elements per character")
    parser.add_argument("--num_innocence", type=int, default=1,
                        help="Number of elements proving innocence")
    parser.add_argument("--num_distracting", type=int, default=5,
                        help="Number of distracting elements")
    parser.add_argument("--max_distractors", type=int, default=3,
                        help="Maximum number of distractor stories")
    args = parser.parse_args()

    config = StoryConfig(
        num_stories=args.num_stories,
        interactive_mode=args.interactive_mode,
        num_suspicious_elements=args.num_suspicious,
        num_proving_innocence_elements=args.num_innocence,
        num_distracting_elements=args.num_distracting,
        max_distractor_stories=args.max_distractors
    )

    for i in range(config.num_stories):
        create_story(config)

if __name__ == '__main__':
    main()
