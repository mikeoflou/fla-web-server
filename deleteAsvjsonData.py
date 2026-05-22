import json
import os
import re

def fix_data_asv():
    # This is the file we are wiping and fixing
    file_path = os.path.join(os.path.dirname(__file__), 'data-asv.json')
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    print(f"Wiping corrupted data and extracting Numbers 27 into {file_path}...")

    try:
        # 1. Read the file as raw text first (since the JSON is broken)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            raw_content = f.read()

        # 2. Find every instance of Numbers 27
        # This regex finds "Numbers 27:1", "Numbers 27:2", etc.
        pattern = re.compile(r"Numbers\s*27:(\d+)\s*(.*?)(?=Numbers\s*27:|\"|\]|$)", re.DOTALL)
        matches = pattern.findall(raw_content)

        verses_dict = {}
        for v_num, v_text in matches:
            # Clean up the text (remove extra quotes and backslashes)
            clean_text = v_text.strip().replace('\\"', '"').replace('"', '')
            # Using a dictionary automatically deletes all those "repeated" copies
            if v_num not in verses_dict:
                verses_dict[v_num] = f"Numbers 27:{v_num} {clean_text}"

        # 3. Sort the verses so they are in order (1, 2, 3...)
        final_list = [verses_dict[n] for n in sorted(verses_dict.keys(), key=int)]

        if not final_list:
            print("Could not find any Numbers 27 verses to save.")
            return

        # 4. OVERWRITE: 'w' mode deletes the old mess and starts fresh
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(final_list, f, indent=2)

        print(f"Success! Deleted the mess and saved {len(final_list)} clean verses.")

    except Exception as e:
        print(f"Error fixing the file: {e}")

if __name__ == "__main__":
    fix_data_asv()