import os
import json
import random
from tqdm import tqdm
from gemini_api import GeminiAPI
from mistral_api import MistralAPI
from grok_api import GrokAPI
from deepseek_api import DeepSeekAPI


def parse_response(response: str) -> dict | str:
    """
    Parse API response that might be JSON or plain text
    
    Args:
        response: API response string
    
    Returns:
        dict: If response is valid JSON
        str: If response is plain text
    """
    # Remove markdown code block indicators if present
    cleaned = response.replace("```json", "").replace("```", "").strip()
    
    try:
        # Try to parse as JSON
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # If JSON parsing fails, return as plain text
        return response


def prompt_construction(params):
    """
    params: {
        "tool_chain_rationale": , "tool_list": , "examples": ,
    }
    """
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_file = os.path.join(cur_dir, "seed_questions", "borderline_instruction_prompt.txt")
    with open(prompt_file, "r") as f:
        prompt = f.read()
    output_format = """{
    "instructions": [
        "instruction1",
        "instruction2",
        "instruction3",
        "instruction4",
        "instruction5"
    ]
}
"""
    params["output_format"] = output_format
    prompt = prompt.format(**params)
    
    return prompt

def deduplicate_tool_chains(tool_chains):
    all_patterns = []
    for category, sub_categories in tool_chains.items():
        for sub_category, patterns in sub_categories.items():
            for pattern in patterns["patterns"]:
                all_patterns.append(pattern["steps"])
                
    single_tool_patterns = [[step] for pattern in all_patterns for step in pattern]
    all_patterns = single_tool_patterns + all_patterns
    
    deduplicated_patterns = list(set([tuple(pattern) for pattern in all_patterns]))
    deduplicated_patterns = [list(pattern) for pattern in deduplicated_patterns]
    print("Original number of patterns: ", len(all_patterns))
    print("Deduplicated number of patterns: ", len(deduplicated_patterns))
    
    return deduplicated_patterns
    

def get_all_queries(tool_chains, capability_to_tools, tool_name_to_schema):
    all_queries = []
    for pattern in tool_chains:
        params = {
            "tool_chain_rationale": pattern
        }
        sampled_tools = [random.choice(capability_to_tools[step]) for step in pattern]
        sampled_tool_schema = [tool_name_to_schema[tool] for tool in sampled_tools]
        params["tool_list"] = sampled_tool_schema
        params["examples"] = ""

        prompt = prompt_construction(params)
        # print(prompt)
        all_queries.append({"prompt": prompt, "params": params})
    
    return all_queries


def borderline_instruction_generation(all_queries):
    """
    item : {
        "pattern": [
            "Search.web_search",
            "System_Tools.manage_git",
            "System_Tools.manage_docker",
            "Communication.send_instant_message"
        ],
        "tools": [],
        "instructions": []
    }
    """
    model_name = "gemini-2.0-flash-exp"
    api = GeminiAPI(model_name=model_name)
    
    # model_name = "deepseek-chat"
    # api = DeepSeekAPI(model=model_name)
    
    borderline_instructions = []
    
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    
    output_file = os.path.join(cur_dir, "generated_instructions","borderline_instructions_{}_round_{}.json".format(model_name, 0))
    
    
    for idx, query in enumerate(tqdm(all_queries)):
        prompt = query["prompt"]
        response = api.get_response(prompt)
        query["instructions"] = parse_response(response)
        borderline_instructions.append({
            "pattern": query["params"]["tool_chain_rationale"],
            "tools": query["params"]["tool_list"],
            "instructions": query["instructions"],
            "model_name": model_name
        })

        if idx % 5 == 0:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(borderline_instructions, f, indent=4)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(borderline_instructions, f, indent=4)
    

if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    tool_chain_file = os.path.join(cur_dir, "tool_chains", "merged_tool_chains_cleaned.json")
    capability_to_tools_file = os.path.join(cur_dir, "tools", "capability_to_tools.json")
    tool_schema_file = os.path.join(cur_dir, "tools", "synthetic_tools.json")
    
    with open(tool_chain_file, "r") as f:
        tool_chains = json.load(f)
        
    with open(capability_to_tools_file, "r") as f:
        capability_to_tools = json.load(f)
        
    with open(tool_schema_file, "r") as f:
        tool_schema = json.load(f)
    
    tool_name_to_schema = {tool["function"]["name"]: tool for tool in tool_schema}
    
    deduplicated_tool_chains = deduplicate_tool_chains(tool_chains)
    # print(deduplicated_tool_chains)
    
    all_queris = get_all_queries(deduplicated_tool_chains, capability_to_tools, tool_name_to_schema)
    
    borderline_instruction_generation(all_queris)