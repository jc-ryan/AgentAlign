import os
import json


def refresh_invalid_examples(instruction_file):
    with open(instruction_file, "r", encoding="utf-8") as f:
        instructions = json.load(f)
        
    valid_examples = []
    invalid_examples = []
    for instruction in instructions:
        if instruction["response"]["stop_reason"] != "error":
            valid_examples.append(instruction)
        else:
            invalid_examples.append(instruction)
            
    print(f"Valid examples: {len(valid_examples)}")
    print(f"Filtered invalid examples: {len(invalid_examples)}")
            
    with open(instruction_file, "w", encoding="utf-8") as f:
        json.dump(valid_examples, f, indent=4)


if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    
    instruction_file = os.path.join(cur_dir, "harmful_instructions_responses.json")
    refresh_invalid_examples(instruction_file)