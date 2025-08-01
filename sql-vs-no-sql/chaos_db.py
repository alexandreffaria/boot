import time
import random
import sys
import json
import math

# Typing simulation
def type_line(line, newline=True, min_delay=0.001, max_delay=0.02):
    for char in line:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(random.uniform(min_delay, max_delay))
    if newline:
        print()

# Simulated user commands
time.sleep(0.2)
type_line(">> db.users.insert({name: 'John'})")
time.sleep(0.1)
type_line(">> db.users.insert({name: ['John', 'Johnny'], age: 'maybe'})")
time.sleep(0.2)
type_line(">> db.users.insert({age: true})")
time.sleep(0.25)
type_line("\n>> db.users.find()\n", newline=False)
time.sleep(.3)

# The actual documents returned
documents = [
    {"name": "John"},
    {"name": ["John", "Johnny"], "age": "maybe"},
    {"age": True},
    {"bio": float('nan'), "tags": 999, "profile": None},
    {"name": {"nested": "yes"}, "profile": "🧌"},
    {"active": {"deep": {"deeper": {"deepest": "help"}}}, "age": float('nan')}
]

# Custom JSON dump that handles NaN
def safe_json_dumps(obj):
    def default(o):
        if isinstance(o, float) and math.isnan(o):
            return "NaN"
        raise TypeError
    return json.dumps(obj, ensure_ascii=False, default=default)

# Print each document
for i, doc in enumerate(documents, 1):
    print(f"[{i:03}] {safe_json_dumps(doc)}")

