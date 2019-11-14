import json
import copy
import six.moves.urllib.request as urlreq
from six import PY3

import dash
import dash_bio as dashbio
import dash_html_components as html
import random


Graph_ID=32; #group ID


#--------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------

Node_Label_list=[];
f=open('BZR_node_labels.txt');
for line in f:
    Node_Label_list.append(int(line));
f.close();

Node_Attribute_list=[];
f=open('BZR_node_attributes.txt');
for line in f:
    temp=line.split(',');
    for i in range(0,len(temp)):
        temp[i]=float(temp[i]);
    Node_Attribute_list.append(temp);
f.close();

Bond_list=[];
f=open('BZR_A.txt');
for line in f:
    temp=line.split(',');
    for i in range(0,len(temp)):
        temp[i]=int(temp[i]);
    Bond_list.append(temp);
f.close();

Graph_Label_list=[];
f=open('BZR_graph_labels.txt');
for line in f:
    Graph_Label_list.append(int(line));
f.close();

Graph_Indicator_list=[];
f=open('BZR_graph_indicator.txt');
for line in f:
    Graph_Indicator_list.append(int(line));
f.close();

print(Graph_Label_list[Graph_ID]);


data={"nodes":[],"links":[]};
Atom_Info={"id": 1, "atom": "C"};
Atoms=[];
Bond_Info={"id": 3, "source": 1, "target": 17, "bond": 1, "strength": 1, "distance": 20.2};
Bonds=[];
Visual_Info={"color": "#8282D2", "visualization_type": "cartoon"};
Visual={};

Element_list=['','H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl'];

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
        temp["id"]=count+1;
        #temp["atom"]=Element_list[Node_Label_list[i]]+"-"+str(count+1);
        temp["atom"]=Element_list[Node_Label_list[i]]+"-"+str(Node_Label_list[i]);
        count_map[i]=count;
        
        Atoms.append(temp);
        temp=copy.deepcopy(Visual_Info);
        temp["color"]=Node_Color_list[Node_Label_list[i]-1];
        Visual[str(count)]=temp;
        count=count+1;

count=1;
for i in range(len(Bond_list)):
    temp_bond=Bond_list[i];
    if(Graph_Indicator_list[temp_bond[0]-1]==Graph_ID and Graph_Indicator_list[temp_bond[1]-1]==Graph_ID):
        temp=copy.deepcopy(Bond_Info);
        temp["source"]=count_map[temp_bond[0]-1]+1;
        temp["target"]=count_map[temp_bond[1]-1]+1;
        temp["id"]=count;
        count=count+1;
        Bonds.append(temp);

data["nodes"]=Atoms;
data["links"]=Bonds;

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
    dashbio.Molecule2dViewer(
        id='my-dashbio-molecule2d',
        modelData=data,
        #selectedAtomIds=list(range(1, 18))
    ),
    html.Hr(),
    html.Div(id='molecule2d-output')
])


@app.callback(
    dash.dependencies.Output('molecule2d-output', 'children'),
    [dash.dependencies.Input('my-dashbio-molecule2d', 'selectedAtomIds')]
)
def update_selected_atoms(ids):
    if ids is None or len(ids) == 0:
        return "No atom has been selected. Select atoms by clicking on them."
    return "Selected atom IDs: {}.".format(', '.join([str(i) for i in ids]))


if __name__ == '__main__':
    app.run_server(debug=True)