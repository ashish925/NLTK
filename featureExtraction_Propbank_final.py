import pandas as pd
from nltk.corpus import propbank
from sklearn.feature_extraction import DictVectorizer as DV
df=pd.DataFrame(columns=['Roleset','Form','Tense','Voice','Predicate','V POS','Head Word','Head Word POS','Phrase type','Path','Relative Position','Target'])

def createCSV(inst_num):
	pb_instances = propbank.instances()
	inst = pb_instances[inst_num]
	t=inst.tree
	infl=inst.inflection
	# for (argloc, argid) in inst.arguments:
	# 	print('%-10s %s' % (argid, argloc.select(t).pprint(500)[:50]))
	
	try:
		# print inst.predicate
		index_pred=inst.predicate.wordnum
	except Exception, e:
		try:
			# print inst.predicate.pieces
			index_pred=inst.predicate.pieces[0].wordnum
		except Exception, e:
			# print inst.predicate.pieces[0].pieces
			index_pred=inst.predicate.pieces[0].pieces[0].wordnum
	# index_pred is index2 always
	for x in xrange(0,len(inst.arguments)):	
		# print inst.arguments[x][0]
		try:
			
			index1_height= inst.arguments[x][0].height
			index1=inst.arguments[x][0].wordnum
			index1_type=inst.arguments[x][1]
			# print "yes"
		except Exception, e:
			try:
				# print "no"
				# print inst.arguments[x][0].pieces[0]
				
				index1_height= inst.arguments[x][0].pieces[0].height
				index1=inst.arguments[x][0].pieces[0].wordnum
				index1_type=inst.arguments[x][1]

				
			except Exception, e:
				# print "no-no"
				# print inst.arguments[x][0].pieces[0].pieces[0]
				
				index1_height= inst.arguments[x][0].pieces[0].pieces[0].height
				index1=inst.arguments[x][0].pieces[0].pieces[0].wordnum
				index1_type=inst.arguments[x][1]
				
		else:
			pass

		
		
		# print index1,index1_height,index1_type,index_pred
		

		leaves_pos= t.treepositions('leaves')
		pred=t[leaves_pos[index_pred]]
		const=t[leaves_pos[index1][0:len(leaves_pos[index1])-index1_height-1]]
		target=index1_type
		head_word=t[leaves_pos[index1]]
		(phrase,hwpos)= phrase_type(leaves_pos,t,index1,index1_height)
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
		df=df.append({'Roleset':inst.roleset,'Form':infl.form,'Tense':infl.tense,'Voice':infl.voice,'Predicate':pred,'Target':target,'Head Word':head_word,'Phrase type':phrase,'Relative Position':rel_pos,'Path':path,'Head Word POS':hwpos,'V POS':vpos},ignore_index=True)
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

for x in xrange(0,1000):
	print x ," - - - - - - - - - - - - - - - - - -";
	createCSV(x);
df.to_csv("data_roleset.csv")
# cat_dict = df.T.to_dict().values()
# vectorizer = DV( sparse = False )
# vec_x_cat_train = vectorizer.fit_transform( cat_dict )


