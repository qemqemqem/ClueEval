import argparse
from story.writer import create_story
from config.story_config import StoryConfig

def main():
    parser = argparse.ArgumentParser(description="Create mystery stories.")
    parser.add_argument("num_stories", type=int, nargs="?", default=1,
                        help="Number of stories to create (default: 1)")
    parser.add_argument("--interactive_mode", action="store_true",
                        help="If true, the application will ask you to guess the murderer before revealing it.")
    parser.add_argument("--num_suspicious", type=int, default=3,
                        help="Number of suspicious elements per character")
    parser.add_argument("--num_innocence", type=int, default=1,
                        help="Number of elements proving innocence for the bystanders (capped at the number that are generated)")
    parser.add_argument("--num_distracting", type=int, default=5,
                        help="Number of distracting elements per character")
    args = parser.parse_args()

    config = StoryConfig(
        num_stories=args.num_stories,
        interactive_mode=args.interactive_mode,
        num_suspicious_elements=args.num_suspicious,
        num_proving_innocence_elements=args.num_innocence,
        num_distracting_elements=args.num_distracting,
    )

    for i in range(config.num_stories):
        create_story(config)

if __name__ == '__main__':
    main()
