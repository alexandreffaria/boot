#!/usr/bin/env python3
import argparse
import keyboard
import time
import os
import sys
import random

def calculate_delay(wpm):
    """Calculate delay between keystrokes based on WPM."""
    # Average word length is ~5 characters
    # WPM = words per minute, so characters per minute = WPM * 5
    # Characters per second = characters per minute / 60
    # Delay between characters = 1 / characters per second
    return 60 / (wpm * 5)

def type_file_contents(file_path, wpm, humanize=True):
    """Type the contents of a file at the specified WPM rate."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print(f"Starting to type contents of {file_path} at {wpm} WPM...")
        print("Press Ctrl+C to stop typing at any time.")
        
        # Give the user time to switch to the target application
        for i in range(3, 0, -1):
            print(f"Starting in {i}...")
            time.sleep(1)
        
        base_delay = calculate_delay(wpm)
        
        for char in content:
            keyboard.write(char)
            
            # Add human-like typing variations if humanize is enabled
            if humanize:
                # Random variation in typing speed (±20%)
                variation = random.uniform(0.8, 1.2)
                # Longer pauses after punctuation
                if char in ['.', ',', ';', ':', '!', '?', '\n']:
                    time.sleep(base_delay * variation * 2)
                else:
                    time.sleep(base_delay * variation)
            else:
                time.sleep(base_delay)
                
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except KeyboardInterrupt:
        print("\nTyping stopped by user.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Type out file contents when F1 is pressed.')
    parser.add_argument('file', help='Path to the file to type')
    parser.add_argument('--wpm', type=int, default=60, help='Words per minute typing speed (default: 60)')
    parser.add_argument('--no-humanize', action='store_true', help='Disable human-like typing variations')
    
    args = parser.parse_args()
    
    if not os.path.isfile(args.file):
        print(f"Error: File '{args.file}' not found.")
        sys.exit(1)
    
    print(f"GodTyper initialized with file: {args.file}")
    print(f"WPM set to: {args.wpm}")
    print("Press F1 to start typing the file contents.")
    print("Press Ctrl+C to exit the program.")
    
    # Set up the F1 key handler
    keyboard.add_hotkey('f2', lambda: type_file_contents(args.file, args.wpm, not args.no_humanize))
    
    # Keep the program running until Ctrl+C is pressed
    try:
        keyboard.wait('ctrl+c')
    except KeyboardInterrupt:
        pass
    finally:
        print("\nExiting GodTyper.")

if __name__ == "__main__":
    main()