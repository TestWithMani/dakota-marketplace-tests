import os
import re

# Test directories
test_dirs = [
    'all_tabs_column_name',
    'all_tabs_fields_comparison',
    'all_tabs_fields_display_functionality',
    'all_tabs_lazy_loading',
    'all_tabs_list_view_crud',
    'all_tabs_pin_unpin_functionality'
]

tabs = set()

for test_dir in test_dirs:
    dir_path = f'tests/{test_dir}'
    if os.path.exists(dir_path):
        for filename in os.listdir(dir_path):
            if filename.startswith('test_') and filename.endswith('.py'):
                # Extract tab name from filename
                # Pattern: test_<tab_name>_tab_<suite_type>.py
                match = re.search(r'test_([^_]+(?:_[^_]+)*)_tab_', filename)
                if match:
                    tab_name = match.group(1)
                    tabs.add(tab_name)

# Print sorted tabs
for tab in sorted(tabs):
    print(tab)

