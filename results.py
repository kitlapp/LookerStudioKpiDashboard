import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, balanced_accuracy_score, matthews_corrcoef,
)


def get_classification_metrics(y_test, y_pred, conf_matrix_title=None, runtime=None):
    df = pd.DataFrame(data=[
        round(accuracy_score(y_true=y_test, y_pred=y_pred), 4),
        round(balanced_accuracy_score(y_true=y_test, y_pred=y_pred), 4),
        round(recall_score(y_true=y_test, y_pred=y_pred), 4),
        round(precision_score(y_true=y_test, y_pred=y_pred), 4),
        round(f1_score(y_true=y_test, y_pred=y_pred), 4),
        round(matthews_corrcoef(y_true=y_test, y_pred=y_pred), 4),
        round(runtime, 2)
    ],
                 index=[
        'Accuracy', 'Balanced Accuracy', 'Recall', 'Precision', 'F1 Score', 'Φ Coefficient (MCC)', 'Runtime (Minutes)'],
                 columns=['Value'])
    df.index.name = 'Metric'
    # Confusion Matrix Visualization
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        confusion_matrix(y_test, y_pred),
        annot=True,
        fmt='d',
        cmap='Blues',
        xticklabels=['Negative', 'Positive'],
        yticklabels=['Negative', 'Positive'])
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title(conf_matrix_title)
    plt.show()
    return df


def random_forest_interpretation(X_train_scaled, model):
    weight_array = model.feature_importances_
    weight_df = pd.DataFrame({'Feature': X_train_scaled.columns, 'Importance': weight_array})
    weight_df_sorted = weight_df.sort_values(by='Importance', ascending=False)
    return weight_df_sorted


def logreg_interpretation(X_train_scaled, model):
    # Access the coefficients of log odds
    weight_array = model.coef_.flatten()
    # Convert log-odds to odds ratio
    odds_ratios = np.exp(weight_array)
    # Normalize odds ratios as a proportion of the total odds
    normalized_odds_sum_to_1 = odds_ratios / odds_ratios.sum()
    # Normalize odds relative to the maximum
    normalized_odds_max = odds_ratios / odds_ratios.max()
    # Calculate the interception
    weight_df = pd.DataFrame({'Feature': X_train_scaled.columns,
                              'Odds Ratio': odds_ratios,  # Absolute value for ranking
                              'Normalized Odds - Proportionality to the Total Odds': normalized_odds_sum_to_1,
                              'Normalized Odds - Relation to the Maximum': normalized_odds_max})
    weight_df_sorted = weight_df.sort_values(by='Odds Ratio', ascending=False)
    return weight_df_sorted
