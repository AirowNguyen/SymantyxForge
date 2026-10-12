import os
import sys
import re

def parse_tree(tree_text):
    lines = tree_text.splitlines()
    paths = []

    stack = []

    for line in lines:
        # Remove drawing characters
        clean = re.sub(r"[├─│└ ]+", "", line).strip()
        if not clean:
            continue

        depth = (len(line) - len(line.lstrip())) // 4

        # Adjust stack to current depth
        stack = stack[:depth]
        stack.append(clean)

        paths.append("/".join(stack))

    return paths

def build(paths):
    for p in paths:
        if "." in os.path.basename(p):
            # It's a file
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w") as f:
                f.write(f"# {os.path.basename(p)}\nGenerated automatically.\n")
            print("Created file:", p)
        else:
            # It's a directory
            os.makedirs(p, exist_ok=True)
            print("Created directory:", p)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build_from_tree.py \"ASCII TREE HERE\"")
        sys.exit(1)

    tree = sys.argv[1]
    paths = parse_tree(tree)
    build(paths)