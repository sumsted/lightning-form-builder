import json
import uuid
import sys


def start(file_name):
    root = build_syntax_tree(file_name)
    traverse_tree(root)
    

def create_node(file):
    line = file.readline()
    if line == '':
        return None
    parts = line[:-1].split(':',1)
    name = parts[0].strip()
    level = int((len(parts[0]) - len(name))/4)
    try:
        attributes = json.loads(parts[1].strip())
    except Exception as e:
        attributes = {}
    node = {
        'id': str(uuid.uuid4()),
        'name': name,
        'level': level,
        'attributes': attributes,
        'nodes': []
    }
    return node

    
def build_syntax_tree(file_name):
    root = {
        'id': str(uuid.uuid4()),
        'name': 'root',
        'level': -1,
        'attributes': {},
        'nodes': []
    }
    parents = {}
    current_level = 0
    parent = root
    with open(file_name,'r') as file:
        while True:
            current = create_node(file)
            if current is None:
                break
            difference = current['level'] - parent['level']
            if difference > 0:
                parent['nodes'].append(current)
                parents[current['id']] = parent
            elif difference == 0:
                parent = parents[parent['id']]
                parent['nodes'].append(current)
                parents[current['id']] = parent
            elif difference < 0:
                while difference <= 0:
                    parent = parents[parent['id']]
                    difference = current['level'] - parent['level']
                parent['nodes'].append(current)                
                parents[current['id']] = parent
            else: 
                pass
            parent = current
    return root 


markup = []
def to_markup(data, level):
    line = "".join(['    ']*level)+data
    markup.append(line)
    print(line)


def add_attributes(tag_name, attributes):
    tag = "<"+tag_name
    try:
        for n, v in attributes.items():
            if v is None:
                tag += ' '+n
            elif str(v)[0] == '{':
                tag += ' '+n+'='+str(v)
            else:
                tag += ' '+n+'="'+str(v)+'"'
    except Exception as e:
        pass
    tag += ">"
    return tag


def transform_node(current, label=None):
    label = label if label is not None else current['name']
    to_markup(add_attributes(label, current['attributes']),current['level'])
    for node in current['nodes']:
        traverse_tree(node)
    to_markup("</"+label+">", current['level'])


name_map = {
    'layout': 'lightning-layout',
    'item': 'lightning-layout-item',
    'input': 'lightning-input',
    'button': 'lightning-button',
    'card': 'lightning-card',
    'root': 'template',
    'tabset': 'lightning-tabset',
    'tab': 'lightning-tab',
    'rich': 'lightning-formatted-rich-text',
    'tile': 'lightning-tile'
}
def traverse_tree(current):
    try:
        transform_node(current, name_map[current['name']])
    except:
        transform_node(current)


if __name__=='__main__':
    if len(sys.argv) != 2:
        print("Usage: python lfb.py {definition}")
    else:
        start(sys.argv[1])