# tools/project_writer.py

import os

def save_index_html(html_code: str, project_name: str = "html_site") -> str:
    base_path = f"./projects/{project_name}"
    os.makedirs(base_path, exist_ok=True)

    file_path = os.path.join(base_path, "index.html")
    with open(file_path, 'w') as f:
        f.write(html_code)

    return base_path
