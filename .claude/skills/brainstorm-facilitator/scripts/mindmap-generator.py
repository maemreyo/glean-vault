#!/usr/bin/env python3
"""
Mind Map Generator for Brainstorming Sessions
Generates visual mind maps from markdown text
"""

import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple

def parse_markdown_indents(text: str) -> List[Tuple[int, str]]:
    """Parse markdown indented list into (level, text) tuples."""
    lines = text.strip().split('\n')
    parsed = []

    for line in lines:
        if not line.strip():
            continue

        # Count leading spaces or tabs for level
        stripped = line.lstrip()
        if not stripped:
            continue

        # Count indent level
        indent_level = len(line) - len(stripped)
        level = indent_level // 2  # Assuming 2 spaces per level

        # Remove markdown markers
        cleaned = re.sub(r'^[-*+]\s*', '', stripped.strip())
        cleaned = re.sub(r'^\d+\.\s*', '', cleaned)
        cleaned = re.sub(r'^\#\s*', '', cleaned)

        if cleaned:
            parsed.append((level, cleaned))

    return parsed

def generate_mermaid_mindmap(parsed_items: List[Tuple[int, str]], title: str = "Mind Map") -> str:
    """Generate Mermaid mindmap syntax."""
    mermaid = ["mindmap"]
    mermaid.append(f"  root(({title}))")

    for level, text in parsed_items:
        indent = "  " * (level + 1)
        # Clean text for Mermaid
        clean_text = text.replace('"', '\\"').replace('(', '\\(').replace(')', '\\)')
        mermaid.append(f"{indent}{clean_text}")

    return "\n".join(mermaid)

def generate_plantuml_mindmap(parsed_items: List[Tuple[int, str]], title: str = "Mind Map") -> str:
    """Generate PlantUML mindmap syntax."""
    plantuml = ["@startmindmap"]
    plantuml.append(f"* {title}")

    current_level = 0
    for level, text in parsed_items:
        if level > current_level:
            plantuml.append("**" * (level - current_level) + " " + text)
        elif level < current_level:
            plantuml.append("*" * (current_level - level) + " " + text)
        else:
            plantuml.append(text)
        current_level = level

    plantuml.append("@endmindmap")
    return "\n".join(plantuml)

def generate_ascii_tree(parsed_items: List[Tuple[int, str]], title: str = "Mind Map") -> str:
    """Generate ASCII tree representation."""
    lines = [title]

    for level, text in parsed_items:
        prefix = "│   " * level
        if level == 0:
            lines.append(f"├── {text}")
        else:
            # Check if this is the last item at this level
            lines.append(f"{prefix}├── {text}")

    return "\n".join(lines)

def generate_dot_graph(parsed_items: List[Tuple[int, str]], title: str = "Mind Map") -> str:
    """Generate Graphviz DOT syntax."""
    dot = ["digraph mindmap {"]
    dot.append(f'  label="{title}";')
    dot.append('  labelloc=t;')
    dot.append('  fontsize=20;')
    dot.append('  node [shape=box, style=filled, fillcolor=lightblue];')

    # Create nodes
    node_id = 0
    nodes = []
    for level, text in parsed_items:
        node_id += 1
        safe_name = f"node_{node_id}"
        label = text.replace('"', '\\"')
        dot.append(f'  {safe_name} [label="{label}"];')
        nodes.append((level, safe_name))

    # Create edges
    parent_stack = []
    for level, node_id in nodes:
        # Clear stack if we're going up levels
        while len(parent_stack) > level:
            parent_stack.pop()

        if parent_stack:
            parent = parent_stack[-1]
            dot.append(f'  {parent} -> {node_id};')

        parent_stack.append(node_id)

    dot.append("}")
    return "\n".join(dot)

def generate_json_structure(parsed_items: List[Tuple[int, str]], title: str = "Mind Map") -> Dict:
    """Generate JSON structure of the mind map."""
    def build_tree(items: List[Tuple[int, str]]) -> List[Dict]:
        if not items:
            return []

        result = []
        i = 0

        while i < len(items):
            level, text = items[i]

            # Find children (higher level numbers)
            children = []
            j = i + 1
            while j < len(items) and items[j][0] > level:
                children.append(items[j])
                j += 1

            # Build node
            node = {
                "text": text,
                "level": level,
                "children": build_tree(children)
            }
            result.append(node)

            i = j

        return result

    return {
        "title": title,
        "nodes": build_tree(parsed_items)
    }

def main():
    parser = argparse.ArgumentParser(description="Generate mind maps from markdown")
    parser.add_argument("input", help="Input markdown file")
    parser.add_argument("-o", "--output", help="Output file (optional)")
    parser.add_argument("-f", "--format",
                       choices=["mermaid", "plantuml", "ascii", "dot", "json"],
                       default="mermaid",
                       help="Output format")
    parser.add_argument("-t", "--title", default="Mind Map",
                       help="Title for the mind map")

    args = parser.parse_args()

    # Read input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{args.input}' not found")
        return 1

    with open(input_path, 'r') as f:
        content = f.read()

    # Parse markdown
    parsed = parse_markdown_indents(content)

    # Generate output
    if args.format == "mermaid":
        output = generate_mermaid_mindmap(parsed, args.title)
    elif args.format == "plantuml":
        output = generate_plantuml_mindmap(parsed, args.title)
    elif args.format == "ascii":
        output = generate_ascii_tree(parsed, args.title)
    elif args.format == "dot":
        output = generate_dot_graph(parsed, args.title)
    elif args.format == "json":
        import json
        output = json.dumps(generate_json_structure(parsed, args.title), indent=2)

    # Write output
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w') as f:
            f.write(output)
        print(f"Mind map saved to: {output_path}")
    else:
        print(output)

    return 0

if __name__ == "__main__":
    exit(main())