import pickle

Tokens = pickle.load(open('Tokens', 'rb'), encoding='bytes')
Graph_Label_list = pickle.load(open('Graph_Label_list', 'rb'), encoding='bytes')
positive = set()
negative = set()
for i in range(len(Tokens)):
    for t in Tokens[i]:
        if Graph_Label_list[i] == 1:
            positive.add(t)
        else:
            negative.add(t)

pn = positive&negative
Tokens_reduction = []
for i in range(len(Tokens)):
    temp = []
    for t in Tokens[i]:
        if t in pn:
            continue
        else:
            temp.append(t)
    Tokens_reduction.append(temp)