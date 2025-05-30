import os
import time
import functools
import google.generativeai as genai


def retry_with_exponential_backoff(retries=3, base_delay=1):
   def decorator(func):
       @functools.wraps(func)
       def wrapper(*args, **kwargs):
           delay = base_delay
           for i in range(retries):
               try:
                   return func(*args, **kwargs)
               except Exception as e:
                   if i == retries - 1:  # Last retry failed
                       raise e
                   print(f"Retry attempt {i+1}...")
                   time.sleep(delay)  # Exponential backoff delay
                   delay *= 2  # Double delay for next retry
           return None
       return wrapper
   return decorator


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


class GeminiAPI:
   def __init__(self, model_name: str = "gemini-1.5-pro"):
       
       # Set API key
       genai.configure(api_key="YOUR_API_KEY")
       
       # Initialize model
       self.model = genai.GenerativeModel(
           model_name=model_name,
           generation_config={
               "temperature": 1,
               "top_p": 0.95,
               "max_output_tokens": 8192,
               "response_mime_type": "text/plain",
           }
       )
   
#    @retry_with_exponential_backoff(retries=10, base_delay=2)
   @retry_with_fixed_interval(retries=100, delay=5)
   def get_response(self, prompt: str) -> str:
       """Generate content"""
       response = self.model.generate_content(prompt)
       return response.text