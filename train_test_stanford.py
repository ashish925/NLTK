import numpy as np
import pandas as pd
from sklearn.feature_extraction import DictVectorizer as DV
from sklearn.svm import SVC
from sklearn.metrics import roc_auc_score as AUC

# train_file = 'data.csv'
# test_file = 'data2.csv'
train_file='train_1_check.csv'
test_file='data_stanford.csv'

train = pd.read_csv( train_file )
test = pd.read_csv( test_file )


# numeric x

numeric_cols = [ 'Relative Position' ]
x_num_train = train[ numeric_cols ].as_matrix()
x_num_test = test[ numeric_cols ].as_matrix()

# scale to <0,1>

max_train = np.amax( x_num_train, 0 )
max_test = np.amax( x_num_test, 0 )		# not really needed

x_num_train = x_num_train / max_train
x_num_test = x_num_test / max_train		# scale test by max_train

#-----------------------------------------------------------------

y_train = train.Target
y_test = test.Target

# target_cols = [ 'Target' ]
# y_train=train[ target_cols ].as_matrix()
# y_test=test[ target_cols ].as_matrix()

# cat_train=train.Target
# cat_test=test.Target

# y_cat_train = cat_train.T.to_dict().values()
# y_cat_test = cat_test.T.to_dict().values()


# vectorizer = DV( sparse = False )
# y_train = vectorizer.fit_transform( y_cat_train )
# y_test = vectorizer.transform( y_cat_test )

# ----------------------------------------------------------------


cat_train = train.drop(  numeric_cols+ [ 'Index', 'Target'], axis = 1 )
cat_test = test.drop( numeric_cols + [ 'Index', 'Target'], axis = 1 )

# cat_train.fillna( 'NA', inplace = True )
# cat_test.fillna( 'NA', inplace = True )

x_cat_train = cat_train.T.to_dict().values()
x_cat_test = cat_test.T.to_dict().values()


vectorizer = DV( sparse = False )
vec_x_cat_train = vectorizer.fit_transform( x_cat_train )
vec_x_cat_test = vectorizer.transform( x_cat_test )


# complete x

x_train = np.hstack(( x_num_train, vec_x_cat_train ))
x_test = np.hstack(( x_num_test, vec_x_cat_test ))



if __name__ == "__main__":

	# SVM looks much better in validation

	print "training SVM..."
	
	# although one needs to choose these hyperparams
	C = 120 #c=120 gamma=.005 data=998
	gamma = .005 #c=100 gamma=.001 data=998
	shrinking = True

	probability = True
	verbose = True

	#svc = SVC( C = C, gamma = gamma)
	svc = SVC( C = C, gamma = gamma, shrinking = shrinking, probability = probability, verbose = verbose )
	svc.fit( x_train, y_train )

	# p = svc.predict_proba( x_test )	
	# print "P :",p
	# print "X train : ",x_train[0]
	# print "x_test : ",x_test[0]
	# print "x_test : ",x_test[1]
	# print "x_test : ",x_test[2]
	
	count=0;
	for x in xrange(0,len(y_test)):
		pred=svc.predict(x_test[x])
		# print x,pred
		print pred[0],y_test[x]
		p = svc.predict_proba( x_test[x] )	
		print max(p[0])

		if(pred[0]==y_test[x]):
			count+=1
			print count

	
	sc=svc.score(x_test,y_test)
	print sc
	
	
	# auc = AUC( y_test, p[:,1] )
	# print "SVM AUC", auc	