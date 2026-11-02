import random

# Constants
MAX_LEVEL = 4  
P = 0.5  

# Initialize Skip List
def create_skip_list():
    return {"head": {"key": -1, "value": None, "forward": [None] * MAX_LEVEL}, "level": 1}

# Generate random level for a new node
def random_level():
    lvl = 1
    while random.random() < P and lvl < MAX_LEVEL:
        lvl += 1
    return lvl

# Insert a book into the Skip List
def insert(skip_list, key, value):
    update = [None] * MAX_LEVEL
    current = skip_list["head"]

    for i in range(skip_list["level"] - 1, -1, -1):
        while current["forward"][i] and current["forward"][i]["key"] < key:
            current = current["forward"][i]
        update[i] = current

    new_level = random_level()
    if new_level > skip_list["level"]:
        for i in range(skip_list["level"], new_level):
            update[i] = skip_list["head"]
        skip_list["level"] = new_level

    new_node = {"key": key, "value": value, "forward": [None] * new_level}
    for i in range(new_level):
        new_node["forward"][i] = update[i]["forward"][i]
        update[i]["forward"][i] = new_node

# Search for a book in the Skip List
def search(skip_list, key):
    current = skip_list["head"]
    for i in range(skip_list["level"] - 1, -1, -1):
        while current["forward"][i] and current["forward"][i]["key"] < key:
            current = current["forward"][i]
    current = current["forward"][0]

    if current and current["key"] == key:
        return current["value"]
    return None

# Display Skip List
def display(skip_list):
    print("\nSkip List Structure:")
    for lvl in range(skip_list["level"]):
        node = skip_list["head"]["forward"][lvl]
        level_nodes = []
        while node:
            level_nodes.append(f"{node['key']}")
            node = node["forward"][lvl]
        print(f"Level {lvl}: {' -> '.join(level_nodes)}")
