from sklearn.model_selection import train_test_split
from gensim.models.doc2vec import Doc2Vec
import pickle
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support

def get_vector(path, label):
    model = Doc2Vec.load(path)
    RES = []
    for i in range(len(label)):
        RES.append(model.docvecs['g_'+str(i)])
    return np.array(RES), np.array(label)

if __name__ == '__main__':
    path_dm = './models/graph-dm.model'  
    Graph_Label_list = pickle.load(open('Graph_Label_list', 'rb'), encoding='bytes')
    
    X, Y = get_vector(path_dm, Graph_Label_list)
    
    x_train, x_test, y_train, y_test = train_test_split(X, Y, random_state=1, train_size=0.6)
    
    clf = SVC(C=20, kernel='rbf', gamma='auto', decision_function_shape='ovr')
    clf.fit(x_train, y_train.ravel())
    y_hat = clf.predict(x_train)
    
    print('training set accuracy:', accuracy_score(y_hat, y_train))
    y_hat = clf.predict(x_test)
    print('testing set accuracy:', accuracy_score(y_hat, y_test))
    # col[0]=results of -1, col[1]=results of 1 
    print('precision, recall, fscore, support', precision_recall_fscore_support(y_test, y_hat, labels=[-1]))
