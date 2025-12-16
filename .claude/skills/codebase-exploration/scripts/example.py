#!/usr/bin/env python3
"""
Example usage of codebase exploration search utilities
"""

from search import search_files, search_architecture, search_patterns

def main():
    print("=== Codebase Exploration Examples ===\n")

    # Example 1: Search for authentication-related files
    print("1. Searching for authentication files...")
    result = search_files("auth", max_results=5)
    for file in result['results']:
        print(f"  - {file['name']} ({file['category']})")

    # Example 2: Analyze architecture
    print("\n2. Analyzing architecture...")
    arch_result = search_architecture()
    print(f"  Architecture pattern: {arch_result['results'][0]['pattern']}")
    print(f"  Frameworks detected: {', '.join(arch_result['results'][0]['frameworks'])}")

    # Example 3: Search for TODO comments
    print("\n3. Searching for TODO comments...")
    todo_result = search_patterns("TODO|FIXME|XXX|HACK", max_results=3)
    for match in todo_result['results']:
        print(f"  File: {match['file']['name']}")
        for m in match['matches'][:2]:
            print(f"    Line {m['line_number']}: {m['content']}")

if __name__ == "__main__":
    main()