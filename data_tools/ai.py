import os
import time

import openai
from dotenv import load_dotenv
from openai.error import RateLimitError

# Load environment variables from a .env file
load_dotenv()

# Set your OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_text(text):
    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Please summarize the following video transcript:\n\n{text}"}
                ]
            )
            return response.choices[0].message['content'].strip()
        except RateLimitError as e:
            # Handle rate limit error by waiting and retrying
            print(f"Rate limit exceeded. Waiting before retrying... {str(e)}")
            time_to_wait = int(e.headers.get("Retry-After", 60))  # Wait for the time suggested by the error, default 60s
            time.sleep(time_to_wait)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            break

# Walk through the directory and find all .txt files
for root, dirs, files in os.walk('./data/playlist_PL9fPq3eQfaaDLMTtVZDqq4aoU97NhZFP9'):
    for file in files:
        if file.endswith('transcript.txt'):
            file_path = os.path.join(root, file)
            print(f"Processing file: {file_path}")
            
            # Load the txt file
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

            # Send text to OpenAI API to summarize
            summary = summarize_text(text)
            
            if summary:
                # Create the summary file path
                summary_file_path = os.path.join(root, file.replace('.txt', '_summary.txt'))
                
                # Write the summary to the summary file
                with open(summary_file_path, 'w', encoding='utf-8') as summary_file:
                    summary_file.write(summary)
                
                print(f"Summary saved to: {summary_file_path}\n")

print("All summaries have been saved.")
