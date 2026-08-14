#!/usr/bin/env python3
import os
import sys

def is_gb2312(data):
    """Check if data is GB2312 encoded (not already UTF-8)"""
    try:
        text = data.decode('gb2312')
        # If it decodes successfully with gb2312, it might be gb2312
        # But we need to be careful - utf-8 might also decode
        return True
    except:
        return False

def convert_file(filepath):
    """Convert file from GB2312 to UTF-8 without BOM if needed"""
    with open(filepath, 'rb') as f:
        data = f.read()
    
    # Try to detect if it's GB2312 (not UTF-8, not already UTF-8 without BOM)
    try:
        # Try decoding as UTF-8 first
        text = data.decode('utf-8')
        # Check if it has BOM
        if data.startswith(b'\xef\xbb\xbf'):
            # Already UTF-8 with BOM - remove BOM
            text = text[1:]
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                f.write(text)
            print(f"Removed BOM from: {filepath}")
            return
        else:
            # Already UTF-8 without BOM - no conversion needed
            print(f"Already UTF-8 (no BOM): {filepath}")
            return
    except UnicodeDecodeError:
        pass
    
    # Try GB2312
    try:
        text = data.decode('gb2312')
        # Convert to UTF-8 without BOM
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            f.write(text)
        print(f"Converted GB2312 to UTF-8: {filepath}")
        return
    except:
        pass
    
    # Try GBK (common alternative)
    try:
        text = data.decode('gbk')
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            f.write(text)
        print(f"Converted GBK to UTF-8: {filepath}")
        return
    except:
        pass
    
    print(f"Skipped (unknown encoding): {filepath}")

# Find all matching files
directory = os.getcwd()
target_patterns = ['overview.html', 'stringtable.csv', 'briefing.html']

files_converted = 0
files_skipped = 0

for root, dirs, files in os.walk(directory):
    for fname in files:
        if fname in target_patterns:
            filepath = os.path.join(root, fname)
            convert_file(filepath)
            files_converted += 1

print(f"\nDone. Processed files in: {directory}")