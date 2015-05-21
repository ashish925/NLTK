import numpy as np
import pandas as pd
from sklearn.feature_extraction import DictVectorizer as DV
from sklearn.svm import SVC
from sklearn.metrics import roc_auc_score as AUC
from featureExtraction_Propbank_final_stanford import Feature

# train_file = 'data.csv'
# test_file = 'data2.csv'
test=0;
x_test=0;
y_test=0;
constituent_test=0;
train_file='train_1_check.csv'


train = pd.read_csv( train_file )



# numeric x

numeric_cols = [ 'Relative Position' ]
x_num_train = train[ numeric_cols ].as_matrix()


# scale to <0,1>

max_train = np.amax( x_num_train, 0 )

x_num_train = x_num_train / max_train


#-----------------------------------------------------------------

y_train = train.Target


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


# cat_train.fillna( 'NA', inplace = True )
# cat_test.fillna( 'NA', inplace = True )

x_cat_train = cat_train.T.to_dict().values()



vectorizer = DV( sparse = False )
vec_x_cat_train = vectorizer.fit_transform( x_cat_train )



# complete x

x_train = np.hstack(( x_num_train, vec_x_cat_train ))




#----------------------------------------------------$$$$$


def testing():
	global x_test
	global y_test
	global max_train
	global vectorizer
	global constituent_test
	global test
	test_file='data_stanford.csv'
	test = pd.read_csv( test_file )

	numeric_cols = [ 'Relative Position' ]
	x_num_test = test[ numeric_cols ].as_matrix()

	# scale to <0,1>
	max_test = np.amax( x_num_test, 0 )		# not really needed

	x_num_test = x_num_test / max_train		# scale test by max_train

	#-----------------------------------------------------------------
	y_test = test.Target
	constituent_test=test.Constituent
	cat_test = test.drop( numeric_cols + ['Target','Constituent'], axis = 1 )

	x_cat_test = cat_test.T.to_dict().values()


	
	vec_x_cat_test = vectorizer.transform( x_cat_test )

	x_test = np.hstack(( x_num_test, vec_x_cat_test ))
	return;


#----------------------------------------------------$$$$$

def query(text,index):
	global svc
	Feature(text,index);
	print "Feature extraction... DONE ! "
	testing();
	print "testing SVM... "
	Predicate=test.Predicate
	size_const=len(y_test);
	size=(size_const+1)/2
	for x in xrange(0,size_const):
		pred=svc.predict(x_test[x])
		# print x,pred
		if Predicate[0] in constituent_test[x] :
			print pred[0],constituent_test[x],"---- > Not Selected"
		elif (x<size):
			print pred[0],constituent_test[x],"---- > Not Selected (level 1) " 
		else:
			print pred[0],constituent_test[x],"---- > Selected"
		p = svc.predict_proba( x_test[x] )	
		print max(p[0])

	return;

svc=0;
def FINAL():

	# SVM looks much better in validation

	print "training SVM..."
	
	# although one needs to choose these hyperparams
	C = 120 #c=120 gamma=.005 data=998
	gamma = .005 #c=100 gamma=.001 data=998
	shrinking = True

	probability = True
	verbose = True
	global svc
	#svc = SVC( C = C, gamma = gamma)
	svc = SVC( C = C, gamma = gamma,  probability = probability)
	svc.fit( x_train, y_train )

	print "training SVM... DONE ! "
	# while(1):
	# 	query(svc);
	# 	exit=raw_input('Press 1 to continue , 0 to exit : ')
	# 	if(int(exit)==0):
	# 		break


	
# FINAL()