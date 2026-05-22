import json
import os
import re

def extract_clean_verses():
    input_file = os.path.join(os.path.dirname(__file__), 'data-asvCopy.json')
    output_file = os.path.join(os.path.dirname(__file__), 'data-asv.json')

    if not os.path.exists(input_file):
        print(f"Error: Could not find {input_file}")
        return

    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Find Numbers 27 verses
        pattern = re.compile(r"Numbers\s*27:(\d+)\s*(.*?)(?=Numbers\s*27:|\"|\]|$)", re.DOTALL)
        matches = pattern.findall(content)

        verses_dict = {}
        for v_num, v_text in matches:
            # CLEANING LOGIC: This removes the quotes and extra spaces
            clean_text = v_text.strip().replace('\\"', '"').replace('"', '').replace(',', '')
            
            # We save ONLY the text, not the "Numbers 27:" part
            if v_num not in verses_dict:
                verses_dict[v_num] = f"{v_num} {clean_text}"

        # Sort and save
        final_verses = [verses_dict[n] for n in sorted(verses_dict.keys(), key=int)]

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_verses, f, indent=2)

        print(f"Success! {len(final_verses)} verses saved without the 'Numbers 27:' prefix.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    extract_clean_verses()