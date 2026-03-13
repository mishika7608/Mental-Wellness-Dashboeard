"""
Visualization Utilities
Contains functions for creating various plots and charts
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def plot_class_distribution(y, title="Class Distribution"):
    """
    Plot distribution of target classes
    
    Args:
        y: Target variable
        title: Plot title
    """
    fig, ax = plt.subplots(1, 2, figsize=(14, 5))
    
    # Count plot
    value_counts = pd.Series(y).value_counts()
    ax[0].bar(value_counts.index, value_counts.values, color=['#2ecc71', '#e74c3c'])
    ax[0].set_xlabel('Class')
    ax[0].set_ylabel('Count')
    ax[0].set_title(f'{title} - Counts')
    ax[0].set_xticks([0, 1])
    ax[0].set_xticklabels(['No Depression', 'Depression'])
    
    # Add value labels on bars
    for i, v in enumerate(value_counts.values):
        ax[0].text(i, v + 50, str(v), ha='center', fontweight='bold')
    
    # Pie chart
    colors = ['#2ecc71', '#e74c3c']
    ax[1].pie(value_counts.values, labels=['No Depression', 'Depression'], 
              autopct='%1.1f%%', colors=colors, startangle=90)
    ax[1].set_title(f'{title} - Percentage')
    
    plt.tight_layout()
    return fig


def plot_feature_distributions(df, features, target='Depression', ncols=3):
    """
    Plot distributions of multiple features
    
    Args:
        df: Input DataFrame
        features: List of feature names
        target: Target column name
        ncols: Number of columns in subplot grid
    """
    nrows = (len(features) + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(5*ncols, 4*nrows))
    axes = axes.flatten() if len(features) > 1 else [axes]
    
    for idx, feature in enumerate(features):
        if df[feature].dtype in ['int64', 'float64']:
            # Numerical feature - histogram
            for label in df[target].unique():
                subset = df[df[target] == label]
                axes[idx].hist(subset[feature], alpha=0.6, 
                             label=f'Class {label}', bins=20)
        else:
            # Categorical feature - count plot
            pd.crosstab(df[feature], df[target]).plot(
                kind='bar', ax=axes[idx], color=['#2ecc71', '#e74c3c']
            )
        
        axes[idx].set_title(f'{feature} Distribution')
        axes[idx].legend()
        axes[idx].grid(True, alpha=0.3)
    
    # Hide empty subplots
    for idx in range(len(features), len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    return fig


def plot_correlation_matrix(df, figsize=(12, 10)):
    """
    Plot correlation matrix heatmap
    
    Args:
        df: Input DataFrame
        figsize: Figure size
    """
    # Calculate correlation matrix
    corr = df.corr()
    
    # Create mask for upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    # Plot
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', 
                cmap='RdYlGn_r', center=0, square=True,
                linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
    ax.set_title('Feature Correlation Matrix', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    return fig


def plot_confusion_matrix(cm, classes=['No Depression', 'Depression']):
    """
    Plot confusion matrix
    
    Args:
        cm: Confusion matrix array
        classes: Class labels
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=classes, yticklabels=classes,
                cbar_kws={'label': 'Count'}, ax=ax)
    
    ax.set_ylabel('True Label', fontsize=12)
    ax.set_xlabel('Predicted Label', fontsize=12)
    ax.set_title('Confusion Matrix', fontsize=14, fontweight='bold')
    
    # Add accuracy information
    accuracy = (cm[0, 0] + cm[1, 1]) / cm.sum()
    plt.text(0.5, -0.15, f'Overall Accuracy: {accuracy:.2%}',
             ha='center', transform=ax.transAxes, fontsize=12)
    
    plt.tight_layout()
    return fig


def plot_roc_curve(fpr, tpr, auc_score):
    """
    Plot ROC curve
    
    Args:
        fpr: False positive rate
        tpr: True positive rate
        auc_score: Area under curve score
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    ax.plot(fpr, tpr, color='#e74c3c', lw=2, 
            label=f'ROC Curve (AUC = {auc_score:.3f})')
    ax.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--', 
            label='Random Classifier')
    
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate', fontsize=12)
    ax.set_ylabel('True Positive Rate (Recall)', fontsize=12)
    ax.set_title('Receiver Operating Characteristic (ROC) Curve', 
                 fontsize=14, fontweight='bold')
    ax.legend(loc="lower right", fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_feature_importance(importance_df, top_n=15, title='Feature Importance'):
    """
    Plot feature importance
    
    Args:
        importance_df: DataFrame with 'feature' and 'importance' columns
        top_n: Number of top features to show
        title: Plot title
    """
    # Get top N features
    top_features = importance_df.nlargest(top_n, 'importance')
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 8))
    
    colors = plt.cm.RdYlGn_r(top_features['importance'] / top_features['importance'].max())
    
    ax.barh(range(len(top_features)), top_features['importance'], color=colors)
    ax.set_yticks(range(len(top_features)))
    ax.set_yticklabels(top_features['feature'])
    ax.set_xlabel('Importance Score', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    
    # Add value labels
    for i, v in enumerate(top_features['importance']):
        ax.text(v + 0.001, i, f'{v:.4f}', va='center', fontsize=10)
    
    plt.tight_layout()
    return fig


def plot_learning_curves(train_sizes, train_scores, val_scores):
    """
    Plot learning curves
    
    Args:
        train_sizes: Array of training set sizes
        train_scores: Training scores
        val_scores: Validation scores
    """
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    val_mean = np.mean(val_scores, axis=1)
    val_std = np.std(val_scores, axis=1)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(train_sizes, train_mean, label='Training Score', 
            color='#3498db', marker='o')
    ax.fill_between(train_sizes, train_mean - train_std, 
                     train_mean + train_std, alpha=0.2, color='#3498db')
    
    ax.plot(train_sizes, val_mean, label='Validation Score', 
            color='#e74c3c', marker='o')
    ax.fill_between(train_sizes, val_mean - val_std, 
                     val_mean + val_std, alpha=0.2, color='#e74c3c')
    
    ax.set_xlabel('Training Set Size', fontsize=12)
    ax.set_ylabel('Score', fontsize=12)
    ax.set_title('Learning Curves', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def create_interactive_feature_importance(importance_df, top_n=15):
    """
    Create interactive Plotly feature importance chart
    
    Args:
        importance_df: DataFrame with 'feature' and 'importance' columns
        top_n: Number of top features to show
    """
    top_features = importance_df.nlargest(top_n, 'importance').sort_values('importance')
    
    fig = go.Figure(go.Bar(
        x=top_features['importance'],
        y=top_features['feature'],
        orientation='h',
        marker=dict(
            color=top_features['importance'],
            colorscale='Reds',
            showscale=True,
            colorbar=dict(title="Importance")
        ),
        text=top_features['importance'].round(4),
        textposition='auto',
    ))
    
    fig.update_layout(
        title=f'Top {top_n} Feature Importances',
        xaxis_title='Importance Score',
        yaxis_title='Feature',
        height=600,
        template='plotly_white',
        font=dict(size=12)
    )
    
    return fig


def create_interactive_correlation_heatmap(df):
    """
    Create interactive correlation heatmap using Plotly
    
    Args:
        df: Input DataFrame
    """
    corr = df.corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title='Feature Correlation Heatmap',
        xaxis_title='Features',
        yaxis_title='Features',
        height=800,
        width=900,
        template='plotly_white'
    )
    
    return fig


def plot_model_comparison(results_df):
    """
    Plot comparison of multiple models
    
    Args:
        results_df: DataFrame with columns ['Model', 'Accuracy', 'Recall', 'Precision', 'F1']
    """
    metrics = ['Accuracy', 'Recall', 'Precision', 'F1']
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, metric in enumerate(metrics):
        ax = axes[idx]
        results_df.plot(x='Model', y=metric, kind='bar', ax=ax, 
                       color='#3498db', legend=False)
        ax.set_title(f'{metric} Comparison', fontsize=12, fontweight='bold')
        ax.set_ylabel(metric, fontsize=11)
        ax.set_xlabel('Model', fontsize=11)
        ax.set_ylim([0, 1])
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for i, v in enumerate(results_df[metric]):
            ax.text(i, v + 0.02, f'{v:.3f}', ha='center', fontweight='bold')
    
    plt.tight_layout()
    return fig


def create_dashboard_summary(model_metrics, feature_importance_df):
    """
    Create comprehensive dashboard summary with subplots
    
    Args:
        model_metrics: Dictionary with metrics
        feature_importance_df: DataFrame with feature importances
    """
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Model Performance Metrics', 'Feature Importance',
                       'Precision-Recall Trade-off', 'Class Distribution'),
        specs=[[{'type': 'bar'}, {'type': 'bar'}],
               [{'type': 'scatter'}, {'type': 'pie'}]]
    )
    
    # Metrics bar chart
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1']
    values = [model_metrics.get(m, 0) for m in metrics]
    
    fig.add_trace(
        go.Bar(x=metrics, y=values, marker_color='#3498db', 
               text=[f'{v:.3f}' for v in values], textposition='auto'),
        row=1, col=1
    )
    
    # Feature importance
    top_5 = feature_importance_df.nlargest(5, 'importance')
    fig.add_trace(
        go.Bar(x=top_5['importance'], y=top_5['feature'], 
               orientation='h', marker_color='#e74c3c'),
        row=1, col=2
    )
    
    # Precision-Recall (example - would need actual data)
    recall_range = np.linspace(0, 1, 100)
    precision_range = 1 - (recall_range * 0.3)  # Example curve
    
    fig.add_trace(
        go.Scatter(x=recall_range, y=precision_range, 
                  mode='lines', line=dict(color='#9b59b6', width=2)),
        row=2, col=1
    )
    
    # Class distribution pie
    if 'class_distribution' in model_metrics:
        dist = model_metrics['class_distribution']
        fig.add_trace(
            go.Pie(labels=list(dist.keys()), values=list(dist.values()),
                  marker=dict(colors=['#2ecc71', '#e74c3c'])),
            row=2, col=2
        )
    
    fig.update_layout(height=800, showlegend=False, 
                     title_text="Model Performance Dashboard")
    
    return fig


def save_plot(fig, filename, dpi=300):
    """
    Save matplotlib figure to file
    
    Args:
        fig: Matplotlib figure
        filename: Output filename
        dpi: Dots per inch
    """
    fig.savefig(filename, dpi=dpi, bbox_inches='tight')
    print(f"Plot saved to {filename}")


if __name__ == "__main__":
    print("Visualization Utilities Module")
    print("Import this module to create various plots and charts")