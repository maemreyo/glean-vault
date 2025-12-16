#!/usr/bin/env python3
"""
Codebase Exploration Core Utilities
Shared functionality for codebase exploration analysis
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
DEFAULT_EXCLUDE_PATTERNS = [
    "node_modules", ".git", "dist", "build", ".next", "coverage",
    ".pytest_cache", "__pycache__", ".venv", "venv", "target"
]

class ExplorationConfig:
    """Configuration for codebase exploration"""

    def __init__(self):
        self.file_extensions = {
            'typescript': ['.ts', '.tsx'],
            'javascript': ['.js', '.jsx', '.mjs', '.cjs'],
            'python': ['.py'],
            'java': ['.java'],
            'go': ['.go'],
            'rust': ['.rs'],
            'csharp': ['.cs'],
            'php': ['.php'],
            'ruby': ['.rb'],
            'html': ['.html', '.htm'],
            'css': ['.css', '.scss', '.sass', '.less'],
            'json': ['.json'],
            'yaml': ['.yml', '.yaml'],
            'markdown': ['.md', '.mdx'],
            'config': ['.config.js', '.config.ts', '.env.example']
        }

        self.pattern_priorities = {
            'high': [
                r'index\.(ts|tsx|js|jsx)$',      # Entry points
                r'main\.(ts|tsx|js|jsx)$',       # Main files
                r'app\.(ts|tsx|js|jsx)$',       # App files
                r'.*Controller\.(ts|js)$',       # Controllers
                r'.*Service\.(ts|js)$',          # Services
                r'.*Model\.(ts|js)$',            # Models
                r'.*Component\.(tsx|jsx)$',     # React components
                r'.*(config|settings)\.(ts|js)$' # Config files
            ],
            'medium': [
                r'.*Hook\.(ts|js)$',             # Custom hooks
                r'.*Utils?\.(ts|js)$',          # Utilities
                r'.*Helper\.(ts|js)$',           # Helpers
                r'.*Types?\.(ts|d\.ts)$',        # Type definitions
                r'.*Interface\.(ts|d\.ts)$'     # Interfaces
            ],
            'low': [
                r'.*test\.(ts|tsx|js|jsx)$',     # Tests
                r'.*spec\.(ts|tsx|js|jsx)$',     # Specs
                r'.*\.test\.(py|java|go)$'        # Test files in other languages
            ]
        }

        self.architecture_patterns = {
            'feature_based': [
                r'features?/', r'modules?/', r'domains/'
            ],
            'layered': [
                r'controllers/', r'services/', r'models/', r'repositories/'
            ],
            'mvc': [
                r'model/', r'view/', r'controller/'
            ],
            'clean': [
                r'usecases?/', r'entities/', r'interfaces/', r'infrastructure/'
            ]
        }

        self.framework_patterns = {
            'react': [
                r'use[A-Z][a-zA-Z]*\(\)',          # React hooks
                r'import.*React',                 # React imports
                r'from\s+[\'"]react',              # React from import
                r'export.*function\s+[A-Z]',      # React component
                r'<[A-Z][a-zA-Z]*',               # JSX tags
                r'\.tsx?$',                       # TypeScript React files
            ],
            'vue': [
                r'export default\s*{',            # Vue component export
                r'<template>',                    # Vue template tag
                r'<script>',                      # Vue script tag
                r'vue-router',                    # Vue Router
                r'pinia',                         # Pinia store
                r'Composition API',              # Vue 3 Composition API
            ],
            'angular': [
                r'@Component',                    # Angular component decorator
                r'@Injectable',                   # Angular injectable
                r'ngOnInit',                      # Angular lifecycle
                r'HttpClient',                    # Angular HTTP client
                r'RouterModule',                 # Angular router
            ],
            'express': [
                r'require\([\'"]express[\'"]\)',   # Express require
                r'import.*express',               # Express import
                r'app\.get\(',                   # Express routes
                r'app\.post\(',                  # Express routes
                r'middleware',                    # Express middleware
            ],
            'fastapi': [
                r'from fastapi import',            # FastAPI imports
                r'@app\.',                         # FastAPI decorator
                r'BaseModel',                      # Pydantic BaseModel
                r'Depends',                       # FastAPI dependency injection
                r'async def',                     # Async functions
            ],
            'django': [
                r'from django\.',                 # Django imports
                r'forms\.ModelForm',              # Django forms
                r'models\.Model',                 # Django models
                r'render\(',                       # Django render
                r'HttpResponse',                  # Django responses
            ]
        }

def is_excluded(path: Path, exclude_patterns: List[str] = None) -> bool:
    """Check if path should be excluded from exploration"""
    exclude_patterns = exclude_patterns or DEFAULT_EXCLUDE_PATTERNS

    path_str = str(path)
    for pattern in exclude_patterns:
        if pattern in path_str or path_str.endswith(pattern):
            return True
    return False

def categorize_file(file_path: Path, config: ExplorationConfig) -> Dict[str, Any]:
    """Categorize a file based on its path and content patterns"""
    file_info = {
        'path': str(file_path),
        'name': file_path.name,
        'extension': file_path.suffix,
        'directory': str(file_path.parent),
        'relative_path': str(file_path.relative_to(Path.cwd())),
        'category': 'unknown',
        'priority': 'medium',
        'size': 0
    }

    # Get file size
    try:
        file_info['size'] = file_path.stat().st_size
    except:
        pass

    # Determine category based on path
    path_parts = file_path.parts
    path_lower = str(file_path).lower()

    # Category detection
    if 'test' in path_lower or 'spec' in path_lower:
        file_info['category'] = 'test'
    elif 'docs' in path_lower or 'documentation' in path_lower:
        file_info['category'] = 'documentation'
    elif 'config' in path_lower or 'settings' in path_lower:
        file_info['category'] = 'config'
    elif file_info['extension'] in ['.ts', '.tsx', '.js', '.jsx', '.py']:
        if 'component' in path_lower or 'components' in path_lower:
            file_info['category'] = 'component'
        elif 'service' in path_lower or 'services' in path_lower:
            file_info['category'] = 'service'
        elif 'controller' in path_lower or 'controllers' in path_lower:
            file_info['category'] = 'controller'
        elif 'model' in path_lower or 'models' in path_lower:
            file_info['category'] = 'model'
        elif 'hook' in path_lower or 'hooks' in path_lower:
            file_info['category'] = 'hook'
        elif 'util' in path_lower or 'utils' in path_lower:
            file_info['category'] = 'utility'
        elif 'type' in path_lower or file_info['name'].endswith('.d.ts'):
            file_info['category'] = 'type'
        elif file_path.name in ['index.ts', 'index.js', 'index.tsx', 'index.jsx', 'main.ts', 'main.js', 'app.ts', 'app.js', 'app.tsx', 'app.jsx']:
            file_info['category'] = 'entry'
        else:
            file_info['category'] = 'implementation'
    else:
        file_info['category'] = 'other'

    # Determine priority based on patterns
    for priority, patterns in config.pattern_priorities.items():
        for pattern in patterns:
            if re.search(pattern, file_info['name']):
                file_info['priority'] = priority
                break

    return file_info

def detect_architecture(files: List[Dict[str, Any]], config: ExplorationConfig) -> Dict[str, Any]:
    """Detect architectural pattern from file structure"""
    architecture = {
        'pattern': 'unknown',
        'frameworks': [],
        'structure': {},
        'evidence': []
    }

    # Collect all paths
    all_paths = [f['relative_path'] for f in files]

    # Detect architecture pattern
    for pattern_name, patterns in config.architecture_patterns.items():
        for pattern in patterns:
            if any(re.search(pattern, path) for path in all_paths):
                architecture['pattern'] = pattern_name
                architecture['evidence'].append(f"Found {pattern} in file structure")
                break
        if architecture['pattern'] != 'unknown':
            break

    # Detect frameworks
    # Read a sample of files to detect framework usage
    sample_size = min(10, len(files))
    for file_info in files[:sample_size]:
        if file_info['category'] == 'implementation':
            file_path = Path(file_info['path'])
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(2000)  # Read first 2KB

                    for framework, patterns in config.framework_patterns.items():
                        for pattern in patterns:
                            if re.search(pattern, content):
                                if framework not in architecture['frameworks']:
                                    architecture['frameworks'].append(framework)
                                    architecture['evidence'].append(f"Detected {framework} in {file_info['name']}")
                                break
                except:
                    pass

    # Analyze structure
    directory_counts = {}
    for file_info in files:
        parts = Path(file_info['relative_path']).parts
        if len(parts) > 1:
            top_dir = parts[0]
            directory_counts[top_dir] = directory_counts.get(top_dir, 0) + 1

    architecture['structure'] = {
        'top_directories': directory_counts,
        'total_files': len(files),
        'files_by_category': {}
    }

    # Count files by category
    for file_info in files:
        category = file_info['category']
        if category not in architecture['structure']['files_by_category']:
            architecture['structure']['files_by_category'][category] = []
        architecture['structure']['files_by_category'][category].append(file_info['name'])

    return architecture

def analyze_dependencies(files: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze dependencies from import statements"""
    dependencies = {
        'external': {},  # npm packages, pip packages
        'internal': set(), # Local imports
        'frameworks': set(), # Framework-specific dependencies
        'summary': {
            'total_external': 0,
            'total_internal': 0,
            'most_used_external': [],
            'most_used_internal': []
        }
    }

    # Sample files for dependency analysis
    sample_size = min(20, len(files))
    implementation_files = [f for f in files[:sample_size]
                            if f['category'] in ['implementation', 'component', 'service']]

    for file_info in implementation_files:
        file_path = Path(file_info['path'])
        if not file_path.exists():
            continue

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Extract imports based on file type
            if file_path.suffix in ['.ts', '.tsx', '.js', '.jsx']:
                # JavaScript/TypeScript imports
                imports = re.findall(r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]', content)
                for imp in imports:
                    if not imp.startswith('.') and not imp.startswith('/'):
                        if imp not in dependencies['external']:
                            dependencies['external'][imp] = 0
                        dependencies['external'][imp] += 1

                # Local imports
                local_imports = re.findall(r'import\s+.*?\s+from\s+[\'"](\.|\.\./|@/)', content)
                dependencies['internal'].update(local_imports)

            elif file_path.suffix == '.py':
                # Python imports
                imports = re.findall(r'from\s+([^\s]+)\s+import', content)
                for imp in imports:
                    if not imp.startswith('.') and '.' in imp:
                        if imp not in dependencies['external']:
                            dependencies['external'][imp] = 0
                        dependencies['external'][imp] += 1

                local_imports = re.findall(r'import\s+([^\s]+)(?:\s+as\s+[^\s]+)?$', content)
                for imp in local_imports:
                    if imp.startswith('.'):
                        dependencies['internal'].add(imp)

        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")

    # Calculate summary
    dependencies['summary']['total_external'] = len(dependencies['external'])
    dependencies['summary']['total_internal'] = len(dependencies['internal'])

    # Most used external dependencies
    sorted_external = sorted(dependencies['external'].items(),
                            key=lambda x: x[1], reverse=True)[:10]
    dependencies['summary']['most_used_external'] = sorted_external

    # Convert internal set to list
    dependencies['internal'] = list(dependencies['internal'])

    return dependencies

def generate_report(data: Dict[str, Any]) -> str:
    """Generate a formatted report from analysis data"""
    report = []

    if 'files' in data:
        report.append("## File Analysis")
        report.append(f"Total files found: {len(data['files'])}")

        # Files by category
        categories = {}
        for file_info in data['files']:
            cat = file_info['category']
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += 1

        report.append("\n### Files by Category:")
        for category, count in sorted(categories.items()):
            report.append(f"- {category}: {count} files")

    if 'architecture' in data:
        arch = data['architecture']
        report.append("\n## Architecture Analysis")
        report.append(f"Pattern detected: {arch['pattern']}")
        report.append(f"Frameworks: {', '.join(arch['frameworks'])}")

        if arch['evidence']:
            report.append("\n### Evidence:")
            for evidence in arch['evidence']:
                report.append(f"- {evidence}")

    if 'dependencies' in data:
        deps = data['dependencies']
        report.append("\n## Dependencies")

        report.append(f"External dependencies: {deps['summary']['total_external']}")
        if deps['summary']['most_used_external']:
            report.append("\n### Most Used External:")
            for dep, count in deps['summary']['most_used_external'][:5]:
                report.append(f"- {dep}: {count} imports")

        report.append(f"\nInternal dependencies: {deps['summary']['total_internal']}")

    return "\n".join(report)