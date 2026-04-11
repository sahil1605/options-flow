import os
import re

def remove_chinese_punct_from_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        pattern = re.compile(r'[\u3000-\u303F\uFF00-\uFFEF]')
        new_content = pattern.sub('', content)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
            
    except Exception as e:
        pass
    return False

def main():
    modified_count = 0
    for root, dirs, files in os.walk('/Users/sahil/Documents/MiroFish-main'):
        if '.git' in root or 'node_modules' in root or '__pycache__' in root or '.venv' in root:
            continue
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.ico', '.webp', '.svg')):
                continue
            filepath = os.path.join(root, file)
            if remove_chinese_punct_from_file(filepath):
                modified_count += 1
                
    print(f"Removed Chinese punctuation from {modified_count} files.")

if __name__ == '__main__':
    main()
