# ClueEval: Investigating LLM Reasoning through Mystery Solving

ClueEval is a project designed to evaluate the reasoning capabilities of Large Language Models (LLMs) by challenging them to solve generated mystery stories. This tool creates complex, Agatha Christie-style murder mysteries and presents them to LLMs, testing their ability to follow clues, make logical deductions, and arrive at correct conclusions.

## Purpose

The main objectives of ClueEval are:

1. To assess LLMs' capacity for complex reasoning and deduction.
2. To evaluate LLMs' ability to process and synthesize information from multiple sources.
3. To test LLMs' understanding of cause and effect in narrative contexts.
4. To explore LLMs' potential for creative problem-solving within structured scenarios.

## How It Works

1. **Story Generation**: The system creates a unique murder mystery, complete with a killer, victim, murder weapon, location, and a cast of characters with their own motives and alibis.

2. **Narrative Creation**: A detailed narrative is generated, including both the true events and misleading information.

3. **Clue Assembly**: The system compiles a set of clues, some relevant to solving the mystery and others serving as red herrings.

4. **LLM Challenge**: The generated mystery, along with its clues, is presented to an LLM for solving.

5. **Evaluation**: The LLM's solution is compared to the actual solution, assessing its reasoning process and accuracy.

## How to Run

1. Ensure you have Python 3.7+ installed on your system.

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

5. Run the main script:
   ```
   python story/writer.py
   ```

This will generate a new mystery, create the narrative, and present it to the LLM for solving.

## Project Structure

- `story/`: Contains the core logic for story generation and processing.
- `utils/`: Utility functions, including GPT API interactions.
- `config/`: Configuration files, including prompts and element lists.

## Contributing

We welcome contributions to ClueEval! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the works of Agatha Christie and other classic mystery authors.
- Powered by OpenAI's GPT models.

Happy mystery solving!
