import xlwings as xw
import openai
import os
from rich.progress import track
from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn


openai.api_key ='XX'    # 替換為您的 API Key


# ChatGPT API 函數
def ChatGPT_api(input_text):
    try:
        response = openai.ChatCompletion.create(
            model="", # 這裡要填入你的模型名稱
            messages=[{"role": "user", "content": input_text}],
            temperature=0.8,    # 溫度
            max_tokens=512,   # 最大token數
            top_p=0.8,       # top_p
            frequency_penalty=1, # 頻率懲罰
            presence_penalty=0, # 存在懲罰
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    excel_wb = xw.Book("XXXXX.excel")                   ### Excel 的檔名
    excel_ws = excel_wb.sheets['sheet1']                          ### 工作表名稱
    length = excel_ws.range('C2').end("down").row        ### 知道一個column有幾個有數據(資料數量)
    with Progress(TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeRemainingColumn(),
                TimeElapsedColumn()) as progress:               ### 進度條設定
        data_tqdm = progress.add_task(description="Asking ChatGPT", total=length) ### 進度條任務設定
        for i in range(0, length-1):                            ### 會把這個A欄位的資料依序詢問ChatGPT並且將回答儲存在右方
            input_text = excel_ws.cells(str(i+2), 'G').value    ### 問題在excel表的哪一格, cells(row, column)
            ans = ChatGPT_api(input_text)                       ### 透過api詢問ChatGPT
            excel_ws.cells(str(i+2), 'H').value = ans           ### 將ChatGPT的回答儲存到哪一格, cells(row, column)
            excel_wb.save()                                     ### 將回答儲存到excel
            progress.advance(data_tqdm, advance=1)              ### 進度條進度+1
