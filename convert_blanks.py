import os
import re

# This regex finds 3 or more underscores
pattern = re.compile(r'_{3,}')

# This is the input box HTML we want to replace them with
input_box = '<input type="text" class="save-input" style="width: 200px; border: none; border-bottom: 2px solid #555; background: transparent; font-size: 1em; outline: none; margin: 0 5px;">'

for filename in os.listdir('.'):
    if filename.endswith('.json'):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace underscores with the input box
        new_content = pattern.sub(input_box, content)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Converted blanks in {filename}")