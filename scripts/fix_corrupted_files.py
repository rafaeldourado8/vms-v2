"""Find and fix corrupted Python files with null bytes."""
import os
from pathlib import Path

def find_corrupted_files(root_dir):
    """Find Python files with null bytes."""
    corrupted = []
    for path in Path(root_dir).rglob("*.py"):
        try:
            with open(path, 'rb') as f:
                content = f.read()
                if b'\x00' in content:
                    corrupted.append(path)
        except Exception as e:
            print(f"Error reading {path}: {e}")
    return corrupted

def fix_file(path):
    """Fix corrupted file by creating empty or minimal content."""
    if path.name == "__init__.py":
        # Empty __init__.py
        with open(path, 'w', encoding='utf-8') as f:
            f.write('"""Package initialization."""\n')
        print(f"Fixed: {path}")
    else:
        print(f"MANUAL FIX NEEDED: {path}")

if __name__ == "__main__":
    src_dir = Path(__file__).parent.parent / "src"
    print(f"Scanning {src_dir}...")
    
    corrupted = find_corrupted_files(src_dir)
    
    if not corrupted:
        print("✅ No corrupted files found!")
    else:
        print(f"\n❌ Found {len(corrupted)} corrupted files:\n")
        for path in corrupted:
            print(f"  - {path}")
            if path.name == "__init__.py":
                fix_file(path)
        
        print(f"\n✅ Fixed {len([p for p in corrupted if p.name == '__init__.py'])} __init__.py files")
        
        other_files = [p for p in corrupted if p.name != "__init__.py"]
        if other_files:
            print(f"\n⚠️  {len(other_files)} other files need manual fix")
