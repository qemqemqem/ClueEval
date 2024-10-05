import argparse
from story.writer import create_story


def main():
    parser = argparse.ArgumentParser(description="Create mystery stories.")
    parser.add_argument("num_stories", type=int, nargs="?", default=5,
                        help="Number of stories to create (default: 1)")
    parser.add_argument("--interactive_mode", action="store_true")
    args = parser.parse_args()

    for i in range(args.num_stories):
        create_story(args.interactive_mode)

if __name__ == '__main__':
    main()
