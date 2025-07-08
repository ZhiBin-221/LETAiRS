import os
import pandas as pd
import json
import glob

# Step 1: Excel to JSONL
def excel_to_jsonl(input_excel, output_jsonl):
    df = pd.read_excel(input_excel, dtype=str).fillna('None')
    with open(output_jsonl, 'w', encoding='utf-8') as jsonl_file:
        for _, row in df.iterrows():
            jsonl_file.write(json.dumps(row.to_dict(), ensure_ascii=False) + '\n')
    print(f"Excel 檔案已成功轉換為 JSONL 檔案: {output_jsonl}")

# Step 2: Add Prompt to JSONL
def add_prompt_to_jsonl(input_jsonl, output_jsonl, prompt_prefix):
    with open(input_jsonl, "r", encoding="utf-8") as infile:
        data = [json.loads(line) for line in infile]

    converted_data = []
    for item in data:
        # 確保每個項目都有必要欄位
        if all(key in item for key in ["原始資料", "是否有關議題", "是否支持議題", "關鍵句"]):
            prompt = prompt_prefix + item["原始資料"]
            completion = (
                f"是否有關議題: {item['是否有關議題']}, "
                f"是否支持議題: {item['是否支持議題']}, "
                f"關鍵句: {item['關鍵句']}"
            )
            converted_data.append({"prompt": prompt, "completion": completion})
        else:
            print(f"跳過不完整條目：{item}")

    with open(output_jsonl, "w", encoding="utf-8") as outfile:
        for entry in converted_data:
            outfile.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"已處理並儲存新的 JSONL：{output_jsonl}")

# Step 3: Convert to ChatGPT Format
def convert_to_chatgpt_format(input_jsonl, output_jsonl):
    with open(input_jsonl, 'r', encoding='utf-8') as infile, open(output_jsonl, 'w', encoding='utf-8') as outfile:
        for line in infile:
            data = json.loads(line.strip())
            if "prompt" in data and "completion" in data:
                chat_format = {
                    "messages": [
                        {"role": "user", "content": data["prompt"].strip()},
                        {"role": "assistant", "content": data["completion"].strip()}
                    ]
                }
                outfile.write(json.dumps(chat_format, ensure_ascii=False) + '\n')
            else:
                print(f"缺少必要欄位的項目：{data}")
    print(f"轉換完成，已保存至 {output_jsonl}")

# 主程式執行
if __name__ == "__main__":
    # 路徑設定
    input_excel = r"XXXX.xlsx"  # 替換為您的 Excel 檔案路徑
    intermediate_jsonl = "XXXX.jsonl"  # JSONL 暫存檔
    processed_jsonl = r"XXXX.jsonl"  # JSONL 加入 prompt 後的檔案
    final_output = "chatgpt_format.jsonl"  # 最終輸出檔案

    # Prompt 前綴
    prompt_prefix = "123"

    # 執行步驟
    excel_to_jsonl(input_excel, intermediate_jsonl)
    add_prompt_to_jsonl(intermediate_jsonl, processed_jsonl, prompt_prefix)
    convert_to_chatgpt_format(processed_jsonl, final_output)
