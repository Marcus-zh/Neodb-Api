import uvicorn
from fastapi import FastAPI, HTTPException, status
import requests
import json
from os import environ
from redis_color import kv, process_item
import threading
from typing import TypeVar, Optional
from pydantic import BaseModel

app = FastAPI(
    title="Marcus的api",
    version="0.0.1",
    terms_of_service="http://blog.marcus233.top/",
    contact={
        "name": "Marcus",
        "url": "https://blog.marcus233.top/",
        "email": "marcus-zh@qq.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

T = TypeVar('T')


class WebResponse(BaseModel):
    code: int
    msg: Optional[str]
    data: Optional[T]
    pages: Optional[int]
    count: Optional[int]


descr = """
获取用户书架的所有标记的列表\n
书架的类型应该是 `wishlist` / `progress` / `complete` 中的一个；类别是可选的，如果没有指定，将返回所有类别的标记。
"""


@app.get("/", name='获取用户书架的所有标记的列表', description=descr, response_model=WebResponse)
def getdata(type: str, category: str, page: int, theme: str):
    # 获取环境变量中的ACCESSTOKEN
    token = environ.get('ACCESSTOKEN', None)
    threads = []
    # 设置请求头
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}',
        'Referer': 'http://redish101.top',
    }

    if not token or not type:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="缺失type,详情请见https://blog.marcus233.top/wiki/neodbapi/index.html")

    try:
        # 发起请求
        response = requests.get(f"https://neodb.social/api/me/shelf/{type}?category={category}&page={page}",
                                headers=headers)
        # 解析响应
        data = json.loads(response.text)

        if environ.get('USE_REDIS'):
            if environ.get('USE_I2C') and theme == "true":
                pagedata = f"page-{page}-{type}-{category}-theme"
            else:
                pagedata = f"page-{page}-{type}-{category}"

            kvdata = kv.get(pagedata)
            kvcount = kv.get("count")

            if kvdata and str(data['count']) == str(kvcount):
                return WebResponse(code=response.status_code, msg="succeed", data=json.loads(kvdata)).dict()
            else:
                if environ.get('USE_I2C') and theme and theme[0] == "true":
                    for i in data['data']:
                        thread = threading.Thread(target=process_item, args=(i,))
                        threads.append(thread)
                        thread.start()
                    for thread in threads:
                        thread.join()

                kv.set("count", data['count'])
                kv.set(pagedata, json.dumps(data))
                return WebResponse(data=data["data"], code=response.status_code, msg="succeed", pages=data["pages"],
                                  count=data["count"]).dict()

        else:
            return WebResponse(data=data["data"], code=response.status_code, msg="succeed", pages=data["pages"],
                              count=data["count"]).dict()
    except Exception as e:
        return WebResponse(data="", code=0, msg=str(e), pages=0, count=0).dict(), status.HTTP_500_INTERNAL_SERVER_ERROR


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, host='0.0.0.0')
