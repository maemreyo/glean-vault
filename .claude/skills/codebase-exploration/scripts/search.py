#!/usr/bin/env python3
"""
Codebase Exploration Search - Search and analyze codebase patterns
Usage: python search.py "<pattern>" [--type <type>] [--framework <framework>] [--output <format>]

Types: files, architecture, dependencies, patterns
Frameworks: react, vue, angular, express, fastapi, django
"""

import argparse
import json
from pathlib import Path
from core import ExplorationConfig, is_excluded, categorize_file, detect_architecture, analyze_dependencies

def search_files(pattern: str, search_type: str = None, max_results: int = 50) -> dict:
    """Search for files matching pattern"""
    config = ExplorationConfig()
    results = []

    # Convert pattern to regex
    if pattern.startswith('/') and pattern.endswith('/'):
        pattern = pattern[1:-1]
    else:
        pattern = pattern.replace('*', '.*')

    import re
    regex_pattern = re.compile(pattern, re.IGNORECASE)

    # Search current directory
    for file_path in Path('.').rglob('*'):
        if file_path.is_file() and not is_excluded(file_path):
            # Match pattern against file path or name
            if regex_pattern.search(str(file_path)) or regex_pattern.search(file_path.name):
                file_info = categorize_file(file_path, config)
                results.append(file_info)
                if len(results) >= max_results:
                    break

    return {
        'type': 'files',
        'pattern': pattern,
        'count': len(results),
        'results': results[:max_results]
    }

def search_architecture(max_results: int = 50) -> dict:
    """Analyze codebase architecture"""
    config = ExplorationConfig()
    all_files = []

    # Collect all files
    for file_path in Path('.').rglob('*'):
        if file_path.is_file() and not is_excluded(file_path):
            file_info = categorize_file(file_path, config)
            all_files.append(file_info)

    # Filter implementation files for architecture analysis
    impl_files = [f for f in all_files
                  if f['category'] in ['implementation', 'component', 'service', 'controller', 'model', 'entry']]

    architecture = detect_architecture(impl_files, config)

    return {
        'type': 'architecture',
        'count': len(impl_files),
        'results': [architecture],
        'all_files_count': len(all_files)
    }

def search_dependencies(framework: str = None, max_results: int = 30) -> dict:
    """Analyze dependencies"""
    config = ExplorationConfig()
    all_files = []

    # Collect all files
    for file_path in Path('.').rglob('*'):
        if file_path.is_file() and not is_excluded(file_path):
            file_info = categorize_file(file_path, config)
            all_files.append(file_info)

    # Filter files based on framework if specified
    if framework:
        framework_files = [f for f in all_files
                           if framework.lower() in f.get('frameworks', [])]
    else:
        framework_files = all_files

    dependencies = analyze_dependencies(framework_files)

    return {
        'type': 'dependencies',
        'framework': framework,
        'count': len(framework_files),
        'results': [dependencies]
    }

def search_patterns(pattern: str, max_results: int = 20) -> dict:
    """Search for specific code patterns"""
    import re

    config = ExplorationConfig()
    matches = []

    # Convert pattern to regex
    regex_pattern = re.compile(pattern, re.IGNORECASE)

    # Search in files
    for file_path in Path('.').rglob('*'):
        if file_path.is_file() and not is_excluded(file_path):
            try:
                file_info = categorize_file(file_path, config)

                # Read file and search for pattern
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()

                file_matches = []
                for i, line in enumerate(lines, 1):
                    if regex_pattern.search(line):
                        file_matches.append({
                            'line_number': i,
                            'content': line.strip(),
                            'context': get_line_context(lines, i)
                        })

                if file_matches:
                    matches.append({
                        'file': file_info,
                        'matches': file_matches[:5]  # Limit matches per file
                    })

                if len(matches) >= max_results:
                    break

            except Exception as e:
                print(f"Error searching {file_path}: {e}")

    return {
        'type': 'patterns',
        'pattern': pattern,
        'count': len(matches),
        'results': matches
    }

def get_line_context(lines: list, line_num: int, context_lines: int = 2) -> str:
    """Get context around a line"""
    start = max(0, line_num - context_lines - 1)
    end = min(len(lines), line_num + context_lines)
    context = [lines[i].rstrip() for i in range(start, end)]
    return '\n'.join(context)

def format_output(result: dict) -> str:
    """Format results for Claude consumption"""
    if 'error' in result:
        return f"Error: {result['error']}"

    output = []

    # Header
    search_type = result['type'].title()
    output.append(f"## Codebase Exploration - {search_type}")

    if result.get('pattern'):
        output.append(f"**Pattern:** {result['pattern']}")

    if result.get('framework'):
        output.append(f"**Framework:** {result['framework']}")

    output.append(f"**Found:** {result['count']} results\n")

    # Format based on type
    if result['type'] == 'files':
        output.append("### Matching Files:")
        for i, file_info in enumerate(result['results'], 1):
            output.append(f"\n#### {i}. {file_info['name']}")
            output.append(f"- **Path:** `{file_info['relative_path']}`")
            output.append(f"- **Category:** {file_info['category']}")
            output.append(f"- **Priority:** {file_info['priority']}")
            output.append(f"- **Size:** {file_info['size']:,} bytes")

    elif result['type'] == 'architecture':
        for arch in result['results']:
            output.append("\n### Architecture Pattern")
            output.append(f"- **Pattern:** {arch['pattern']}")
            output.append(f"- **Frameworks:** {', '.join(arch['frameworks'])}")
            output.append(f"- **Files analyzed:** {result['count']}")

            if arch['structure']:
                struct = arch['structure']
                output.append("\n#### Structure:")
                output.append(f"- **Top directories:** {list(struct['top_directories'].items())}")
                output.append(f"- **Categories:** {list(struct['files_by_category'].keys())}")

    elif result['type'] == 'dependencies':
        for deps in result['results']:
            output.append("\n### Dependency Analysis")
            summary = deps['summary']
            output.append(f"- **External dependencies:** {summary['total_external']}")
            output.append(f"- **Internal dependencies:** {summary['total_internal']}")

            if summary['most_used_external']:
                output.append("\n#### Most Used External:")
                for dep, count in summary['most_used_external']:
                    output.append(f"- **{dep}** ({count} imports)")

    elif result['type'] == 'patterns':
        output.append("### Pattern Matches:")
        for i, match in enumerate(result['results'], 1):
            file_info = match['file']
            output.append(f"\n#### {i}. {file_info['name']}")
            output.append(f"**File:** `{file_info['relative_path']}`")
            output.append(f"**Matches:** {len(match['matches'])}")

            for j, m in enumerate(match['matches'][:3], 1):  # Show first 3 matches
                output.append(f"\nMatch {j} (line {m['line_number']}):")
                output.append(f"`{m['content']}`")

    return '\n'.join(output)

def main():
    parser = argparse.ArgumentParser(description="Codebase Exploration Search")
    parser.add_argument("pattern", help="Search pattern (regex supported)")
    parser.add_argument("--type", "-t",
                       choices=['files', 'architecture', 'dependencies', 'patterns'],
                       default='files',
                       help="Type of search")
    parser.add_argument("--framework", "-f",
                       help="Filter by framework (react, vue, angular, etc.)")
    parser.add_argument("--max-results", "-n", type=int, default=50,
                       help="Maximum results (default: 50)")
    parser.add_argument("--json", action="store_true",
                       help="Output as JSON")

    args = parser.parse_args()

    # Perform search based on type
    if args.type == 'architecture':
        result = search_architecture(args.max_results)
    elif args.type == 'dependencies':
        result = search_dependencies(args.framework, args.max_results)
    elif args.type == 'patterns':
        result = search_patterns(args.pattern, args.max_results)
    else:  # files
        result = search_files(args.pattern, args.type, args.max_results)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_output(result))

if __name__ == "__main__":
    main()