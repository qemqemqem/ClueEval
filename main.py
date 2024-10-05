import argparse
from story.writer import create_story


def main():
    parser = argparse.ArgumentParser(description="Create mystery stories.")
    parser.add_argument("num_stories", type=int, nargs="?", default=5,
                        help="Number of stories to create (default: 5)")
    args = parser.parse_args()

    for i in range(args.num_stories):
        create_story()

if __name__ == '__main__':
    main()
