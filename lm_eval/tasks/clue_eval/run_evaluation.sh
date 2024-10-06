#!/bin/bash

lm_eval --model openai-chat-completions \
    --model_args model=gpt-4o-mini \
    --tasks clue_eval \
    --num_fewshot 0 \
    --batch_size 1 \
    --output_path lm_eval/tasks/clue_eval/results/gpt4o_mini_clue_eval \
    --apply_chat_template \
    --log_samples \
    --verbosity DEBUG
