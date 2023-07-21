import os
import json
from html import unescape

def convert_format_a_to_b(json_a_file, jsonl_b_file, name):
    replacements = {
        "<p>": "\n",
        "<strong>": "**",
        "</strong>": "**",
        "<em>": "*",
        "</em>": "*",
        "</p>": ""
        # Add more replacements as needed
    }
    
    with open(json_a_file, 'r') as f_a, open(jsonl_b_file, 'w') as f_b:
        data = json.load(f_a)
        messages = data['data']['message']
        
        for message in messages:
            role = message['role']
            text = message['data']
            
            for tag, replacement in replacements.items():
                text = text.replace(tag, replacement)
            
            cleaned_text = unescape(text.strip())
            
            formatted_message = {
                "name": name.capitalize(),
                "is_user": role == "user",
                "is_name": True,
                "send_date": "",  # You can add the appropriate send date/time if available
                "mes": cleaned_text,
                "extra": {}
            }
            
            f_b.write(json.dumps(formatted_message) + '\n')

def convert_directory(dir_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    converted_dir = os.path.join(script_dir, "converted_files")
    os.makedirs(converted_dir, exist_ok=True)
    
    for filename in os.listdir(dir_path):
        if filename.endswith('.json'):
            base_name = os.path.splitext(filename)[0]
            name = base_name.split('_', 1)[0]
            converted_file = f"{base_name}-converted.jsonl"
            json_a_file = os.path.join(dir_path, filename)
            jsonl_b_file = os.path.join(converted_dir, converted_file)
            convert_format_a_to_b(json_a_file, jsonl_b_file, name)

# Usage
convert_directory('chats')
