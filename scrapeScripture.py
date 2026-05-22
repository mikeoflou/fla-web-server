import json
import os

def get_local_scripture(book_name, chapter_num):
    # Absolute path logic to ensure it finds the file
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, 'data-asv.json')
    
    if not os.path.exists(file_path):
        return f"System Error: Looked for {file_path} but it's not there."

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            bible_data = json.load(f)

        # 1. Check if the file was empty or invalid
        if not bible_data or not isinstance(bible_data, dict):
            return "Error: JSON file is empty or not a valid dictionary."

        # 2. Find the Book (Using 'books' key)
        # Note: If your JSON starts with 'verses' or a different key, change 'books' below
        books_list = bible_data.get('books', [])
        book = next((b for b in books_list if b['name'].lower() == book_name.lower()), None)
        
        if not book:
            return f"Book '{book_name}' not found."

        # 3. Find the Chapter
        chapter = next((c for c in book.get('chapters', []) if str(c['num']) == str(chapter_num)), None)
        
        if not chapter:
            return f"Chapter {chapter_num} not found in {book_name}."

        # 4. Build the text
        verses = [f"{v['num']} {v['text']}" for v in chapter.get('verses', [])]
        return " ".join(verses)

    except json.JSONDecodeError:
        return "Error: data-asv.json is empty or corrupted. Please check the file content."
    except Exception as e:
        return f"Unexpected Error: {str(e)}"

if __name__ == "__main__":
    content = get_local_scripture("Numbers", 27)
    print("--- Numbers 27 ---")
    print(content)