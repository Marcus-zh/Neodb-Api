from functools import lru_cache
from vercel_kv_sdk import KV
import dotenv
import requests
import json
from os import environ

dotenv.load_dotenv()

kv = KV()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'http://redish101.top',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7',
    'Connection': 'keep-alive'
}

# 用装饰器来缓存get_theme_color函数的返回值
@lru_cache(maxsize=None)
def get_theme_color(uuid,cover_image_url):
  theme_color = kv.get(uuid)

  if theme_color is not None:
      # 如果在 Redis 缓存中找到主题色，直接返回它
      return theme_color
  else:
      try:
          # 发起请求获取数据
          print(cover_image_url)
          response = requests.get(f"{environ.get('IMG2COLOR')}{cover_image_url}",headers=headers)
          data = json.loads(response.text)

          # 从响应中提取主题色
          theme_color = data.get('RGB')
          # print(theme_color)

          if theme_color is not None:
              # 将主题色存入 Redis 缓存
              kv.set(uuid,theme_color)

          return theme_color
      except Exception as e:
          print(f"Error: {e}")
          return None
def process_item(item):
    uuid = item['item']['uuid']
    cover_image_url = item['item']['cover_image_url']
    theme_color = get_theme_color(uuid, cover_image_url)
    item['item']['color'] = theme_color
