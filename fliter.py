import pandas as pd
import emoji, re, os
from ckip_transformers.nlp import CkipWordSegmenter, CkipNerChunker
from tqdm import tqdm
ws = CkipWordSegmenter(model='bert-base')
ner = CkipNerChunker(model="bert-base")
def remove_emoji(sen):
  res = emoji.replace_emoji(sen,replace = "")
  return res

def filter_str(desstr, restr=''):
    res = re.compile("[^\\u4e00-\\u9fa5^0-9^、^,^，^。^？^！^+]")
    return res.sub(restr, desstr)

def remove_command(sen):
  new_sen = ""
  left_command = ['(','[','【','{','〔']
  right_command = [')',']','】','}','〕']
  f = False
  for ch in sen:
    if ch in left_command:
      f = True
    if f == False:
      new_sen += ch
    if ch in right_command:
      f = False
  return new_sen

idiot_words = ["http", "html", "<br>", "<br />", "#"]
def filter_keyword(sen):
  tmp = ws([sen])
  tmp = tmp[0]
  for i in tqdm(idiot_words):
    tmp2 = []
    for j in tmp:
      if i not in j:
        tmp2.append(j)
    tmp = tmp2.copy()
  s = ""
  for i in tmp:
    s += i
  return s

def people_detect(sen):
  tmp = ner([sen])
  if len(tmp) > 0:
    if tmp[0][0].ner == 'PERSON':
      sen = sen[(tmp[0][0].idx)[1]:]
  return sen

def filter(data):
  new_data, article = [], []
  for i in tqdm(data):
    tmp = str(i)
    # print(tmp)
    if tmp == None:
      continue
    if len(tmp) > 300:
      try:
        tmp = remove_command(tmp)
        tmp = filter_keyword(tmp)
        tmp = filter_str(tmp)
      except:
        continue
      article.append(tmp)
    elif len(tmp) > 10:
      try:
        tmp = remove_emoji(tmp)
        tmp = remove_command(tmp)
        tmp = filter_keyword(tmp)
        tmp = people_detect(tmp)
        tmp = filter_str(tmp)
      except:
        continue
      if len(tmp)> 3:
        new_data.append(tmp)
  return new_data, article


data = r'C:\Users\BIN\Desktop\論文資料\Opview_Insight_Result_AI自駕車_2024-0717.xlsx'

df = pd.read_excel(data)
new_data, article = filter(df['內容'])

dup = []
word_count = []
id = 1
file = open(r'C:\Users\BIN\Desktop\論文資料\Opview_Insight_Result_AI自駕車_2024-0717','w',encoding='utf-8') # output file name should change or it will be covered
for i in new_data:
  if i not in dup:
    tmp = str(id) + ". " + i + '\n'
    id += 1
    file.write(tmp)
    word_count.append(len(i))
    dup.append(i)
id = 1

dup = []
word_count = []
id = 1
file = open(r'C:\Users\BIN\Desktop\論文資料\Opview_Insight_Result_AI自駕車_2024-0717文章.txt','w',encoding='utf-8') # output file name should change or it will be covered
for i in article:
  if i not in dup:
    tmp = str(id) + ". " + i + '\n'
    id += 1
    file.write(tmp)
    word_count.append(len(i))
    dup.append(i)
id = 1


print(new_data)
print(article)