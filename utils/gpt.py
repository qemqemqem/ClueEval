import os
import re
import time

import os
import openai

from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Set up your OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]


def prompt_completion(question, engine="davinci-instruct-beta", max_tokens=64, temperature=1.0, n=1, stop=None, return_top_n: int = None, ideal_length=None, collapse_newlines=True, throwaway_empties=True):
    if stop is None:
        stop = ["\n", "DONE"]
    start_time = time.perf_counter()
    prompt = f"{question} "
    response = openai.Completion.create(
        model=engine,  # "curie" is cheaper, "davinci" is good, there's also an option to get chatgpt on the website
        prompt=prompt,
        max_tokens=max_tokens,
        n=n,
        stop=stop,  # ["\n", "DONE"],  # ["\n", " Q:"],
        temperature=temperature,
    )
    if collapse_newlines:
        # Replace any number of newlines with a single newline, using regular expressions
        for i in range(len(response.choices)):
            response.choices[i].text = re.sub(r"\n+", "\n", response.choices[i].text)
    if return_top_n is None:
        answer = response.choices[0].text.strip()
    elif ideal_length is not None:
        answer = []
        ordered_choices = sorted(response.choices, key=lambda x: abs(sum(c.isalpha() for c in x.text)) - ideal_length)
        if throwaway_empties:
            ordered_choices = [x for x in ordered_choices if sum(c.isalpha() for c in x.text) > 0]
        for i in range(return_top_n):
            answer.append(ordered_choices[i].text.strip())
        print(f"Ordered choices: {ordered_choices}")
    else:  # TODO This doesn't really handle all cases
        answer = []
        for i in range(return_top_n):
            answer.append(response.choices[i].text.strip())
    # print(f"\tPROMPT: {question}\n\tANSWER: {answer}\n")
    duration = time.perf_counter() - start_time
    # print(f"Duration: {duration:.2f} seconds: {answer}")
    return answer


def prompt_completion_chat(question="", model="gpt-4o", n=1, temperature=0.2, max_tokens=256, system_description="You write clearly and well.", messages=None, stop=None):
    start_time = time.perf_counter()
    prompt = f"{question} "
    response = client.chat.completions.create(
        # https://openai.com/blog/introducing-chatgpt-and-whisper-apis
        model=model,
        messages=messages if messages is not None else [
            {"role": "system", "content": system_description},
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
        n=n,
        stop=stop,
    )
    # print(response)
    answers = []
    for i in range(n):
        ans = response.choices[i].message.content.strip()
        # Sometimes it quotes the response, so strip those off
        if ans[0] == "\"" and ans[-1] == "\"":
            ans = ans[1:-1]
        answers.append(ans)
    # print(f"\tPROMPT: {question}\n\tANSWER: {answer}\n")
    duration = time.perf_counter() - start_time
    short_answer = answers[0][:20].replace('\n', ' ')
    # print(f"Duration: {duration:.2f} seconds: {short_answer}...")
    if n == 1:
        return answers[0]
    return

def prompt_completion_json(messages, model="gpt-4o-mini", temperature=0.2, max_tokens=1000):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages + [{"role": "system", "content": "You must respond with valid JSON only."}],
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in JSON completion: {e}")
        return None
