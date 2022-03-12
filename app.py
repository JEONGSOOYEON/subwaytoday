import json

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


from bson import json_util, ObjectId
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
import sys
# from bson.json_util import dumps
# from json import JSONEncoder

# client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://test:test@52.79.241.120', 27017)
db = client.dbhappy


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/check')
def check():
    return render_template('result.html')


@app.route('/listing')
def listing():
    return render_template('list.html')


#menu-sadnwich api
@app.route('/api/list/sandwich', methods=['GET'])
def all_sandwich():
    sandwiches = list(db.a_sandwich.find({}, {'_id': False}))
    return jsonify({'all_sandwich': sandwiches})

# menu-bread api
@app.route('/api/list/bread', methods=['GET'])
def all_bread():
    breads = list(db.a_bread.find({}, {'_id': False}))
    return jsonify({'all_bread': breads})

#menu-sauce api
@app.route('/api/list/sauce', methods=['GET'])
def all_sauce():
    sauces = list(db.a_sauce.find({}, {'_id': False}))
    return jsonify({'all_sauce': sauces})

#menu-cheese api
@app.route('/api/list/cheese', methods=['GET'])
def all_cheese():
    cheese = list(db.a_cheese.find({}, {'_id': False}))
    return jsonify({'all_cheese': cheese})


# 유저가 선택한 주메뉴, 빵, 치즈, 소스 data를 db에 생성하는 API
@app.route('/menu', methods=['POST'])
def menuPost():
    sandwich_receive = request.form['sandwich_give']
    bread_receive = request.form['bread_give']
    sauce_receive = request.form.getlist('sauce_give')
    cheese_receive = request.form['cheese_give']
    comment_receive = request.form['comment_give']
    img_find = request.form['find_give']
    user = db.a_sandwich.find_one({'name': img_find})['img']


    doc = {
        'sandwich': sandwich_receive,
        'bread': bread_receive,
        'sauce': sauce_receive,
        'cheese': cheese_receive,
        'comment': comment_receive,
        'img': user,
        'like': 0,
    }
    objectid = db.userchoice.insert_one(doc).inserted_id
    db.userchoice.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '조합이 완료되었습니다!'})



#lastpage로 조합 내려주기
@app.route('/check/check', methods=['GET'])
def last_page():
    mychoices = list(db.userchoice.find({}, {'_id': False}).sort("_id", -1).limit(1))
    return jsonify({'all_mychoices': mychoices})

#최신순 data 내려주기
@app.route('/listing/list', methods=['GET'])
def mychoice_recent ():
    mychoices_recent = list(db.userchoice.find({}, {'_id': False}).sort("_id", -1))
    return jsonify({'all_mychoices': mychoices_recent})


#좋아요순 data 내려주기
@app.route('/listing/popular', methods=['GET'])
def all_popular():
    popularchoices = list(db.userchoice.find({}).sort("like", -1).limit(10))
    popular = json.loads(json_util.dumps(popularchoices))
    return jsonify({'all_popularchoices': popular})

#좋아요 api
@app.route('/listing/like', methods=['POST'])
def like_sandwich():
    like_receive = request.form['like_give']
    target_id = db.userchoice.find_one({'_id':ObjectId(like_receive)})
    # print(target_id, file=sys.stdout)
    current_like = target_id['like']

    new_like = current_like + 1
    db.userchoice.update_one({'_id': ObjectId(like_receive)}, {'$set': {'like': new_like}})

    return jsonify({'msg':'좋아요 완료!'})


#좋아요 api
# @app.route('/listing', methods=['POST'])
# def like_sandwich():
#     like_receive = request.form['like_give']
#
#     target_sandwiche = db.userchoice.find_one({'main': name_receive})
#     current_like = target_star['like']
#
#     new_like = current_like + 1
#     db.mystar.update_one({'name': name_receive}, {'$set': {'like': new_like}})
#     return jsonify({'msg':'좋아요 완료!'})

# @app.route('/result', methods=['GET'])
# def show_mychoice():
#     mychoice = list(db.userchoice.find({}, {'_id': False}))
#     return jsonify({'all_choices': mychoice})
#
#
# @app.route('/result', methods=['POST'])
# def save_comment():
#     comment_receive = request.form['comment_give']
#     doc = {
#         'comment': comment_receive
#     }
#     db.savecomment.insert_one(doc)
#     return jsonify({'result': 'success', 'msg': '완료되었습니다!'})


# db.total.aggregate([
#     {$lookup:{
#     from: "userchoice",
#     localField: "savecomment",
#     foreignField: "_id",
#     as: "total",
# }
# }
# ])


# subway_dict_list = [{
#     'sandwich': sandwich_receive,
#     'bread': bread_receive,
#     'sauce': sauce_receive,
#     'cheese': cheese_receive
# }]
# df = pd.DataFrame(subway_dict_list, columns=['sandwich', 'bread', 'sauce', 'cheese'])
#
# subway_comment_list = [{
#    'comment': comment_receive
# }]
# df2 = pd.DataFrame(subway_comment_list, columns= ['comment'])
#
# # df.append(df2) 아래로 테이블 추가


# def merge_data():
#    return .join(['num' for nume in xrage(1.10)])

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
