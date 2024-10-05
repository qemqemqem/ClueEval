import argparse
from story.writer import create_story
from config.story_config import StoryConfig
from utils.gpt import set_default_model


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
    parser.add_argument("--num_random_people", type=int, default=3,
                        help="Number of bystanders in the story who might be confused with the killer. This many plus one (for the killer) stories will be generated.")
    parser.add_argument("--num_random_items", type=int, default=2,
                        help="Number of random suspicious items to be in the story. One of them will be the murder weapon. I find that a high value tends to cause too much discussion of random distracting items.")
    parser.add_argument("--num_random_places", type=int, default=3,
                        help="Number of random places to select, like rooms or other settings")
    parser.add_argument("--default_model", type=str, default="gpt-4o-mini",
                        help="Default model to use for GPT completions. Supports gpt-4o-mini or gpt-4o.")
    args = parser.parse_args()

    set_default_model(args.default_model)

    config = StoryConfig(
        interactive_mode=args.interactive_mode,
        num_suspicious_elements=args.num_suspicious,
        num_proving_innocence_elements=args.num_innocence,
        num_distracting_elements=args.num_distracting,
        num_random_people=args.num_random_people,
        num_random_items=args.num_random_items,
        num_random_places=args.num_random_places,
    )

    for i in range(args.num_stories):
        create_story(config)


if __name__ == '__main__':
    main()
