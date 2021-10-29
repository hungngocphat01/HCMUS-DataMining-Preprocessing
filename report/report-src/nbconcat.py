"""
Nối 2 hay nhiều jupyter notebook với nhau 
"""
import json 
import sys 

# Last arg: output filename
ipynb_names = sys.argv[1:]
ipynb_jsons = []

# Read all notebooks
for name in ipynb_names:
    with open(name, 'rt') as f:
        json_data = json.loads(f.read())
        ipynb_jsons.append(json_data)

# Append all notebooks to the first one (only keep the document metadata of the first one)
first_notebook = ipynb_jsons[0]
for i in range(1, len(ipynb_jsons)):
    cells = ipynb_jsons[i]['cells']
    for cell in cells:
        if 'id' in cell:
            del cell['id']

    first_notebook['cells'] += cells

# Write to stdout
print(json.dumps(first_notebook, indent=2))