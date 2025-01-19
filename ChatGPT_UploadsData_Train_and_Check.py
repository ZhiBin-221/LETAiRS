import openai
import requests
import json

# 設定 API Key
API_KEY = "XX"  # 替換為您的 API Key
openai.api_key = API_KEY

def confirm_action(action_name):
    """
    確認使用者是否要執行指定的操作。
    :param action_name: 操作名稱
    :return: True 表示執行，False 表示跳過
    """
    response = input(f"是否要執行 {action_name}? (y/n): ").strip().lower()
    return response == "y"

def upload_file(file_path):
    """
    上傳訓練文件。
    :param file_path: 文件的完整路徑
    :return: 文件上傳結果
    """
    if not confirm_action("上傳文件"):
        print("已跳過上傳文件步驟。")
        return None
    try:
        response = openai.File.create(
            file=open(file_path, "rb"),
            purpose="fine-tune"
        )
        print("文件上傳成功：", response)
        return response
    except Exception as e:
        print("文件上傳失敗：", e)
        return None

def list_files():
    """
    列出所有已上傳的文件。
    :return: 文件清單
    """
    if not confirm_action("列出已上傳的文件"):
        print("已跳過列出文件步驟。")
        return None
    try:
        result = openai.File.list()
        print("已上傳的文件清單：", result)
        return result
    except Exception as e:
        print("列出文件失敗：", e)
        return None

def create_fine_tuning_job(training_file_id, validation_file_id, model_name):
    """
    建立 Fine-Tuning 任務。
    :param training_file_id: 訓練文件 ID
    :param validation_file_id: 驗證文件 ID
    :param model_name: 模型名稱
    :return: Fine-Tuning 任務建立結果
    """
    if not confirm_action("建立 Fine-Tuning 任務"):
        print("已跳過建立 Fine-Tuning 任務步驟。")
        return None
    url = "https://api.openai.com/v1/fine_tuning/jobs"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "training_file": training_file_id,
        "validation_file": validation_file_id,
        "model": model_name
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print("Fine-Tuning 任務建立結果：", response.json())
        return response.json()
    except Exception as e:
        print("建立 Fine-Tuning 任務失敗：", e)
        return None

def retrieve_fine_tuning_job(job_id):
    """
    查詢 Fine-Tuning 任務狀態。
    :param job_id: Fine-Tuning 任務 ID
    :return: 任務狀態
    """
    if not confirm_action("查詢 Fine-Tuning 任務狀態"):
        print("已跳過查詢任務狀態步驟。")
        return None
    try:
        result = openai.FineTuningJob.retrieve(job_id)
        print("Fine-Tuning 任務狀態：", result)
        return result
    except Exception as e:
        print("查詢 Fine-Tuning 任務狀態失敗：", e)
        return None

# 主程式範例
if __name__ == "__main__":
    # 替換為您的文件路徑
    file_path = r"C:\Users\BIN\Desktop\論文資料\data_trans\dataset_test\1\2\3\1000_VAL_processed_chat_format.jsonl"

    # 上傳文件
    uploaded_file = upload_file(file_path)
    
    # 列出文件清單
    file_list = list_files()
    
    # 替換為您的訓練與驗證文件 ID，以及模型名稱
    training_file_id = "file-XXXXXXXXXXXXXXXXXX"  # 替換為訓練文件 ID
    validation_file_id = "file-XXXXXXXXXXXXXXXXXXXX"  # 替換為驗證文件 ID
    model_name = "gpt-3.5-turbo-0125"  # 替換為模型名稱

    # 建立 Fine-Tuning 任務
    fine_tuning_job = create_fine_tuning_job(training_file_id, validation_file_id, model_name)
    
    # 替換為您的 Fine-Tuning Job ID
    fine_tuning_job_id = "ftjob-XXXXXXXXXXXX"  # 替換為 Fine-Tuning Job ID
    
    # 查詢任務狀態
    job_status = retrieve_fine_tuning_job(fine_tuning_job_id)
