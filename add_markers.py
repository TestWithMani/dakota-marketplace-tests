"""
Script to add pytest markers to all test files.
This script adds:
1. Tab marker (e.g., @pytest.mark.accounts) - runs all 6 test cases for a specific tab
2. Suite marker (e.g., @pytest.mark.column_names) - runs all tests in a specific suite
"""
import os
import re

# Test directories and their corresponding suite markers
test_dirs = {
    'all_tabs_column_name': 'column_names',
    'all_tabs_fields_comparison': 'fields_comparison',
    'all_tabs_fields_display_functionality': 'fields_display',
    'all_tabs_lazy_loading': 'lazy_loading',
    'all_tabs_list_view_crud': 'list_view_crud',
    'all_tabs_pin_unpin_functionality': 'pin_unpin'
}

def extract_tab_name(filename):
    """Extract tab name from filename."""
    # Pattern 1: test_<tab_name>_tab_<suite_type>.py
    match = re.search(r'test_([^_]+(?:_[^_]+)*)_tab_', filename)
    if match:
        return match.group(1)
    
    # Pattern 2: test_<tab_name>_<suite_type>.py (without _tab_)
    # Remove suite suffixes
    suite_suffixes = [
        '_column', '_fields_comparison', '_fields_display', 
        '_lazy_loading', '_list_view_crud', '_pin_unpin_functionality',
        '_default_fields_display'
    ]
    name = filename.replace('test_', '').replace('.py', '')
    for suffix in suite_suffixes:
        if name.endswith(suffix):
            tab_name = name[:-len(suffix)]
            return tab_name
    
    return None

def normalize_tab_name(tab_name):
    """Normalize tab name for marker (replace underscores, make lowercase)."""
    return tab_name.lower().replace(' ', '_')

def add_markers_to_file(filepath, tab_marker, suite_marker):
    """Add markers to a test file if they don't already exist."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Check if markers already exist
    content = ''.join(lines)
    if f'@pytest.mark.{tab_marker}' in content and f'@pytest.mark.{suite_marker}' in content:
        return False
    
    # Check if pytest is imported
    has_pytest_import = any('import pytest' in line or 'from pytest' in line for line in lines)
    
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a test function definition
        if re.match(r'^\s*def test_', line):
            # Check if markers already exist for this function
            # Look backwards for decorators
            j = i - 1
            has_tab_marker = False
            has_suite_marker = False
            
            while j >= 0 and (lines[j].strip().startswith('@') or lines[j].strip() == ''):
                if f'@pytest.mark.{tab_marker}' in lines[j]:
                    has_tab_marker = True
                if f'@pytest.mark.{suite_marker}' in lines[j]:
                    has_suite_marker = True
                j -= 1
            
            # Add markers if they don't exist
            if not has_tab_marker or not has_suite_marker:
                indent = len(line) - len(line.lstrip())
                marker_indent = ' ' * indent
                
                # Find where to insert (after existing decorators or before function)
                insert_pos = i
                while insert_pos > 0 and (lines[insert_pos - 1].strip().startswith('@') or 
                                          lines[insert_pos - 1].strip() == ''):
                    insert_pos -= 1
                
                # Insert markers
                if not has_tab_marker:
                    new_lines.insert(insert_pos, f"{marker_indent}@pytest.mark.{tab_marker}\n")
                    insert_pos += 1
                if not has_suite_marker:
                    new_lines.insert(insert_pos, f"{marker_indent}@pytest.mark.{suite_marker}\n")
                    insert_pos += 1
        
        new_lines.append(line)
        i += 1
    
    # Add pytest import if not present
    if not has_pytest_import:
        # Find where to insert import (usually at the top after other imports)
        import_inserted = False
        for i, line in enumerate(new_lines):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                # Insert after the last import
                continue
            elif not import_inserted and (line.strip() == '' or not line.strip().startswith('#')):
                new_lines.insert(i, 'import pytest\n')
                import_inserted = True
                break
    
    # Write back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    return True

def main():
    """Main function to add markers to all test files."""
    print("Adding pytest markers to all test files...")
    print("=" * 60)
    
    total_files = 0
    modified_files = 0
    
    for test_dir, suite_marker in test_dirs.items():
        dir_path = f'tests/{test_dir}'
        if not os.path.exists(dir_path):
            print(f"Directory not found: {dir_path}")
            continue
        
        print(f"\nProcessing {test_dir}...")
        
        for filename in sorted(os.listdir(dir_path)):
            if filename.startswith('test_') and filename.endswith('.py'):
                filepath = os.path.join(dir_path, filename)
                tab_name = extract_tab_name(filename)
                
                if not tab_name:
                    print(f"  Could not extract tab name from {filename}, skipping...")
                    continue
                
                tab_marker = normalize_tab_name(tab_name)
                total_files += 1
                
                print(f"  Processing {filename}...")
                print(f"    Tab marker: {tab_marker}")
                print(f"    Suite marker: {suite_marker}")
                
                if add_markers_to_file(filepath, tab_marker, suite_marker):
                    modified_files += 1
                    print(f"    [OK] Markers added successfully")
                else:
                    print(f"    [-] Skipped (markers already exist)")
    
    print("\n" + "=" * 60)
    print(f"Summary:")
    print(f"  Total files processed: {total_files}")
    print(f"  Files modified: {modified_files}")
    print(f"  Files skipped (already had markers): {total_files - modified_files}")
    print("\nDone!")

if __name__ == '__main__':
    main()

