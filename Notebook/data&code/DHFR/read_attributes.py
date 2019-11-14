import pickle

def read_file(f_node_attributes):
    Node_Attribute_list = []
    for line in f_node_attributes:
        tmp = line.split(',')
        for i in range(0, len(tmp)):
            tmp[i] = float(tmp[i])
        Node_Attribute_list.append(tmp)
    f_node_attributes.close()
    return Node_Attribute_list

if __name__ == '__main__':
    f_node_attributes = open('DHFR_node_attributes.txt')
    Node_Attribute_list = read_file(f_node_attributes)
    pickle.dump(Node_Attribute_list, open('Node_Attribute', 'wb'), protocol=2)