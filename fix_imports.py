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
                content = re.sub(r'from src\.admin\.', 'from src.modules.admin.', content)
                content = re.sub(r'import src\.admin\.', 'import src.modules.admin.', content)
                content = re.sub(r'from src\.cidades\.', 'from src.modules.cidades.', content)
                content = re.sub(r'import src\.cidades\.', 'import src.modules.cidades.', content)
                
                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Fixed: {filepath}")

if __name__ == "__main__":
    fix_imports("src/modules")
    print("Done!")
