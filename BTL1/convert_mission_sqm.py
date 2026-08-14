#!/usr/bin/env python3
import os

directory = os.getcwd()
target_file = 'mission.sqm'

files_converted = 0

for root, dirs, files in os.walk(directory):
    for fname in files:
        if fname == target_file:
            filepath = os.path.join(root, fname)
            with open(filepath, 'rb') as f:
                data = f.read()
            
            try:
                text = data.decode('gbk')
                with open(filepath, 'w', encoding='utf-8', newline='') as f:
                    f.write(text)
                # Remove BOM if present
                if data.startswith(b'\xef\xbb\xbf'):
                    pass  # Already handled by write in utf-8 which doesn't add BOM by default
                print(f"Converted: {filepath}")
                files_converted += 1
            except UnicodeDecodeError:
                print(f"Skipped (not GBK): {filepath}")

print(f"\nDone. Converted {files_converted} mission.sqm files.")