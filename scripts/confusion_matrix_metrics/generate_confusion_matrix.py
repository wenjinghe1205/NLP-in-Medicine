import pandas as pd
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

# Example of CLI: python3 generate_confusion_matrix.py flant5_base_enriched
# Output: .PNG file of confusion matrix and .CSV file with performance metrics

def compare_section_headers(file_name):
    # Read the CSV file
    data = pd.read_csv(file_name)
    
    # Extract 'section_header' and 'predictions' columns
    true_labels = data['section_header']
    predictions = data['predictions']
    
    # Generate the confusion matrix
    labels = sorted(true_labels.unique())
    conf_matrix = confusion_matrix(true_labels, predictions, labels=labels)
    
    # Plot the confusion matrix
    plt.figure(figsize=(14, 12))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    
    # Format the title to include only the model name, excluding "predictions" and ".csv"
    model_name = file_name.replace('_predictions.csv', '')
    plt.title(f'Confusion Matrix for {model_name}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.xticks(rotation=90, fontsize=10)
    plt.yticks(rotation=0, fontsize=10)
    plt.tight_layout()
    
    # Save the confusion matrix using the model name
    plt.savefig(f'{model_name}_confusion_matrix.png', bbox_inches='tight', dpi=300)
    plt.close()

    # Calculate metrics
    metrics_list = []
    for i, label in enumerate(labels):
        TP = conf_matrix[i, i]
        FP = conf_matrix[:, i].sum() - TP
        FN = conf_matrix[i, :].sum() - TP
        TN = conf_matrix.sum() - (TP + FP + FN)
        Precision = TP / (TP + FP) if (TP + FP) > 0 else 0
        Recall = TP / (TP + FN) if (TP + FN) > 0 else 0
        metrics_list.append([label, TP, FP, FN, TN, Precision, Recall])
    
    # Convert to DataFrame and save
    metrics_df = pd.DataFrame(metrics_list, columns=['Label', 'TP', 'FP', 'FN', 'TN', 'Precision', 'Recall'])
    metrics_csv_path = f'{model_name}_performance_metrics.csv'
    metrics_df.to_csv(metrics_csv_path, index=False)
    
    return metrics_df, metrics_csv_path

def main():
    # List of available models
    models = [
        "flant5_base_enriched",
        "flant5_base",
        "flant5_small_enriched",
        "flant5_small"
    ]

    # Create argument parser
    parser = argparse.ArgumentParser(description="Generate confusion matrix and metrics for model predictions.")
    parser.add_argument("model_name", choices=models, help="Pick from the available models: " + ", ".join(models))
    args = parser.parse_args()

    file_name = args.model_name + '_predictions.csv'  # Construct the file name based on the input model name
    metrics_df, metrics_csv_path = compare_section_headers(file_name)
    print(metrics_df)

if __name__ == "__main__":
    main()
