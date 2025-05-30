import os
import json
from collections import defaultdict


def explore_harmful_categories(cur_dir):
    """
    This function explores the harmful categories in the current directory
    """
    harmful_categories = []
    with open(os.path.join(cur_dir, 'harmful_categories.json'), 'r', encoding="utf-8") as f:
        harmful_categories = json.load(f)
        
    # print("Harmful categories: {}".format(harmful_categories))
    print("Number of harmful categories: {}".format(len(harmful_categories)))
    
    total_fine_grained_categories = 0
    for category, sub_categories in harmful_categories.items():
        total_fine_grained_categories += len(sub_categories)
    
    print("Total number of fine-grained categories: {}".format(total_fine_grained_categories))
    
    for category, sub_categories in harmful_categories.items():
        print("{}".format(category))
        print("{}".format(sub_categories))


def explore_tool_chain_patterns(cur_dir):
    """
    This function explores the tool chain patterns in the current directory
    {
        "category_name": {
            "subcategory_name": {
                "patterns": [
                    {
                        "steps": ["tool1", "tool2", ...],
                        "explanation": "Detailed explanation of how these tools could be misused      together..."
                    }
                ]
            }
        }
    }
    """
    tool_chains_file = os.path.join(cur_dir, 'tool_chains', 'merged_tool_chains_cleaned.json')
    with open(tool_chains_file, 'r', encoding="utf-8") as f:
        tool_chains = json.load(f)
    category_to_tool_chain = defaultdict(list)
    for category, sub_categories in tool_chains.items():
        for sub_category, patterns in sub_categories.items():
            category_to_tool_chain[category].extend(patterns["patterns"])
        print("Category: {}".format(category))
        print("Number of patterns: {}".format(len(category_to_tool_chain[category])))
    
    print("Total number of patterns: {}".format(sum([len(v) for v in category_to_tool_chain.values()])))


if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    # explore_harmful_categories(cur_dir)

    explore_tool_chain_patterns(cur_dir)