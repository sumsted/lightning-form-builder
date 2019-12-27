"""lfb.py - Lightning Form Builder

Using a yaml-like definition file, generate markup for a Lighting Web Component. 

Each line represents a tag. 
Indentation indicates the nesting of tags with one another. 
Dict tag_map exists to map shortcuts to tag names.
Those names not found in tag_map are used as named.
JSON after a tag is translated to tag attributes.
Templated @track names are translated without quotes.
A list of all @track names is comment at end of markup.

Definition
----------
card: {"title":"MyForm","icon-name":"custom:custom20"}
    layout: {"multiple-rows":"readonly"}
        item: {"size": 12, "padding":"around-small", "small-device-size":"12"}
            layout:
                item: {"size":6, "padding":"horizontal-small"}
                    input: {"label":"Search Term", "value":"{searchTerm}"}
                item: {"size":6, "padding":"horizontal-small"}
                    div: {"style":"position:relative;height:100%;width:100%"}
                        div: {"style":"position:absolute;bottom:0"}
                            button: {"label":"Search", "onclick":"{performSearch}"}

Generated Markup
----------------
<template>
<lightning-card title="MyForm" icon-name="custom:custom20">
    <lightning-layout multiple-rows="readonly">
        <lightning-layout-item size="12" padding="around-small" small-device-size="12">
            <lightning-layout>
                <lightning-layout-item size="6" padding="horizontal-small">
                    <lightning-input label="Search Term" value={searchTerm}>
                    </lightning-input>
                </lightning-layout-item>
                <lightning-layout-item size="6" padding="horizontal-small">
                    <div style="position:relative;height:100%;width:100%">
                        <div style="position:absolute;bottom:0">
                            <lightning-button>
                            </lightning-button>
                        </div>
                    </div>
                </lightning-layout-item>
            </lightning-layout>
        </lightning-layout-item>
    </lightning-layout>
</lightning-card>
</template>
<!--
@track searchTerm = '';
-->

"""
import json
import uuid
import sys


tag_map = {
    'layout': 'lightning-layout',
    'item': 'lightning-layout-item',
    'input': 'lightning-input',
    'button': 'lightning-button',
    'card': 'lightning-card',
    'root': 'template',
    'tabset': 'lightning-tabset',
    'tab': 'lightning-tab',
    'rich': 'lightning-formatted-rich-text',
    'tile': 'lightning-tile',
    'format': 'lightning-formatted-text',
    'table': 'lightning-datatable'
}
tracks = {}
markup = []


def start(file_name):
    root = build_syntax_tree(file_name)
    traverse_tree(root)
    output_markup()
    output_tracks()


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


def traverse_tree(current):
    try:
        transform_node(current, tag_map[current['name']])
    except:
        transform_node(current)


def transform_node(current, label=None):
    label = label if label is not None else current['name']
    add_markup(add_attributes(label, current['attributes']),current['level'])
    for node in current['nodes']:
        traverse_tree(node)
    add_markup("</"+label+">", current['level'])


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

    
def add_markup(data, level):
    line = "".join(['    ']*level)+data
    markup.append(line)
    # print(line)


def add_attributes(tag_name, attributes):
    tag = "<"+tag_name
    try:
        for n, v in attributes.items():
            if v is None:
                tag += ' '+n
            elif str(v)[0] == '{':
                tag += ' '+n+'='+str(v)
                if n == 'value':
                    tracks[v[1:-1].split('.',1)[0]]= "@track "+v[1:-1].split('.',1)[0]+" = '';"
            else:
                tag += ' '+n+'="'+str(v)+'"'
    except Exception as e:
        pass
    tag += ">"
    return tag


def output_markup():
    print("<!-- Generated by Lightning Form Builder -->")
    for line in markup:
        print(line)
    

def output_tracks():
    print("<!-- ")
    for n, v in tracks.items():
        print(v)
    print("-->")


if __name__=='__main__':
    if len(sys.argv) != 2:
        print("Usage: python lfb.py {definition}")
    else:
        start(sys.argv[1])