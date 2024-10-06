# CLUE Evaluation Task

This directory contains a custom multiple-choice task for the LM Evaluation Harness, specifically for CLUE (Chinese Language Understanding Evaluation) questions.

## How it works

1. **Data**: The task uses a JSON Lines (jsonl) file `clue_questions.jsonl` containing multiple-choice questions from the CLUE dataset.

2. **Configuration**: The task is configured in `clue_eval.yaml`, which specifies how to load and process the data.

3. **Evaluation**: The `run_evaluation.sh` script demonstrates how to run the evaluation using the OpenAI API.

## Files

- `clue_questions.jsonl`: Contains the CLUE questions, choices, and correct answers.
- `clue_eval.yaml`: Configures the task, including how to format the prompt and process the model's output.
- `run_evaluation.sh`: A shell script to run the evaluation.

## What's needed

To use this task:

1. Install the LM Evaluation Harness. You can find installation instructions and more information at https://github.com/EleutherAI/lm-evaluation-harness
2. Make sure you have an OpenAI API key if you're using the OpenAI model (as in the example script).
3. Customize the `clue_questions.jsonl` file with your own questions if desired.
4. Adjust the `run_evaluation.sh` script if you want to use a different model or change evaluation parameters.

## Running the evaluation

To run the evaluation:

1. Make sure you have the LM Evaluation Harness installed and set up correctly. For more information about lm_eval and its installation, visit: https://github.com/EleutherAI/lm-evaluation-harness
2. Make the script executable: `chmod +x lm_eval/tasks/clue_eval/run_evaluation.sh`
3. Run the script: `lm_eval/tasks/clue_eval/run_evaluation.sh`

The script uses the `lm_eval` command provided by the LM Evaluation Harness. You can find the exact command in the `run_evaluation.sh` file.

The results will be saved in the directory specified by `results_path` in the `clue_eval.yaml` file.

## Customization

You can easily customize this task by:
- Adding more questions to `my_multiple_choice.jsonl`
- Modifying the prompt format in `my_multiple_choice.yaml`
- Changing the evaluation model or parameters in `run_evaluation.sh`
