import json

def create_simple_jsonl():
    input_file = "generated_questions/all_questions.jsonl"
    output_file = "generated_questions/simple_questions.jsonl"

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            data = json.loads(line)

            simple_data = {
                "question": f"{data['full_prose']}\n\n{data['question']}",
                "choices": list(data["options"].values()),
                "answer": list(data["options"].values()).index(data["killer"])
            }
            
            json.dump(simple_data, outfile)
            outfile.write('\n')

    print(f"Simple JSONL file created: {output_file}")

if __name__ == "__main__":
    create_simple_jsonl()
