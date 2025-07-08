import jieba
import xlwings as xw
from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn
from rouge_chinese import Rouge
from concurrent.futures import ThreadPoolExecutor, as_completed

# 定義 ROUGE 測試函數
def rouge_test(hypothesis, reference):
    if not hypothesis or not reference:
        return {"ROUGE-1": 0.0, "ROUGE-2": 0.0, "ROUGE-L": 0.0}
    
    hypothesis = ' '.join(jieba.cut(hypothesis))
    reference = ' '.join(jieba.cut(reference))
    
    rouge = Rouge()
    scores = rouge.get_scores(hypothesis, reference)[0]
    return {
        "ROUGE-1": scores['rouge-1']['f'],
        "ROUGE-2": scores['rouge-2']['f'],
        "ROUGE-L": scores['rouge-l']['f']
    }

# 分批處理函數
def process_batch(start, end, excel_ws, executor):
    batch_data = []
    for i in range(start, end + 1):
        hypothesis = excel_ws.cells(i, "K").value
        reference = excel_ws.cells(i, "F").value
        batch_data.append((i, hypothesis, reference))

    # 計算 ROUGE 分數
    futures = {executor.submit(rouge_test, hyp, ref): row for row, hyp, ref in batch_data}
    batch_results = []
    for future in as_completed(futures):
        row = futures[future]
        rouge_scores = future.result()
        batch_results.append((row, rouge_scores))
    return batch_results

if __name__ == '__main__':
    try:
        # 設置 Excel 的 COM 介面參數
        app = xw.App(visible=False)  # 隱藏 Excel 應用程式
        app.screen_updating = False  # 禁用螢幕更新

        # 打開 Excel 檔案和工作表
        excel_wb = app.books.open(r"C:\Users\BIN\Desktop\論文資料\NO_MORE_DATA\GPT\self_drive_all_data_test_GPT_FINETUNE_DONE.xlsx")
        excel_ws = excel_wb.sheets['FT_1000']

        # 獲取資料範圍長度
        total_rows = excel_ws.range("C2").end("down").row

        # 找出上次執行結束的位置
        start_row = 2
        for i in range(total_rows, 1, -1):
            if excel_ws.cells(i, "N").value is not None:
                start_row = i + 1
                break

        # 分批次處理的設定
        batch_size = 100  # 每批處理 100 行數據
        total_batches = (total_rows - start_row + 1) // batch_size + 1

        # 進度條設定
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            TimeElapsedColumn(),
        ) as progress:
            data_tqdm = progress.add_task(description="Calculating ROUGE", total=total_rows - start_row + 1)

            # 多執行緒處理分批數據
            with ThreadPoolExecutor(max_workers=4) as executor:
                for batch_start in range(start_row, total_rows + 1, batch_size):
                    batch_end = min(batch_start + batch_size - 1, total_rows)
                    batch_results = process_batch(batch_start, batch_end, excel_ws, executor)

                   
                    for row, scores in batch_results:
                        excel_ws.cells(row, "N").value = scores["ROUGE-1"]
                        excel_ws.cells(row, "O").value = scores["ROUGE-2"]
                        excel_ws.cells(row, "P").value = scores["ROUGE-L"]
                    excel_wb.save()  

                   
                    progress.advance(data_tqdm, advance=(batch_end - batch_start + 1))

        print("ROUGE 分數計算完成！結果已儲存。")

    except Exception as e:
        print(f"發生錯誤: {e}")

    finally:
        # 關閉 Excel 應用程式
        excel_wb.close()
        app.quit()
