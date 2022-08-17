import Recommender
import pandas
import numpy
import pyrebase
import Content
from sklearn.model_selection import train_test_split
from flask import Flask, request, jsonify
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

config = {
    'apiKey': "AIzaSyBqdBMwUd7wp_FioYW_PdaU5iGStTGeJ1w",
    'authDomain': "alvin-9f1e7.firebaseapp.com",
    'databaseURL': "https://alvin-9f1e7.firebaseio.com",
    'projectId': "alvin-9f1e7",
    'storageBucket': "alvin-9f1e7.appspot.com",
    'messagingSenderId': "264584905386",
    'appId': "1:264584905386:web:32911ca6805d8a4f6e46d3"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

columns = ['userid', 'postid']
history1 = pandas.DataFrame(columns=columns)
hist = db.child("History").get()

columns2 = ['postid', 'location', 'price', 'bedrooms']
houses = pandas.DataFrame(columns=columns2)
items = db.child("Posts").get()

for item in hist:
    history1.loc[len(history1)] = [item.val()['userid'], item.val()['postid']]

history = history1.drop_duplicates(keep='first')

for item in items:
    houses.loc[len(houses)] = [item.val()['postid'], item.val()['location'], item.val()['price'],
                               item.val()['bedrooms']]


def get_important_columns(data):
    important_columns = []
    for i in range(0, data.shape[0]):
        important_columns.append(data['location'][i] + '' + str(data['price'][i]) + '' + str(data['bedrooms'][i]))
    return important_columns


houses['important columns'] = get_important_columns(houses)
houses.reset_index(inplace=True)
houses = houses.rename(columns={'index': 'id'})

#using in content based recommendation for each house
cm = CountVectorizer().fit_transform(houses['important columns'])
cs = cosine_similarity(cm)

users = history['userid'].unique()
all_users = users.tolist()
allhouses = houses['postid'].unique()
listhouses = allhouses.tolist()

train_data, test_data = train_test_split(history, test_size=0.2, random_state=3)
is_model = Content.house_recommender()
is_model.create(train_data, 'userid', 'postid')

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello world come here"


@app.route("/content", methods=['POST'])
def content():
    postid = request.form.get('postid')
    id = listhouses.index(postid)

    scores = list(enumerate(cs[id]))
    sorted_list = sorted(scores, key=lambda x: x[1], reverse=True)
    sorted_list = sorted_list[1:]

    final = ['postid', 'location', 'rank']
    df = pandas.DataFrame(columns=final)

    j = 0
    for item in sorted_list:
        location = houses[houses.id == item[0]]['location'].values[0]
        posts = houses[houses.id == item[0]]['postid'].values[0]

        df.loc[len(df)] = [posts, location, j + 1]
        j = j + 1
        if j > 4:
            break
    rec = df['postid'].unique()
    results = rec.tolist()

    #similar = is_model.similar_items([post])
    #similarlist = similar['house_id'].unique()
    #tolist = similarlist.tolist()

    #results.extend(tolist)
    #results = list(dict.fromkeys(results))

    return jsonify({'postlist': results})


@app.route("/collaborative", methods=['POST'])
def collaborative():
    model = Recommender.house_recommender()
    model.create(train_data, 'userid', 'postid')

    user = request.form.get('userid')
    position = all_users.index(user)
    user_id = users[position]

    user_results = model.recommend(user_id)
    user_results_list = user_results['house_id'].unique()
    final_list = user_results_list.tolist()

    return jsonify({'posts': final_list})


if __name__ == '__main__':
    app.run(debug=True)

# users=history['user_id'].unique()
# apartments=history['house_id'].unique()
# all_users=users.tolist()

# train_data,test_data=train_test_split(history,test_size=0.2,random_state=0)

# model=Recommender.house_recommender()
# model.create(train_data,'user_id','house_id')

# user="user5"
# index=all_users.index(user)
# user_id=users[index]
# print("Recommendation ongoing")
# print("------------------------")
# rec=model.recommend(user_id)
# print(rec)
