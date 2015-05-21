import pandas as pd
import os
from nltk.corpus import propbank
from nltk.parse import stanford
from sklearn.feature_extraction import DictVectorizer as DV
os.environ['STANFORD_PARSER'] = '/home/sony/NLTK/stanford-parser-full-2014-10-31'
os.environ['STANFORD_MODELS'] = '/home/sony/NLTK/stanford-parser-full-2014-10-31'
parser = stanford.StanfordParser(model_path="/home/sony/NLTK/englishPCFG.ser.gz")
df=pd.DataFrame(columns=['Predicate','V POS','Head Word','Head Word POS','Phrase type','Path','Relative Position','Target','Constituent'])
def createCSV(t,height,index_pred,size):
	
	# inst=['I','heard','her','shrill','voice']
	

	
	for x in xrange(0,size-height):	
		
		index1=x
		index1_type="Unknown"
		index1_height=height
		# print index1,index1_height,index1_type,index_pred
		if(index_pred!=index1):

			leaves_pos= t.treepositions('leaves')
			pred=t[leaves_pos[index_pred]]
			const=t[leaves_pos[index1][0:len(leaves_pos[index1])-index1_height-1]]
			target=index1_type
			head_word=t[leaves_pos[index1]]
			(phrase,hwpos)= phrase_type(leaves_pos,t,index1,index1_height)

			# print "Predicate : ",t[leaves_pos[index_pred]]
			# print "Constituent : ",t[leaves_pos[index1][0:len(leaves_pos[index1])-index1_height-1]]
			# print "Target : ",index1_type
			# print "Head Word : ",t[leaves_pos[index1]]
			# print "Phrase type : ", phrase
			(rel_pos,path)=getRelativePosition(leaves_pos,t,index1,index1_height,index_pred)
			vpos=Vpos(leaves_pos,t,index_pred)
			if(rel_pos=="left"):
				rel_pos=0
			else:
				rel_pos=1
			# print "Path :",path;
			# print "Predicate : ",t[leaves_pos[index_pred]]
			# print "Constituent : ",t[leaves_pos[index1][0:len(leaves_pos[index1])-index1_height-1]]
			# print "Target : ",index1_type
			# print "Head Word : ",t[leaves_pos[index1]]
			# print "Phrase type : ", phrase_type(leaves_pos,t,index1,index1_height)
			# print "Path from predicate to constituent : ",getRelativePosition(leaves_pos,t,index1,index1_height,index_pred)
			global df
			df=df.append({'Predicate':pred,'Target':target,'Head Word':head_word,'Phrase type':phrase,'Relative Position':rel_pos,'Path':path,'Head Word POS':hwpos,'V POS':vpos,'Constituent':const},ignore_index=True)
		# global df
		# df=df.append({'Target':1,'Relative Position':0,},ignore_index=True)
	# t.draw()
	return;

def phrase_type(leaves_pos,t,index1,index1_height):
	# print t[leaves_pos[index1]]
	length1=len(leaves_pos[index1])
	# print length1
	# print t[leaves_pos[index1][0:1]]
	# print t[leaves_pos[index1][0:length1-1]]
	return (t[leaves_pos[index1][0:length1- index1_height-1]].label(),t[leaves_pos[index1][0:length1-1]].label());
def Vpos(leaves_pos,t,index2):
	length2=len(leaves_pos[index2])
	return t[leaves_pos[index2][0:length2-1]].label()
def getRelativePosition(leaves_pos,t,index1,index1_height,index2):
	j=0
	t1=t
	while (1) :
		if(leaves_pos[index1][j]==leaves_pos[index2][j]):
			t1=t1[leaves_pos[index1][j]]
			j+=1
		else:
			break;
	if (leaves_pos[index1][j]<leaves_pos[index2][j]):
		position="left"
	else:
		position="right"
	path=""

	length2=len(leaves_pos[index2])
	while (1):
		# print t[leaves_pos[index2][0:length2-1]].label(),u"\u2191"
		path+=t[leaves_pos[index2][0:length2-1]].label()+"1"
		if(length2-1<=j+1):
			break
		else:
			length2-=1

	while (1):
		# print t1.label(),u"\u2193"
		path+=t1.label()+"0"
		t1=t1[leaves_pos[index1][j]]
		j+=1
		if(j>len(leaves_pos[index1])-index1_height-1): #len(leaves_pos[index1]-2
			break

	# print "Relative position : " , position

	return (position,path);

def Feature(statement,index_pred):
	
	# statement=raw_input('Enter the sentence you want to label SEMANTICALLY (SRL) : ')
	global parser
	sentences = parser.raw_parse_sents((statement, ""))
	t=sentences[0]
	size=len(statement.split())
	# print "No. of words : ",size
	# index_pred=raw_input('Index of predicate : ')
	index_pred=int(index_pred)-1
	print index_pred
	for x in xrange(0,2):
		createCSV(t,x,index_pred,size);
	global df

	df.to_csv("data_stanford.csv")

	df=pd.DataFrame(columns=['Predicate','V POS','Head Word','Head Word POS','Phrase type','Path','Relative Position','Target','Constituent'])
	# t.draw()

	return;
# cat_dict = df.T.to_dict().values()
# vectorizer = DV( sparse = False )
# vec_x_cat_train = vectorizer.fit_transform( cat_dict )


# Feature();