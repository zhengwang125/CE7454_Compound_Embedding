import json
import copy
import six.moves.urllib.request as urlreq
from six import PY3

import dash
import dash_bio as dashbio
import dash_html_components as html
import random


Graph_ID=1; #group ID


#--------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------
styles_data = urlreq.urlopen(
    'https://raw.githubusercontent.com/plotly/dash-bio-docs-files/master/' +
    'mol3d/styles_data.js'
).read()

if PY3:
    styles_data = styles_data.decode('utf-8')

Node_Label_list=[];
f=open('COX2_node_labels.txt');
for line in f:
    Node_Label_list.append(int(line));
f.close();

Node_Attribute_list=[];
f=open('COX2_node_attributes.txt');
for line in f:
    temp=line.split(',');
    for i in range(0,len(temp)):
        temp[i]=float(temp[i]);
    Node_Attribute_list.append(temp);
f.close();

Bond_list=[];
f=open('COX2_A.txt');
for line in f:
    temp=line.split(',');
    for i in range(0,len(temp)):
        temp[i]=int(temp[i]);
    Bond_list.append(temp);
f.close();

Graph_Label_list=[];
f=open('COX2_graph_labels.txt');
for line in f:
    Graph_Label_list.append(int(line));
f.close();

Graph_Indicator_list=[];
f=open('COX2_graph_indicator.txt');
for line in f:
    Graph_Indicator_list.append(int(line));
f.close();



data={"atoms":[],"bonds":[]};
Atom_Info={"name": "N", "chain": "A", "positions": [15.407, -8.432, 6.573], "residue_index": 1, "element": "N", "residue_name": "GLY1", "serial": 0};
Atoms=[];
Bond_Info={"atom2_index": 677, "atom1_index": 678};
Bonds=[];
Visual_Info={"color": "#8282D2", "visualization_type": "cartoon"};
Visual={};

max_color=max(Node_Label_list);
colorArr=['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'];
Node_Color_list=[];
for k in range(max_color):
    color="";
    for i in range(6):
        color+=colorArr[random.randint(0,14)];
    color="#"+color;
    Node_Color_list.append("#EBEBEB");

count=0;
count_map=list(range(len(Node_Label_list)));
for i in range(len(Graph_Indicator_list)):
    if(Graph_Indicator_list[i]==Graph_ID):
        temp=copy.deepcopy(Atom_Info);
        temp["name"]=str(Node_Label_list[i]);
        temp["positions"]=Node_Attribute_list[i];
        temp["element"]=str(Node_Label_list[i]);
        temp["residue_name"]=str(i+1);
        temp["serial"]=count;
        temp["residue_index"]=count;
        count_map[i]=count;
        
        Atoms.append(temp);
        temp=copy.deepcopy(Visual_Info);
        temp["color"]=Node_Color_list[Node_Label_list[i]-1];
        Visual[str(count)]=temp;
        count=count+1;


for i in range(len(Bond_list)):
    temp_bond=Bond_list[i];
    if(Graph_Indicator_list[temp_bond[0]-1]==Graph_ID and Graph_Indicator_list[temp_bond[1]-1]==Graph_ID):
        temp=copy.deepcopy(Bond_Info);
        temp["atom2_index"]=count_map[temp_bond[0]-1];
        temp["atom1_index"]=count_map[temp_bond[1]-1];
        Bonds.append(temp);

data["atoms"]=Atoms;
data["bonds"]=Bonds;

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dashbio.Molecule3dViewer(
        id='my-dashbio-molecule3d',
        styles=styles_data,
        modelData=data
    ),
    "Selection data",
    html.Hr(),
    html.Div(id='molecule3d-output')
])
#print(Visual)
print(Graph_Label_list[Graph_ID])
@app.callback(
    dash.dependencies.Output('molecule3d-output', 'children'),
    [dash.dependencies.Input('my-dashbio-molecule3d', 'selectedAtomIds')]
)
def show_selected_atoms(atom_ids):
    if atom_ids is None or len(atom_ids) == 0:
        return 'No atom has been selected. Click somewhere on the molecular \
        structure to select an atom.'
    return [html.Div([
        html.Div('Element: {}'.format(data['atoms'][atm]['element'])),
        html.Div('Chain: {}'.format(data['atoms'][atm]['chain'])),
        html.Div('Residue name: {}'.format(data['atoms'][atm]['residue_name'])),
        html.Br()
    ]) for atm in atom_ids]
#-----------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
