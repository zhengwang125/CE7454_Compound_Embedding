from sklearn.decomposition import PCA
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support

Graph_Label_list=[];
f=open('../COX2_graph_labels.txt');
for line in f:
    Graph_Label_list.append(int(line));
f.close();
Graph_Label_list=np.array(Graph_Label_list);
element=[];
num=[];
f=open('cox2.txt');
element_line=f.readline();
temp=element_line.split(' ');
for i in range(0,len(temp)-1):
    element.append(int(temp[i]));
for line in f:
    temp=line.split(' ');
    new_temp=[];
    for i in range(0,len(temp)-1):
        new_temp.append(int(temp[i]));
    num.append(new_temp);
f.close();

data=np.array(num);
pca=PCA(n_components=5);
reduction=pca.fit_transform(data);
print(pca.explained_variance_ratio_)


x_train, x_test, y_train, y_test = train_test_split(reduction, Graph_Label_list, random_state=1, train_size=0.6)
    
clf = SVC(C=5.0, kernel='poly', gamma='auto', decision_function_shape='ovr')
clf.fit(x_train, y_train.ravel())
y_hat = clf.predict(x_train)
  
print('training set accuracy:', accuracy_score(y_hat, y_train))
y_hat = clf.predict(x_test)
print('testing set accuracy:', accuracy_score(y_hat, y_test))
print('precision, recall, fscore, support', precision_recall_fscore_support(y_test, y_hat, labels=[-1]))