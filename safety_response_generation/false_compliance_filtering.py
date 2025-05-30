import os
import json


def get_safety_data(instruction_data, response_data):
    safety_data = []
    id_to_instruction = {item["id"]: item for item in instruction_data}
    filtered_items = []
    
    for item in response_data:
        if item["response"]["stop_reason"] == "end_turn":
            safety_data.append({
                "id": item["id"],
                "category": id_to_instruction[item["id"]]["category"],
                "sub_category": id_to_instruction[item["id"]]["sub_category"],
                "pattern": id_to_instruction[item["id"]]["pattern"],
                "instruction": item["instruction"],
                "response": item["response"]["content"][0]["text"],
                "tools": id_to_instruction[item["id"]]["tools"]
            })
        else:
            filtered_items.append(item)
    
    
    print("Original number of samples: {}".format(len(response_data)))
    print("Filtered number of samples: {}".format(len(safety_data)))
    print("Filtered {} samples".format(len(filtered_items)))
    
    return safety_data, filtered_items


if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    instruction_file = os.path.join(cur_dir, "harmful_instructions_semantic_filtered.json")
    response_file = os.path.join(cur_dir, "harmful_instructions_responses.json")
    
    with open(instruction_file, "r", encoding="utf-8") as f:
        instruction_data = json.load(f)
        
    with open(response_file, "r", encoding="utf-8") as f:
        response_data = json.load(f)
        
    safety_data, filtered_data = get_safety_data(instruction_data, response_data)

    output_file = os.path.join(cur_dir, "safety_responses.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(safety_data, f, indent=4)
        
    filtered_output_file = os.path.join(cur_dir, "filtered_responses.json")
    with open(filtered_output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, indent=4)