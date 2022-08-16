#import pandas
#import numpy
#import pyrebase
#from flask import Flask, request, jsonify
#from sklearn.metrics.pairwise import cosine_similarity
#from sklearn.feature_extraction.text import CountVectorizer

#config = {
#    'apiKey': "AIzaSyBqdBMwUd7wp_FioYW_PdaU5iGStTGeJ1w",
#    'authDomain': "alvin-9f1e7.firebaseapp.com",
#    'databaseURL': "https://alvin-9f1e7.firebaseio.com",
#    'projectId': "alvin-9f1e7",
#    'storageBucket': "alvin-9f1e7.appspot.com",
#    'messagingSenderId': "264584905386",
#    'appId': "1:264584905386:web:32911ca6805d8a4f6e46d3"
#}

#firebase = pyrebase.initialize_app(config)
#db = firebase.database()
#columns = ['postid', 'location', 'price', 'bedrooms']

#houses = pandas.DataFrame(columns=columns)

#items = db.child("Posts").get()
#for item in items:
#    houses.loc[len(houses)] = [item.val()['postid'], item.val()['location'], item.val()['price'],
#                               item.val()['bedrooms']]

# print(houses.head(8))
# houses=pandas.read_csv('rent_apts.csv')
# houses.reset_index(inplace=True)
# houses=houses.rename(columns={'index':'house_id'})

#necesarrycolumns = ['location', 'price', 'bedrooms']


#def get_important_columns(data):
#    important_columns = []
#    for i in range(0, data.shape[0]):
#        important_columns.append(data['location'][i] + '' + str(data['price'][i]) + '' + str(data['bedrooms'][i]))
#    return important_columns


#houses['important columns'] = get_important_columns(houses)
#houses.reset_index(inplace=True)
#houses = houses.rename(columns={'index': 'id'})

#cm = CountVectorizer().fit_transform(houses['important columns'])
#cs = cosine_similarity(cm)

#allhouses = houses['postid'].unique()
#listhouses = allhouses.tolist()

#post="-N98QoFUIPF7F7KX1yi4"
#id=listhouses.index(post)

#scores=list(enumerate(cs[id]))
#sorted_list=sorted(scores,key=lambda x:x[1],reverse=True)
#sorted_list=sorted_list[1:]
#j=0

#final=['postid','location','rank']
#df=pandas.DataFrame(columns=final)

#for item in sorted_list:
#    location=houses[houses.id==item[0]]['location'].values[0]
#    postid=houses[houses.id==item[0]]['postid'].values[0]
#    df.loc[len(df)]=[postid,location,j+1]
#    j=j+1
#    if j>4:
#        break

#print(df)
