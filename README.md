# Neodb-Api
[neodb.social](https://neodb.social/) 是一个致力于为联邦宇宙居民提供一个自由开放互联的书籍、电影、音乐和游戏收藏评论空间。NeoDB 的源代码来自 NiceDB，NiceDB 由里瓣社区众筹开发。

个人主页[Marcus233@mastodon.social](https://neodb.social/users/marcus233@mastodon.social/)

参考[@immmmm](https://immmmm.com/hi-neodb-api/)和[@eallion](https://eallion.com/neodb/)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FMarcusYYDS%2FNeodb-Api&project-name=Neodb-Api&repository-name=Neodb-Api&env=ACCESSTOKEN&envDescription=Enter%20your%20accesstoken%20from%20https%3A%2F%2Feallion.com%2Fneodb_token.)

## 使用方法

### 申请ASSECCTOKEN

见[@eallion](https://eallion.com/neodb_token)

### 测试

<link rel="stylesheet" type="text/css" href="https://jsd.onmicrosoft.cn/gh/swagger-api/swagger-ui/dist/swagger-ui.css">
<div id="swagger-ui"></div>

<script src="https://jsd.onmicrosoft.cn/gh/swagger-api/swagger-ui/dist/swagger-ui-bundle.js"></script>
<script src="https://jsd.onmicrosoft.cn/gh/swagger-api/swagger-ui/dist/swagger-ui-standalone-preset.js"></script>

<script>
window.onload = function() {
  const ui = SwaggerUIBundle({
    url: "http://127.0.0.1:5000/apispec_1.json",
    dom_id: '#swagger-ui',
    presets: [
      SwaggerUIBundle.presets.apis,
      SwaggerUIStandalonePreset
    ]
  })

  window.ui = ui
}
</script>

### 传入

同[官方](https://neodb.social/developer/#/default/journal_api_list_marks_on_shelf)

| **参数**   | **是否必要** | **类型** | **默认值** | **可选**                                       |
|:--------:|:--------:|:------:|:-------:|:--------------------------------------------:|
| type     | 是        | str    | 无       | wishlist / progress / complete               |
| category | 否        | str    | 全部      | book/movie/tv/music/game/podcast/performance |
| page     | 否        | int    | 1       | 1-最大页数                                       |

### 返回

同[官方](https://neodb.social/developer/#/default/journal_api_list_marks_on_shelf)

```json
{
  "data": [
    {
      "shelf_type": "wishlist",
      "visibility": 2,
      "item": {
        "uuid": "string",
        "url": "string",
        "api_url": "string",
        "category": "book",
        "parent_uuid": "string",
        "display_title": "string",
        "external_resources": [
          {
            "url": "string"
          }
        ],
        "title": "string",
        "brief": "string",
        "cover_image_url": "string",
        "rating": 0,
        "rating_count": 0
      },
      "created_time": "2023-09-23T10:58:23.814Z",
      "comment_text": "string",
      "rating_grade": 10,
      "tags": [
        "string"
      ]
    }
  ],
  "pages": 0,
  "count": 0
}
```

### 示例

见[@石姐姐](https://blog.kouseki.cn/)

### 代码讲解

### 1. 引入模块：
  ```python
  from flask import Flask,request
  import requests
  import json
  from os import environ
  ```
  - 引入 Flask 框架和用于处理 HTTP 请求的 `request` 模块。
  - 引入用于发送 HTTP 请求的 `requests` 模块。
  - 引入处理 JSON 数据的模块。
  - 引入操作系统相关功能，用于获取环境变量。

### 2. 声明 Flask 应用：
   ```python
   app = Flask(__name__)
   ```
   创建了一个 Flask 应用实例。

### 3. 处理逻辑：
   - `@app.route('/', methods=['GET'])`: 定义了一个路由，当接收到 GET 请求时，将会执行下面的 `getdata` 函数。

   - `def getdata()`: 定义了名为 `getdata` 的函数，用于处理 GET 请求。

   - 获取环境变量中的 `ACCESSTOKEN`：
     ```python
     token = environ.get('ACCESSTOKEN')
     ```

   - 设置请求头：
     ```python
     headers = {
       'accept': 'application/json',
       'Authorization': f'Bearer {token}',
     }
     ```

   - 获取请求参数：
     ```python
     cate = request.args.get('category')
     page = request.args.get('page')
     type = request.args.get('type')
     ```

   - 判断参数是否完整，如果 `token` 和 `type` 均存在：
     ```python
     if token and type:
     ```

   - 尝试发起请求：
     ```python
     response = requests.get(f"https://neodb.social/api/me/shelf/{type}?category={cate}&page={page}", headers=headers)
     ```

   - 解析响应：
     ```python
     data = json.loads(response.text)
     ```

   - 添加 `code` 和 `msg` 字段：
     ```python
     data['code'] = response.status_code
     data['msg'] = "succeed"
     ```

   - 打印响应的数据：
     ```python
     print(data)
     ```

   - 返回响应的数据：
     ```python
     return data
     ```

   - 如果发生异常，返回一个带有错误信息的 JSON 响应：
     ```python
     except Exception as e:
       print(e)
       return {
         "code": 0,
         "msg": str(e)
       }, 400
     ```

   - 如果缺少 `type` 参数，返回一个带有错误信息的 JSON 响应：
     ```python
     else:
       print("缺失type,详情请见https://blog.marcus233.top/wiki/neodbapi/index.html")
       return {
         "code": 0,
         "msg": "缺失type,详情请见https://blog.marcus233.top/wiki/neodbapi/index.html"
       }, 400
     ```

### 4. 运行应用：
   ```python
   if __name__ == '__main__':
       app.run()
   ```

--由ChatGPT生成--
