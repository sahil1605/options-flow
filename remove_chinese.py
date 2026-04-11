import os
import re

def remove_chinese_from_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Regex to match Chinese characters
        # Matches Han ideographs, but leaves English, code, etc.
        pattern = re.compile(r'[\u4e00-\u9fa5]+')
        
        # We also want to match Chinese punctuation if needed, e.g. 
        punct_pattern = re.compile(r'[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]')
        
        new_content = pattern.sub('', content)
        new_content = punct_pattern.sub('', new_content)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
            
    except Exception as e:
        # Ignore binary files or files with encoding issues
        pass
    return False

def main():
    modified_count = 0
    # Walk the directory
    for root, dirs, files in os.walk('/Users/sahil/Documents/MiroFish-main'):
        # Skip .git and some other hidden dirs to be safe
        if '.git' in root or 'node_modules' in root or '__pycache__' in root or '.venv' in root:
            continue
            
        for file in files:
            # Skip images and binaries
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.ico', '.webp', '.svg')):
                continue
                
            filepath = os.path.join(root, file)
            if remove_chinese_from_file(filepath):
                modified_count += 1
                
    print(f"Removed Chinese characters from {modified_count} files.")

if __name__ == '__main__':
    main()
