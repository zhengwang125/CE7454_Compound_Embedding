import pickle


G_collection = pickle.load(open('G_collection', 'rb'), encoding='bytes')
G_labeldict = pickle.load(open('G_labeldict', 'rb'), encoding='bytes')
PATTERN = pickle.load(open('PATTERN', 'rb'), encoding='bytes')
Graph_Label_list = pickle.load(open('Graph_Label_list', 'rb'), encoding='bytes')\

Element_list=['','H','He','Li','Be','B',
              'C','N','O','F','Ne','Na',
              'Mg','Al','Si','P','S','Cl',
              'Ar','K','Ca','Sc','Ti','V',
              'Cr','Mn','Fe','Co','Ni','Cu',
              'Zn','Ga','Ge','As','Se','Br',
              'Kr','Rb','Sr','Y','Zr','Nb',
              'Mo','Tc','Ru','Rh','Pd','Ag',
              'Cd','In','Sn','Sb','Te','I','Xe']

STR_PATTERN = []
for i in range(len(PATTERN)):
    if i % 50 == 0:
        print('processing', i)
    STR = []
    for pattern in PATTERN[i]:
        t = []
        for nid in pattern:
            t.append(Element_list.index(G_labeldict[i][nid]))
            t.sort()
            s=''
            for t_ in t:
                s = s + '$' + str(t_)
        STR.append(s)
    STR_PATTERN.append(STR)

corpus = {}
c = 0 
for str_p in STR_PATTERN:
    for item in str_p:
        if item in corpus:
            continue
        else:
            corpus[item] = c
            c = c + 1
print('Size of corpus', len(corpus))

Tokens = []
Lookup = {}
for i in range(len(STR_PATTERN)):
    tokens = []
    c = 0
    for item in STR_PATTERN[i]:
        tokens.append(corpus[item])
        Lookup[corpus[item]] = (i, c)
        c = c + 1
        #tokens.sort()
    Tokens.append(tokens)
    if i < 10:
        print('Token & Label', Tokens[i], Graph_Label_list[i])

#reduce tokens (if necessary)
#while True:
#    tempset = set(Tokens[0]).intersection(*Tokens)
#    print(tempset)
#    if len(tempset) == 0:
#        break
#    for ts in tempset:
#        for t in Tokens:
#            t.remove(ts)

for i in range(40):
    print('Token & Label', Tokens[i], Graph_Label_list[i])

pickle.dump(Tokens, open('Tokens', 'wb'), protocol=2)
pickle.dump(corpus, open('corpus', 'wb'), protocol=2)
pickle.dump(Lookup, open('Lookup', 'wb'), protocol=2)