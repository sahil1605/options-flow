import os
import re
import time
from deep_translator import GoogleTranslator

def translate_chinese(text_cache, text):
    if not text.strip():
        return text
    if text in text_cache:
        return text_cache[text]
    
    try:
        translated = GoogleTranslator(source='zh-CN', target='en').translate(text)
        time.sleep(0.1) # Be nice to the API
        if translated:
            text_cache[text] = translated
            return translated
    except Exception as e:
        print(f"Failed to translate: {text[:20]}... Error: {e}")
    # Fallback to original if translation fails
    return text

def process_file(filepath, text_cache):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return False
        
    # Find chunks of text containing Chinese characters.
    # This regex looks for substrings that contain Han characters,
    # including punctuation like 「」【】！？，。, but tries not to grab surrounding English code.
    pattern = re.compile(r'([\u4e00-\u9fa5][\u4e00-\u9fa5\u3000-\u303F\uFF00-\uFFEF0-9A-Za-z\s]*[\u4e00-\u9fa5]+|[\u4e00-\u9fa5])')
    
    # Alternatively, just match lines that have Chinese and translate the Chinese parts
    # Better yet: extract matches, translate, and replace
    matches = pattern.findall(content)
    if not matches:
        return False
        
    # Sort matches by length descending to avoid partial replacements!
    matches = list(set(matches))
    matches.sort(key=len, reverse=True)
    
    new_content = content
    modified = False
    
    for match in matches:
        if not match.strip():
            continue
        
        translated_chunk = translate_chinese(text_cache, match)
        if translated_chunk and translated_chunk != match:
            # We replace exactly the old text with the new one
            new_content = new_content.replace(match, translated_chunk)
            modified = True
            
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    print("Installing requirements if necessary...")
    # Optional: ensure it's installed
    try:
        import deep_translator
    except ImportError:
        os.system("pip install deep-translator")
        
    print("Starting translation...")
    text_cache = {}
    modified_count = 0
    total_files = 0
    
    for root, dirs, files in os.walk('/Users/sahil/Documents/MiroFish-main'):
        if any(skip in root for skip in ['.git', 'node_modules', '__pycache__', '.venv', 'dist', 'build']):
            continue
            
        for file in files:
            # Skip media and binary files
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.ico', '.webp', '.svg', '.pyc')):
                continue
                
            filepath = os.path.join(root, file)
            total_files += 1
            if process_file(filepath, text_cache):
                modified_count += 1
                print(f"Translated: {os.path.relpath(filepath, '/Users/sahil/Documents/MiroFish-main')}")
                
    print(f"\nDone! Translated {modified_count} out of {total_files} scanned files.")

if __name__ == '__main__':
    main()
