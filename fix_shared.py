import os
import re

def fix_imports(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original = content
                content = re.sub(r'from src\.shared_kernel\.', 'from src.shared.', content)
                content = re.sub(r'import src\.shared_kernel\.', 'import src.shared.', content)
                
                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Fixed: {filepath}")

if __name__ == "__main__":
    fix_imports("src")
    print("Done!")
