#!/usr/bin/env python3
"""
Remove all emoji characters from Python files systematically.
"""
import os
import re
from pathlib import Path

def remove_emojis_from_file(filepath):
    """Remove all emoji characters from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Define emoji patterns to remove
        emoji_replacements = {
            '': '',  # wrench
            '': '',  # siren
            '': '',  # bar chart
            '': '',  # trending up
            '': '',  # arrows
            '': '',  # magnifying glass
            '': '',  # rocket
            '': '',  # floppy disk
            '': '',  # clipboard
            '': '',   # exclamation
            '': '',  # robot
            '': '',  # stopwatch
            '': '',   # info
            '': '',  # hospital
            '': '',  # plug
            '': '',  # bulb
            '': '',  # prohibited
            '': '',  # snail
            '': '',   # lightning
            '': '',  # party
            '': '',  # explosion
            '': '',   # without space
            '': '',   # without space
            '': '',   # without space
            '': '',   # without space
            '': '',   # without space
            '': '',   # without space
            '': '',   # without space
            '': '',   # without space
            '': '',   # without space
            '': '',    # without space
            '': '',   # without space
            '': '',   # without space
            '': '',    # without space
            '': '',   # without space
            '': '',   # without space
            '': '',   # without space
            '': '',   # without space
            '': '',   # without space
            '': '',    # without space
            '': '',   # without space
            '': '',   # without space
            '': '',   # X mark
            '': '',   # checkmark
        }
        
        # Apply replacements
        for emoji, replacement in emoji_replacements.items():
            content = content.replace(emoji, replacement)
        
        # Remove any remaining emojis using regex (Unicode emoji ranges)
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002600-\U000027BF"  # miscellaneous symbols
            "\U0000FE00-\U0000FE0F"  # variation selectors
            "\U0000200D"             # zero width joiner
            "\U00002000-\U0000206F"  # general punctuation
            "]+", flags=re.UNICODE
        )
        content = emoji_pattern.sub('', content)
        
        # Write back if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Remove emojis from all Python files."""
    base_dir = Path('.')
    modified_files = []
    
    # Find all Python files
    python_files = list(base_dir.rglob('*.py'))
    
    for py_file in python_files:
        if remove_emojis_from_file(py_file):
            modified_files.append(str(py_file))
    
    print(f"Modified {len(modified_files)} files:")
    for file in modified_files:
        print(f"  - {file}")

if __name__ == "__main__":
    main()