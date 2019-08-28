
import requests
import json
from data import data
from pymongo import MongoClient
# mongo = MongoClient(host='127.0.0.1', port=27017)
# db = mongo["JIU"]
# data = db["jiu"].find({},{"_id":0})


APP_ID = "appid"
APP_SECRET ="app_secret"
ENV="云名称"
TEST_COLLECTION="集合名称"

HEADER = {'content-type': 'application/json'}

WECHAT_URL="https://api.weixin.qq.com/"

'''
获取小程序token
'''
def get_access_token():
    url='{0}cgi-bin/token?grant_type=client_credential&appid={1}&secret={2}'.format(WECHAT_URL,APP_ID,APP_SECRET)
    response =requests.get(url)
    result=response.json()
    print(result)
    return result['access_token']

'''
新增集合
'''
def add_collection(accessToken):
    url='{0}tcb/databasecollectionadd?access_token={1}'.format(WECHAT_URL,accessToken)
    data={
        "env":ENV,
        "collection_name":"big"
    }
    response  = requests.post(url,data=json.dumps(data),headers=HEADER)
    print('新增集合：'+response.text)




'''
新增数据
'''
def add_data(accessToken,item):
    url='{0}tcb/databaseadd?access_token={1}'.format(WECHAT_URL,accessToken)
    new_item = "{data:" + json.dumps(item) +"}"
    query='''db.collection("{}").add({})'''.format(TEST_COLLECTION,new_item)

    data={
        "env":ENV,
        "query":query
    }
    response  = requests.post(url,data=json.dumps(data),headers=HEADER)
    print('2.新增数据：'+response.text)


'''
查询数据
'''
def query_data(accessToken):
    url='{0}tcb/databasequery?access_token={1}'.format(WECHAT_URL,accessToken)
    query='''db.collection("{}").limit(50).skip(1).get()'''.format(TEST_COLLECTION)

    data={
        "env":ENV,
        "query":query
    }
    response  = requests.post(url,data=json.dumps(data),headers=HEADER)
    print('3.查询数据：'+response.text)
    result=response.json()
    for item in result["data"]:
        print(item)

    resultValue =json.loads(result['data'][0])
    return resultValue['_id']

'''
删除数据
'''
def delete_data(accessToken,id):
    url='{0}tcb/databasedelete?access_token={1}'.format(WECHAT_URL,accessToken)
    query='''db.collection("test_2").doc("{0}").remove()'''.format(id)

    data={
        "env":ENV,
        "query":query
    }
    response  = requests.post(url,data=json.dumps(data),headers=HEADER)
    print('4.删除数据：'+response.text)

def update_data(accessToken):
    url = '{0}tcb/databaseupdate?access_token={1}'.format(WECHAT_URL, accessToken)
    # query = "db.collection('test_2').doc('age').set({data:{age: 1011}})"
    item = "{age:2}"
    data = "{data:{age:1111}}"
    query = "db.collection('{}').where({}).update({})".format(TEST_COLLECTION,item,data)
    # print(query)

    data = {
        "env": ENV,
        "query": query
    }
    response = requests.post(url, data=json.dumps(data), headers=HEADER)
    print('4.更新数据：' + response.text)


'''
删除集合
'''
def delete_collection(accessToken):
    url='{0}tcb/databasecollectiondelete?access_token={1}'.format(WECHAT_URL,accessToken)
    data={
        "env":ENV,
        "collection_name":TEST_COLLECTION
    }
    response  = requests.post(url,data=json.dumps(data),headers=HEADER)
    print('5.删除集合：'+response.text)

if __name__ =='__main__':
    #获取token
    accessToken=get_access_token()
    
    #新增集合：
    # add_collection(accessToken)
    
    #新增数据
    # add_data(accessToken)
    # for i in data:
    add_data(accessToken, data)
    
    #查询数据
    # id=query_data(accessToken)
    
    #删除数据
    # delete_data(accessToken,id)
    # update_data(accessToken)
    
    #删除集合
    # delete_collection(accessToken)
