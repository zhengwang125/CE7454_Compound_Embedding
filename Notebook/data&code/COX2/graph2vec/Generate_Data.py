import networkx as nx
Node_Label_list=[];
f=open('../COX2_node_labels.txt');
for line in f:
    Node_Label_list.append(int(line));
f.close();

Node_Attribute_list=[];
f=open('../COX2_node_attributes.txt');
for line in f:
    temp=line.split(',');
    for i in range(0,len(temp)):
        temp[i]=float(temp[i]);
    Node_Attribute_list.append(temp);
f.close();

Bond_list=[];
f=open('../COX2_A.txt');
for line in f:
    temp=line.split(',');
    for i in range(0,len(temp)):
        temp[i]=int(temp[i]);
    Bond_list.append(temp);
f.close();

Graph_Label_list=[];
f=open('../COX2_graph_labels.txt');
for line in f:
    Graph_Label_list.append(int(line));
f.close();

Graph_Indicator_list=[];
f=open('../COX2_graph_indicator.txt');
for line in f:
    Graph_Indicator_list.append(int(line));
f.close();

for i in range(1,max(Graph_Indicator_list)+1):
    G=nx.Graph();
    count=0;
    for j in range(0,len(Node_Label_list)):
        if Graph_Indicator_list[j] == i:
            count=count+1;
            G.add_node(count,label=Node_Label_list[j]);
            #G.add_node(count)

    for j in range(0,len(Bond_list)):
        temp_bond=Bond_list[j];
        if Graph_Indicator_list[temp_bond[0]-1]==i:
            G.add_edge(temp_bond[0],temp_bond[1]);

    nx.write_gexf(G,'./data/'+str(i-1)+'.gexf')

f=open('COX2.Labels','w');
for i in range(0,len(Graph_Label_list)):
    if Graph_Label_list[i]==-1:
        f.write(str(i)+'.gexf '+str(1)+'\n');
    else:
        f.write(str(i)+'.gexf '+str(2)+'\n');
f.close();