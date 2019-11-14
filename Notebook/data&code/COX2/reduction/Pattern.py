import networkx as nx
import matplotlib.pyplot as plt
import pickle

f_node_labels = open('../COX2_node_labels.txt')
f_node_attributes = open('../COX2_node_attributes.txt')
f_graph_indicator = open('../COX2_graph_indicator.txt')
f_graph_labels = open('../COX2_graph_labels.txt')
f_graph = open('../COX2_A.txt')
Element_list=['','H','He','Li','Be','B',
              'C','N','O','F','Ne','Na',
              'Mg','Al','Si','P','S','Cl',
              'Ar','K','Ca','Sc','Ti','V',
              'Cr','Mn','Fe','Co','Ni','Cu',
              'Zn','Ga','Ge','As','Se','Br']

def read_file(f_node_labels, f_node_attributes, f_graph_indicator, f_graph_labels, f_graph):
    Node_Label_list=[]
    Node_Attribute_list=[]
    Bond_list=[]
    Graph_Label_list=[]
    Graph_Indicator_list=[]
    
    for line in f_node_labels:
        Node_Label_list.append(int(line))
    f_node_labels.close()

    for line in f_node_attributes:
        temp=line.split(',')
        for i in range(0,len(temp)):
            temp[i]=float(temp[i])
        Node_Attribute_list.append(temp)
    f_node_attributes.close()

    for line in f_graph:
        temp=line.split(',')
        for i in range(0,len(temp)):
            temp[i]=int(temp[i])
        Bond_list.append(temp)
    f_graph.close()

    for line in f_graph_labels:
        Graph_Label_list.append(int(line))
    f_graph_labels.close()

    for line in f_graph_indicator:
        Graph_Indicator_list.append(int(line))
    f_graph_indicator.close()
    
    return Node_Label_list, Node_Attribute_list, Bond_list, Graph_Label_list, Graph_Indicator_list

def build_graph(Bond_list, Graph_Indicator_list, total):
    G_collection = []
    G_labeldict = []
    for Graph_ID in range(1, total+1):
        labeldict = {}
        if Graph_ID % 50 == 0:
            print('processing:', Graph_ID)
        G = nx.Graph()
        for i in range(len(Bond_list)):
            temp_bond = Bond_list[i]
            if Graph_Indicator_list[temp_bond[0]-1] > Graph_ID:
                break
            if Graph_Indicator_list[temp_bond[0]-1] == Graph_ID and Graph_Indicator_list[temp_bond[1]-1] == Graph_ID:
                #print(temp_bond[0]-1, temp_bond[1]-1)
                labeldict[temp_bond[0]-1] = Element_list[Node_Label_list[temp_bond[0] - 1]]
                labeldict[temp_bond[1]-1] = Element_list[Node_Label_list[temp_bond[1] - 1]]
                G.add_edge(temp_bond[0]-1, temp_bond[1]-1)
        G_collection.append(G)
        G_labeldict.append(labeldict)
    return G_collection, G_labeldict

def viz(ID):
    G, node_labels, graph_labels = G_collection[ID], G_labeldict[ID], Graph_Label_list[ID]
    nx.draw(G, with_labels = True, node_color='y', node_size = 250, font_size=15)
    plt.show()
    nx.draw(G, labels = node_labels, with_labels = True, node_color='y', node_size = 250, font_size=15)
    plt.show()
    print('graph_labels', graph_labels)

def find_skeleton(ID):
    pattern_set = []
    skeleton = nx.cycle_basis(G_collection[ID])
    print('Skeleton of carbon circles', skeleton)
    re_node = []
    #remove skeleton
    for sk in skeleton:
        pattern_set.append(sk)
        for i in sk:
            re_node.append(i)
    G_collection[ID].remove_nodes_from(re_node)
    #nx.draw(G_collection[ID], with_labels = False, node_color='y', node_size = 200, font_size=10)
    #plt.show()
    for c in nx.connected_components(G_collection[ID]):
        nodeSet = G_collection[ID].subgraph(c).nodes()
        #print(nodeSet)
        pattern_set.append(list(nodeSet))
    return pattern_set

if __name__ == '__main__':
    Node_Label_list, Node_Attribute_list, Bond_list, Graph_Label_list, Graph_Indicator_list = read_file(f_node_labels, f_node_attributes, f_graph_indicator, f_graph_labels, f_graph)
    G_collection, G_labeldict = build_graph(Bond_list, Graph_Indicator_list, total = 467)
    pickle.dump(G_collection, open('G_collection', 'wb'), protocol=2)
    pickle.dump(G_labeldict, open('G_labeldict', 'wb'), protocol=2)
    ID = 0
    viz(ID)
    PATTERN = []
    for i in range(len(Graph_Label_list)):
        print('processing ID', i)
        pattern_set = find_skeleton(i)
        PATTERN.append(pattern_set)
    pickle.dump(PATTERN, open('PATTERN', 'wb'), protocol=2)
    pickle.dump(Graph_Label_list, open('Graph_Label_list', 'wb'), protocol=2)

