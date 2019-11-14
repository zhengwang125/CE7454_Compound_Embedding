Node_Label_list=[];
f=open('../DHFR_node_labels.txt');
for line in f:
    Node_Label_list.append(int(line));
f.close();

Node_Attribute_list=[];
f=open('../DHFR_node_attributes.txt');
for line in f:
    temp=line.split(',');
    for i in range(0,len(temp)):
        temp[i]=float(temp[i]);
    Node_Attribute_list.append(temp);
f.close();

Bond_list=[];
f=open('../DHFR_A.txt');
for line in f:
    temp=line.split(',');
    for i in range(0,len(temp)):
        temp[i]=int(temp[i]);
    Bond_list.append(temp);
f.close();

Graph_Label_list=[];
f=open('../DHFR_graph_labels.txt');
for line in f:
    Graph_Label_list.append(int(line));
f.close();

Graph_Indicator_list=[];
f=open('../DHFR_graph_indicator.txt');
for line in f:
    Graph_Indicator_list.append(int(line));
f.close();

max_element=max(Node_Label_list);
all_atom_list=[0 for i in range(0,max_element+1)];
atom_map=[0 for i in range(0,max_element+1)];
for j in range(0,len(Node_Label_list)):
    all_atom_list[Node_Label_list[j]]=1;
max_element=0;

f=open('DHFR.txt','w');
for j in range(1,len(all_atom_list)):
    if all_atom_list[j]>0:
        max_element=max_element+1;
        atom_map[j]=max_element;
        f.write(str(j)+' ');

f.write('\n');

#map_list=[0 for i in range(0,len(Graph_Indicator_list))];
miss=0;

for i in range(1,max(Graph_Indicator_list)+1):
    atom_list=[0 for i in range(0,max_element+1)];
    count=0;
    for j in range(0,len(Node_Label_list)):
        if Graph_Indicator_list[j] == i:
            count=count+1;
            if count>miss:
                atom_list[atom_map[Node_Label_list[j]]]=atom_list[atom_map[Node_Label_list[j]]]+1;
    for k in range(1,len(atom_list)):
        f.write(str(atom_list[k])+' ');
    f.write('\n');

f.close();