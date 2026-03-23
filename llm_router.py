import os
from anthropic import Anthropic
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_claude_response(prompt: str, system: str = None) -> str:
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    kwargs = {
        'model': 'claude-haiku-4-5-20251001',
        'max_tokens': 2000,
        'messages': [{'role': 'user', 'content': prompt}]
    }
    if system:
        kwargs['system'] = system
    response = client.messages.create(**kwargs)
    return response.content[0].text

def get_openai_response(prompt: str, system: str = None) -> str:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    messages = []
    if system:
        messages.append({'role': 'system', 'content': system})
    messages.append({'role': 'user', 'content': prompt})
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        max_tokens=2000
    )
    return response.choices[0].message.content
