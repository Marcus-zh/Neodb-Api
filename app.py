from flask import Flask,request
import requests
import json
from os import environ

app = Flask(__name__)

@app.route('/', methods=['GET'])
def getdata():
  # 获取环境变量中的ACCESSTOKEN
  token=environ.get('ACCESSTOKEN')
  # 设置请求头
  headers={
    'accept': 'application/json',
    'Authorization': f'Bearer {token}',
  }
  # 获取请求参数
  cate=request.args.get('category')
  page=request.args.get('page')
  type=request.args.get('type')
  # 判断参数是否完整
  if token and cate and page and type:
    try:
      # 发起请求
      response=requests.get(f"https://neodb.social/api/me/shelf/{type}?category={cate}&page={page}",headers=headers)
      # 解析响应
      data=json.loads(response.text)
      # 添加code和msg字段
      data['code'] = response.status_code
      data['msg'] = "succeed"
      print(data)
      return data
    except Exception as e:
      print(e)
      return {
        "code": 0,
        "msg": str(e)
      },400
  else:
    print("缺失category或page或type,详情请见https://blog.marcus233.top/wiki/neodbapi/index.html")
    return {
      "code": 0,
      "msg": "缺失category或page或type,详情请见https://blog.marcus233.top/wiki/neodbapi/index.html"
      },400

if __name__ == '__main__':
    app.run()