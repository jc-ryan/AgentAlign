import time
import functools
from typing import List, Dict, Union
from openai import OpenAI


def retry_with_fixed_interval(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == retries - 1:  # Last retry failed
                        raise e
                    print(f"Retry attempt {i+1}...")
                    time.sleep(delay)  # Fixed delay
            return None
        return wrapper
    return decorator


class GPTAPI:
    def __init__(self,
                api_key: str = "YOUR_API_KEY",
                model: str = "gpt-4o",
                base_url: str = "BASE_URL"):
        """
        Initialize GPT API client
        
        Args:
            api_key: GPT API key
            model: Model name to use
            base_url: Base URL for API
        """
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        self.model = model

    @retry_with_fixed_interval(retries=100, delay=5)
    def get_response(self,
                    prompt: str,
                    system_prompt: str = None,
                    temperature: float = 1.0,
                    max_tokens: int = None) -> str:
        """
        Get completion from GPT API
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature (default: 1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
        """
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
            
        messages.append({
            "role": "user", 
            "content": prompt
        })

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return completion.choices[0].message.content

    def chat(self,
            messages: List[Dict[str, str]],
            temperature: float = 1.0,
            max_tokens: int = None) -> str:
        """
        Chat completion with message history
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated response text
        """
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return completion.choices[0].message.content

    def get_usage(self,
                 messages: List[Dict[str, str]],
                 temperature: float = 1.0,
                 max_tokens: int = None) -> Dict:
        """
        Get token usage information for a completion
        
        Args:
            messages: List of message dictionaries
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Dictionary containing usage information
        """
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        if completion.usage:
            return completion.usage.model_dump()
        return None