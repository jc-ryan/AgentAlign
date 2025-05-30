import os
import json
import asyncio
import logging
from typing import List, Dict, Optional
from anthropic import AsyncAnthropicBedrock
from tqdm.asyncio import tqdm_asyncio

# did not use
SYSTEM_PROMPT = "You are a helpful AI assistant that provides accurate and relevant information."

# used for further divide the data into benign and harmful（used only of borderline cases）
SYSTEM_PROMPT = "You are a helpful, harmless and honest assistant. You should carefully evaluate if the user's request is safe and ethical to fulfill."

class AnthropicClient:
    _instance = None
    _client = None

    @classmethod
    def get_client(
        cls,
        aws_access_key: str,
        aws_secret_key: str,
        aws_region: str = "us-east-1"
    ) -> AsyncAnthropicBedrock:
        if cls._client is None:
            cls._client = AsyncAnthropicBedrock(
                aws_access_key=aws_access_key,
                aws_secret_key=aws_secret_key,
                aws_region=aws_region
            )
        return cls._client

async def _throttled_anthropic_chat_completion(
    client: AsyncAnthropicBedrock,
    max_attempts: int = 8,
    retry_interval: int = 5,
    model: str = "us.anthropic.claude-3-5-haiku-20241022-v1:0",
    messages: List[Dict[str, str]] = None,
    tools: Optional[List[Dict]] = None,
    max_tokens: int = 1024,
    temperature: float = 1.0,
) -> Dict:
    last_exception = None
    
    for attempt in range(max_attempts):
        try:
            response = await client.messages.create(
                model=model,
                messages=messages,
                tools=tools,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return json.loads(response.model_dump_json())

        except Exception as e:
            last_exception = e
            logging.error(f"Attempt {attempt + 1}/{max_attempts} failed: {str(e)}")
            
            if attempt < max_attempts - 1:
                await asyncio.sleep(retry_interval)
                continue
    
    error_message = f"All {max_attempts} attempts failed. Last error: {str(last_exception)}"
    return {
        "id": "error_response",
        "model": model,
        "content": error_message,
        "role": "assistant",
        "usage": None,
        "stop_reason": "error"
    }


def convert_to_anthropic_tool_schema(tools: List[Dict]) -> List[Dict]:
    """Convert OpenAI/Generic tool schema to Anthropic tool schema format.
    
    Args:
        tools (List[Dict]): Tool schema in OpenAI/Generic format
        
    Returns:
        List[Dict]: Tool schema in Anthropic format
    """
    anthropic_tools = []
    
    for tool in tools:
        if tool["type"] != "function":
            continue
            
        function = tool["function"]
        anthropic_tool = {
            "name": function["name"],
            "description": function["description"],
            "input_schema": function["parameters"]
        }
        anthropic_tools.append(anthropic_tool)
        
    return anthropic_tools

async def generate_from_anthropic_response(
    instructions: List[Dict],
    aws_access_key: str,
    aws_secret_key: str,
    system_prompt: str = None,
    model: str = "us.anthropic.claude-3-5-haiku-20241022-v1:0",
    max_tokens: int = 1024,
    temperature: float = 1.0,
    tools: Optional[List[Dict]] = None,
) -> List[Dict]:
    client = AnthropicClient.get_client(
        aws_access_key=aws_access_key,
        aws_secret_key=aws_secret_key
    )
    
    async_responses = []
    for instruction in instructions:
        messages = []
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        messages.append({
            "role": "user",
            "content": instruction["instruction"]
        })
        
        async_responses.append(
            _throttled_anthropic_chat_completion(
                client=client,
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                tools=convert_to_anthropic_tool_schema(instruction.get("tools", tools) if instruction.get("tools", tools) else [])
            )
        )

    responses = await tqdm_asyncio.gather(*async_responses)
    return responses

async def process_batches(
    instructions: List[Dict],
    aws_access_key: str,
    aws_secret_key: str,
    batch_size: int,
    output_file: str,
    processed_results: Optional[List] = None
) -> List[Dict]:
    total_batches = len(instructions) // batch_size + 1
    all_results = []
    if processed_results:
        all_results.extend(processed_results)
    
    for batch_idx in range(total_batches):
        start_idx = batch_idx * batch_size
        end_idx = min(start_idx + batch_size, len(instructions))
        batch_instructions = instructions[start_idx:end_idx]
        
        batch_responses = await generate_from_anthropic_response(
            instructions=batch_instructions,
            aws_access_key=aws_access_key,
            aws_secret_key=aws_secret_key,
            # system_prompt=SYSTEM_PROMPT
        )
        
        batch_results = []
        for instruction, response in zip(batch_instructions, batch_responses):
            batch_results.append({
                "id": instruction["id"],
                "instruction": instruction["instruction"],
                "response": response
            })
        
        all_results.extend(batch_results)
        
        if batch_idx % 2 == 0:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(all_results, f, indent=4)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=4)
    
    return all_results

def execute_validation(
    instruction_file: str,
    output_file: str,
    aws_access_key: str,
    aws_secret_key: str,
    recover: bool = False
):
    with open(instruction_file, "r", encoding="utf-8") as f:
        instructions = json.load(f)
    
    if recover:
        with open(output_file, "r", encoding="utf-8") as f:
            all_results = json.load(f)
            processed_instruction_ids = set([x["id"] for x in all_results])
            print("Recovered {} instructions from previous results".format(len(all_results)))
            instructions = [x for x in instructions if x["id"] not in processed_instruction_ids]
            print("Continue to process {} remained cases".format(len(instructions)))
            asyncio.run(
                process_batches(
                    instructions=instructions,
                    aws_access_key=aws_access_key,
                    aws_secret_key=aws_secret_key,
                    batch_size=5,
                    output_file=output_file,
                    processed_results=all_results
                )
            )
    else:
        asyncio.run(
            process_batches(
                instructions=instructions,
                aws_access_key=aws_access_key,
                aws_secret_key=aws_secret_key,
                batch_size=10,
                output_file=output_file
            )
        )

if __name__ == "__main__":
    api_key = "YOUR_API_KEY"
    secret_key = "YOUR_API_KEY"
    
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    instruction_file = os.path.join(cur_dir, "harmful_instructions_semantic_filtered.json")
    output_file = os.path.join(cur_dir, "harmful_instructions_responses.json")
    
    # execute_validation(
    #     instruction_file=instruction_file, output_file=output_file,
    #     aws_access_key=api_key, aws_secret_key=secret_key
    # )
    
    execute_validation(
        instruction_file=instruction_file, output_file=output_file, aws_access_key=api_key,
        aws_secret_key=secret_key, recover=True
    )
