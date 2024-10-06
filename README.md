# ClueEval: Murder Mysteries as LLM Evals

ClueEval is a project designed to evaluate the reasoning capabilities of Large Language Models (LLMs) by challenging them to solve generated mystery stories. 

## Purpose

ClueEval creates mystery stories that theoretically test deductive reasoning abilities in solving.

## How It Works

1. **Story Generation**: The system randomly generates a basic mystery, including a killer and victim, in `story/random_details.py`. Then, `story/writer.py` uses an LLM to create a unique murder mystery, giving each character their own story and perspective.

2. **Narrative Creation**: A detailed narrative is generated, including both the true events and misleading information.

3. **Clue Assembly**: The system compiles a set of clues, some relevant to solving the mystery and others serving as red herrings.

4. **Prose**: The set of clues is turned into prose.

5. **Evaluation**: Whodunnit? The clues contained in the prose should be enough to figure it out. These are fair play mysteries.

## How to Run

1. Ensure you have Python 3.10+ installed on your system.

2. Clone this repository:
   ```
   git clone https://github.com/yourusername/ClueEval.git
   cd ClueEval
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```

5. Run the main script (interactive mode):
   ```
   python main.py --interactive_mode
   ```
   
   This will give you a mystery to solve. Read it and decide who you think is the killer!

6. Run the main script (generation mode):
   ```
   python main.py 10
   ```
   
   This will generate 10 mysteries, and store them in `generated_questions`. Beware that each generation will take a couple of minutes, as there is a lot of back and forth with an LLM.

7. Run lm_eval:
   For information on running the CLUE evaluation task using lm_eval, please refer to the README in the `lm_eval/tasks/clue_eval/` directory.

## Project Structure

- `story/`: Contains the core logic for story generation and processing.
- `utils/`: Utility functions, including GPT API interactions.
- `config/`: Configuration files, including prompts and element lists.
- `lm_eval/`: Contains the CLUE evaluation task and results. See the README in `lm_eval/tasks/clue_eval/` for detailed information on running the evaluation.

## Contributing

We welcome contributions to ClueEval! Please feel free to submit issues, feature requests, or pull requests.

## Acknowledgments

- Inspired by golden age mystery authors.
- Narrative generation uses OpenAI's GPT models.
- Anthropic Claude wrote most of the code, although I did some of the work too. I take responsibility for all the bugs.

Happy mystery solving!
