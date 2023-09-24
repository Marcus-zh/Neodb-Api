from flask import Flask,request
import requests
import json
from os import environ
from redis_color import get_theme_color,kv,process_item
import threading

app = Flask(__name__)

@app.route('/', methods=['GET'])
def getdata():
  # 获取环境变量中的ACCESSTOKEN
  token=environ.get('ACCESSTOKEN')
  threads = []
  # 设置请求头
  headers={
    'accept': 'application/json',
    'Authorization': f'Bearer {token}',
    'Referer': 'http://redish101.top',
  }
  # 获取请求参数
  cate=request.args.get('category')
  page=request.args.get('page')
  type=request.args.get('type')
  theme=request.args.get('theme')
  print(theme)
  # 判断参数是否完整
  if token and type:
    try:
      # 发起请求
      response=requests.get(f"https://neodb.social/api/me/shelf/{type}?category={cate}&page={page}",headers=headers)
      # 解析响应
      data=json.loads(response.text)
      print("请求成功")
      if environ.get('USE_REDIS'):
        if environ.get('USE_I2C') and theme=="true":
          pagedata=f"page-{page}-theme"
        else:
          pagedata=f"page-{page}"
        print("请求缓存")
        kvdata=kv.get(pagedata)
        kvcount=kv.get("count")
        print(kvdata)
        if kvdata and str(data['count'])==str(kvcount):
          print("使用缓存")
          return json.loads(kvdata)
        else:
          # 添加code和msg字段
          print("不使用缓存")
          data['code'] = response.status_code
          data['msg'] = "succeed"
          if environ.get('USE_I2C') and theme=="true":
            print("提取主题色")
            for i in data['data']:
              thread = threading.Thread(target=process_item, args=(i,))
              threads.append(thread)
              print("线程+1")
              thread.start()
            for thread in threads:
              thread.join()
          # print(data)
          print("设置缓存")
          kv.set("count",data['count'])
          kv.set(pagedata,json.dumps(data))
          return data
      else:
        data['code'] = response.status_code
        data['msg'] = "succeed"
        return data
    except Exception as e:
      print(e)
      return {
        "code": 0,
        "msg": str(e)
      },400
  else:
    print("缺失type,详情请见https://blog.marcus233.top/wiki/neodbapi/index.html")
    return {
      "code": 0,
      "msg": "缺失type,详情请见https://blog.marcus233.top/wiki/neodbapi/index.html"
      },400

if __name__ == '__main__':
    app.run()