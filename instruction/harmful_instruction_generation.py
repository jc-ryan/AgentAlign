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
        "category": , "sub_category": , "tool_chain_rationale": ,
        "pattern_explanation": , "tool_list": , "examples": ,
    }
    """
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_file = os.path.join(cur_dir, "seed_questions", "harmful_instruction_prompt.txt")
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


def get_all_queries(tool_chains, capability_to_tools, tool_name_to_schema):
    all_queries = []
    for category, sub_categories in tool_chains.items():
        for sub_category, patterns in sub_categories.items():
            for pattern in patterns["patterns"]:
                params = {
                    "category": category,
                    "sub_category": sub_category,
                    "tool_chain_rationale": pattern["steps"],
                    "pattern_explanation": pattern["explanation"],
                }
                sampled_tools = [random.choice(capability_to_tools[step]) for step in pattern["steps"]]
                sampled_tool_schema = [tool_name_to_schema[tool] for tool in sampled_tools]
                params["tool_list"] = sampled_tool_schema
                params["examples"] = ""

                prompt = prompt_construction(params)
                all_queries.append({"prompt": prompt, "params": params})
    
    return all_queries


def upsample_patterns(all_queries):
    """
    choose from those critical patterns
    """
    critical_categories = ["self_harm", "bias_and_fairness", "misinformation"]
    sampled_queries = [query for query in all_queries if query["params"]["category"] in critical_categories]
    
    print("up-sampled {} queries".format(len(sampled_queries)))
    
    return sampled_queries


def harmful_instruction_generation(all_queries):
    """
    item : {
        "category": "cybercrime",
        "sub_category": "malware_deployment",
        "pattern": {
            "steps": [
                "Search.web_search",
                "System_Tools.manage_git",
                "System_Tools.manage_docker",
                "Communication.send_instant_message"
            ],
            "explanation": "This sequence allows an attacker to search for malware code, clone repositories, package the malware in a container, and distribute it to victims using instant messaging."
        },
        "tools": [],
        "instructions": []
    }
    """
    # model_name = "gemini-exp-1206"
    # model_name = "gemini-2.0-flash-exp"
    # model_name = "gemini-1.5-pro"
    # api = GeminiAPI(model_name=model_name)
    
    # model_name = "mistral-large-2411"
    # model_name = "mistral-large-2407"
    # api = MistralAPI(model=model_name)
    
    # model_name = "grok-2-1212"
    # api = GrokAPI(model=model_name)
    
    model_name = "deepseek-chat"
    api = DeepSeekAPI(model=model_name)
    
    harmful_instructions = []
    
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(cur_dir, "generated_instructions","harmful_instructions_{}_round_{}.json".format(model_name, 0))
    
    all_queries = upsample_patterns(all_queries)
    
    for idx, query in enumerate(tqdm(all_queries)):
        prompt = query["prompt"]
        response = api.get_response(prompt)
        query["instructions"] = parse_response(response)
        harmful_instructions.append({
            "category": query["params"]["category"],
            "sub_category": query["params"]["sub_category"],
            "pattern": {
                "steps": query["params"]["tool_chain_rationale"],
                "explanation": query["params"]["pattern_explanation"]
            },
            "tools": query["params"]["tool_list"],
            "instructions": query["instructions"],
            "model_name": model_name
        })

        if idx % 5 == 0:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(harmful_instructions, f, indent=4)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(harmful_instructions, f, indent=4)
    

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
    
    all_queris = get_all_queries(tool_chains, capability_to_tools, tool_name_to_schema)
    
    harmful_instruction_generation(all_queris)