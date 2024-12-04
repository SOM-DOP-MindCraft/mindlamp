import sys
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter

def run_notebook(notebook_path, user_id):
    # Read the notebook
    with open(notebook_path, 'r') as f:
        nb = nbformat.read(f, as_version=4)
    
    # Modify notebook to use specific user ID
    for cell in nb.cells:
        if cell.cell_type == 'code':
            cell.source = cell.source.replace('MIND001', user_id)
    
    # Execute the notebook
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': '.'}})
    
    # Convert to HTML
    html_exporter = HTMLExporter()
    (body, _) = html_exporter.from_notebook_node(nb)
    
    # Save HTML report
    with open(f'reports/{user_id}_report.html', 'w') as f:
        f.write(body)
    
    print(f"Report generated for {user_id}")

if __name__ == '__main__':
    user_id = sys.argv[1]
    run_notebook('notebooks/user_report.ipynb', user_id)
