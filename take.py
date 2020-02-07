#coding:utf-8
import re
import requests
import os
import json
import urllib.request
import ssl

from urllib.parse import urlsplit
from os.path import basename

ssl._create_default_https_context = ssl._create_unverified_context

headers = {
  'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
  'Accept-Encoding': 'gzip, deflate'
}

# 创建文件夹
def mkdir(path):
  if not os.path.exists(path):
    print('新建文件夹：', path)
    os.makedirs(path)
    return True
  else:
    print('已经存在', path)
    return False

def get_content(qid, headers, path, title):
  tmp_url = "https://www.zhihu.com/node/QuestionAnswerListV2"
  offset = 0

  session = requests.Session()

  pattern = re.compile(r'<div class="zm-editable-content clearfix">((.|\n)*?)</div>')

  while True:
    if offset>-1:
      postdata = {'method': 'next',
            'params': '{"url_token":' + str(qid) + ',"pagesize": "1","offset":' + str(offset) + "}"}
      page = session.post(tmp_url, headers=headers, data=postdata)
      # print(page)
      # print(page.text.encode('latin-1').decode('unicode_escape'))
      # print(type(page.text.encode('latin-1').decode('unicode_escape')))
      print(offset)
      text = json.loads(page.text)["msg"][0]
      result = pattern.findall(text)
      txt = '第'+str(offset+1)+'章\n'
      txt += re.sub(r'<.*?>', '\n', result[0][0])
      # print(type(result[0][0]))

        
      f = open(title+'.txt', 'a', encoding='utf-8')
      # f.write(page.text.encode('latin-1').decode('unicode_escape'))
      # f.write(json.loads(page.text)["msg"][0]+'\n\n')
      # f.write(result[0][0]+'\n\n')
      f.write(txt+'\n\n')
      # f.write(page+'\n\n')
      f.close()

    offset += 1

if __name__ == '__main__':
  # title = '答案'
  # question_id = 348025005
  # 
  # title = '有没有一些很神话类似于聊斋的古代民间故事？'
  # question_id = 359061904
  # 
  # title = '有哪些让人听了毛骨悚然的民间故事？'
  # question_id = 359753722  
  # 
  title = '有什么让人听了背脊发凉的恐怖故事？'
  question_id = 317945181

  zhihu_url = "http://www.zhihu.com/question/{qid}".format(qid=question_id)
  path = str(question_id) + '_' + title
  # 创建文件夹
  # mkdir(path)

  get_content(question_id, headers, path, title)