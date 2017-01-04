import numpy as np
from sklearn import datasets, linear_model
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score, ShuffleSplit
import createData as CD
from sklearn.metrics import f1_score, roc_curve, auc, precision_recall_fscore_support

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, precision_score, recall_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV

class Model(object):   

    def __init__(self, object) :
        self.full_X_train, self.full_y_train = object.getTrainData()
        self.full_X_test, self.full_y_test = object.getTestData()
        self.X_train, self.y_train = self.full_X_train[:,1:],self.full_y_train[:,1:] 
        self.X_test, self.y_test = self.full_X_test[:,1:], self.full_y_test[:,1:]
        self.yTrain = np.array(self.full_y_train[:,1], dtype = int)
        self.yTest = np.array(self.full_y_test[:,1], dtype = int)
        self.idsTest = self.y_test[:,0]
        self.acc = None
        self.model = None
        self.classify(self.X_train, self.yTrain, self.X_test, self.yTest)
        

    def classify(self, X_train, yTrain, X_test, yTest):
       
        parameters = {'solver':('lbfgs','sgd','adam'),
                      'activation' : ('relu','logistic','tanh'),
                        'max_iter' : (500,1000),
                        'hidden_layer_sizes' : ((5,), (10,))
                        }
        clf = MLPClassifier()
        #clf = MLPClassifier(solver = 'lbfgs', hidden_layer_sizes=(5, ), activation = 'logistic', max_iter = 1000)
        clf = GridSearchCV(clf, parameters)
        
        # cv = ShuffleSplit(n_splits=3, test_size=0.3, random_state=0)
        # scores = cross_val_score(clf, X_train, yTrain, cv=cv)
        # print("Cross Validation Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        clf.fit(X_train, yTrain)
        
        self.model = clf
        
        X = np.vstack((X_train,X_test))
        X_full = np.vstack((self.full_X_train, self.full_X_test))
        prob = clf.predict_proba(X)
        #self.calculate_f1(yTest, prob)
        p = np.array([a[b^1] for a,b in zip(prob,yTest)])
        
        self.plot_roc(yTest, p)
        
        #print clf
        self.evaluate(X_test,yTest, clf)
        
        
    def calculate_f1(self, yTest, y_pred):
        print "\n======================="
        precision, recall, _, _ = precision_recall_fscore_support(yTest, y_pred, average='macro') 
        print "\nPrecision = ", precision
        print "\nRecall = ", recall
        print "\nf1_score(macro) = ", f1_score(yTest, y_pred, average='macro')  
        print "\nf1_score(micro) = ",f1_score(yTest, y_pred, average='micro')  
        print "\nf1_score(weighted) = ", f1_score(yTest, y_pred, average='weighted')  
        print "\nf1_score(avg=None) = ", f1_score(yTest, y_pred, average=None)
        print "\n======================="
    
    def plot_roc(self, yTest, y_pred):               
    # Compute ROC curve and ROC area for each class
    # http://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html 
        fpr, tpr, _ = roc_curve(yTest, y_pred)
        roc_auc = auc(fpr, tpr)  
        #print roc_auc 
        
    # Compute micro-average ROC curve and ROC area
        fpr_micro, tpr_micro, _ = roc_curve(yTest, y_pred)  
        roc_auc_micro = auc(fpr_micro, tpr_micro)    
        #print "\n======================="
        #print '\nfpr_micro = ', fpr_micro
        #print '\ntpr_micro = ', tpr_micro
        #print '\nroc_auc_micro = ', roc_auc_micro
        #print "\n======================="
        plt.figure()
        lw = 2

        plt.plot(fpr, tpr, color='darkorange', lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic')
        plt.legend(loc="lower right")
        plt.show()
        
        
    
    def evaluate(self, X_test, yTest, clf):
       
        expect = yTest
        predicted = clf.predict(X_test)
        self.acc = accuracy_score(expect, predicted)*100
        
        print("---------------------------------------------------------")
        print("                 Classification Accuracy                 ")
        print(str(accuracy_score(expect, predicted)))
        print("---------------------------------------------------------")
        #print("---------------------------------------------------------")
        #print("                 Classification Report                   ")
        #print(classification_report(expect, predicted))
        
        # Compute confusion matrix
        #cnf_matrix = confusion_matrix(expect, predicted)
        #np.set_printoptions(precision=2)
        #confusion_matrix = confusion_matrix(expect, predicted).tolist()
        #cm_total = float(sum(sum(x) for x in cnf_matrix))

#        print("---------------------------------------------------------")
#        print("---------------------------------------------------------")
#        print("              False Positives and Negatives              ")
#
#        print "False Positive: ", cnf_matrix[1][0] / cm_total
#        print "False Negative: ", cnf_matrix[0][1] / cm_total

    def predict(self,data) :
        clf = self.model
        prob = clf.predict_proba(data[:,1:])
        ind =  np.argpartition(prob[:,1], -10)[-10:]
        moviesID = []
        #finding movie ids of top 10 movies
        for x in ind :
            movie = data[x]
            moviesID.append(movie[0])
        #print "movied IDS = %s" %moviesID      
        return moviesID
        
  