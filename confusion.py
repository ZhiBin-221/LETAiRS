import numpy as np

def calculate_metrics(confusion_matrix):

    total_samples = np.sum(confusion_matrix)

    correct_predictions = np.trace(confusion_matrix)

    accuracy = correct_predictions / total_samples

    precisions = []
    recalls = []
    f1_scores = []

    for i in range(len(confusion_matrix)):
        true_positive = confusion_matrix[i, i]
        predicted_positive = np.sum(confusion_matrix[:, i])
        actual_positive = np.sum(confusion_matrix[i, :])

        precision = true_positive / predicted_positive if predicted_positive > 0 else 0
        recall = true_positive / actual_positive if actual_positive > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        precisions.append(precision)
        recalls.append(recall)
        f1_scores.append(f1)


    precision_avg = np.mean(precisions)
    recall_avg = np.mean(recalls)
    f1_avg = np.mean(f1_scores)

    return {
        "Accuracy": accuracy * 100,  
        "Precision (avg)": precision_avg * 100,  
        "Recall (avg)": recall_avg * 100,  
        "F1 Score (avg)": f1_avg,
    }

def process_input_matrix(matrix_str):
   

    matrix = []
    for line in matrix_str.strip().split("\n"):
        row = [float(value.strip('%')) / 100 for value in line.replace(",", " ").split()]
        matrix.append(row)
    return np.array(matrix)

matrix_input = """
4.16%	0.74%	3.88%
0.83%	6.47%	7.12%
3.60%	4.25%	68.95%

"""

confusion_matrix = process_input_matrix(matrix_input)

metrics = calculate_metrics(confusion_matrix)


# for metric, value in metrics.items():
#     if metric == "F1 Score (avg)":
#         print(f"{metric}: {value:.4f}")
#     else:
#         print(f"{metric}: {value:.2f}%")

for key, value in metrics.items():
    if key == "F1 Score (avg)":
        print(f"{value:.4f}")
    else:
        print(f"{value:.2f}%")