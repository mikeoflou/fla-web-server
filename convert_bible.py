import json
import os

def fix_and_overwrite_bible():
    input_file = 'data-asvCopy.json'
    output_file = 'data-asv.json'
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        return

    print("Reading and converting data...")
    
    verses_list = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Splits the line by the tab character: 'Genesis 1:1\tIn the beginning...'
            parts = line.strip().split('\t')
            if len(parts) < 2:
                continue
                
            ref, text = parts[0], parts[1]
            
            # We ONLY want Numbers 27 for this week's newsletter
            if ref.startswith("Numbers 27:"):
                # Clean up the text and add to our list
                verses_list.append(f"{ref.split(':')[-1]} {text}")

    # Overwrite the data-asv.json with JUST the list of verses
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(verses_list, f, indent=4)
    
    print(f"Success! {output_file} now contains {len(verses_list)} verses from Numbers 27.")

if __name__ == "__main__":
    fix_and_overwrite_bible()