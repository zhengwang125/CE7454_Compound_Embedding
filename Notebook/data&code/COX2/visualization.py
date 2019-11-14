import json
import copy
import six.moves.urllib.request as urlreq
from six import PY3
import dash_core_components as dcc
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


def Get_2Ddata(ID):
    Graph_ID=ID;
    data_2D={"nodes":[],"links":[]};
    Atom_Info_2D={"id": 1, "atom": "C"};
    Atoms_2D=[];
    Bond_Info_2D={"id": 3, "source": 1, "target": 17, "bond": 1, "strength": 1, "distance": 20.2};
    Bonds_2D=[];
    Visual_Info_2D={"color": "#8282D2", "visualization_type": "cartoon"};
    Visual_2D={};

    Element_list_2D=['','H','He','Li','Be','B',
              'C','N','O','F','Ne','Na',
              'Mg','Al','Si','P','S','Cl',
              'Ar','K','Ca','Sc','Ti','V',
              'Cr','Mn','Fe','Co','Ni','Cu',
              'Zn','Ga','Ge','As','Se','Br'];

    max_color_2D=max(Node_Label_list);
    count_2D=0;
    count_map_2D=list(range(len(Node_Label_list)));
    for i in range(len(Graph_Indicator_list)):
        if(Graph_Indicator_list[i]==Graph_ID):
            temp=copy.deepcopy(Atom_Info_2D);
            temp["id"]=count_2D+1;
            temp["atom"]=Element_list_2D[Node_Label_list[i]]+"-"+str(count_2D+1);
            count_map_2D[i]=count_2D;
            
            Atoms_2D.append(temp);
            temp=copy.deepcopy(Visual_Info_2D);
            temp["color"]=Node_Color_list[Node_Label_list[i]-1];
            Visual_2D[str(count_2D)]=temp;
            count_2D=count_2D+1;

    count_2D=1;
    for i in range(len(Bond_list)):
        temp_bond=Bond_list[i];
        if(Graph_Indicator_list[temp_bond[0]-1]==Graph_ID and Graph_Indicator_list[temp_bond[1]-1]==Graph_ID):
            temp=copy.deepcopy(Bond_Info_2D);
            temp["source"]=count_map_2D[temp_bond[0]-1]+1;
            temp["target"]=count_map_2D[temp_bond[1]-1]+1;
            temp["id"]=count_2D;
            count_2D=count_2D+1;
            Bonds_2D.append(temp);

    data_2D["nodes"]=Atoms_2D;
    data_2D["links"]=Bonds_2D;
    return data_2D;


def Get_data(ID):
    Graph_ID=ID;
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
    return data



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

div_list=[html.P(children='''3D Structures of a Specific Molecular Graph''', style={'font-size':'15pt','font-family':'Helvetica','margin-left':'30px'})]
div_list.append(html.Div(children=['Graph ID: ',dcc.Input(id='g-id',value=1,type='number',style={'border-radius':'5px','width':'40px'}), '----- Graph Label: ', html.Div(id='label1',children='Molecule Label: 1')],style={'margin-left':'60px','textAlign':'center','display':'flex'}));
div_list.append(html.Hr());

div_list1=[html.P(children='''2D Structures of a Specific Molecular Graph''', style={'font-size':'15pt','font-family':'Helvetica','margin-left':'30px'})]
div_list1.append(html.Div(children=['Graph ID: ',dcc.Input(id='g-id1',value=1,type='number',style={'border-radius':'5px','width':'40px'}), '----- Graph Label: ', html.Div(id='label2',children='Molecule Label: 1')],style={'margin-left':'60px','textAlign':'center','display':'flex'}));
div_list1.append(html.Hr());

data_2d=Get_2Ddata(1);
div_list1.append(html.Div([
    dashbio.Molecule2dViewer(
        id='my-dashbio-molecule2d',
        modelData=data_2d,
    ),
],style={'margin-left':'150px'}))

for i in range(1,16):
    temp_data=Get_data(i);
    div_list.append(html.Div(id='view'+str(i),children=[dashbio.Molecule3dViewer(styles=data,modelData=temp_data)]));

app.layout = html.Div([html.Div([
    html.H1(children='''Data Visualization for Deep Learning Project''',
        style={'textAlign':'center','color':'#7FDBFF'},id='testt'),
    html.Div(children=div_list,style={'border':'thin lightgrey solid','margin':'0 auto','width':'800px','border-radius':'5px','background':'#FCFCFC','box-shadow':'rgb(240, 240, 240) 5px 5px 5px 0px'}),
    html.Div(children=div_list1,style={'border':'thin lightgrey solid','margin':'0 auto','width':'800px','border-radius':'5px','background':'#FCFCFC','box-shadow':'rgb(240, 240, 240) 5px 5px 5px 0px'})
])],
style={'background':'''linear-gradient(rgba(255, 255, 255, 0.6),rgba(255, 255, 255, 0.6)),url("https://raw.githubusercontent.com/plotly/dash-docs/master/images/dash-pattern.png")'''})

call_list=[dash.dependencies.Output(component_id='label1', component_property='children')];
return_list=[str(Graph_Label_list[1])];
for i in range(1,16):
    call_list.append(dash.dependencies.Output(component_id='view'+str(i), component_property='style'));
    return_list.append({'display':'none'});

@app.callback(
    call_list,
    [dash.dependencies.Input(component_id='g-id', component_property='value')]
)
def update_output_div(input_value):
    if input_value<=0 or input_value>len(return_list):
        return 'ID > 0',{'display':'block'},{'display':'none'};
    else:
        return_list[0]=str(Graph_Label_list[input_value-1]);
        for i in range(1,len(return_list)):
            return_list[i]={'display':'none'};       
        return_list[input_value]={'display':'block'};
        return return_list;

@app.callback(
    [dash.dependencies.Output(component_id='label2', component_property='children'),
    dash.dependencies.Output(component_id='my-dashbio-molecule2d', component_property='modelData')],
    [dash.dependencies.Input(component_id='g-id1', component_property='value')]
)
def update_output_div(input_value):
    if input_value<=0 or input_value>len(return_list):
        return 'ID > 0',data_2d;
    else:
        data_2d=Get_2Ddata(input_value);
        return str(Graph_Label_list[input_value-1]),data_2d;
            
#-----------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
#    app.run_server(host='0.0.0.0')
    app.run_server(host='155.69.150.48')
