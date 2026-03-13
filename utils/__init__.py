"""
Utils Package
Provides preprocessing and visualization utilities
"""

from .preprocessing import (
    DataPreprocessor,
    validate_data_quality,
    split_features_target,
    get_feature_info
)

from .visualization import (
    plot_class_distribution,
    plot_feature_distributions,
    plot_correlation_matrix,
    plot_confusion_matrix,
    plot_roc_curve,
    plot_feature_importance,
    create_interactive_feature_importance,
    create_interactive_correlation_heatmap,
    plot_model_comparison
)

__all__ = [
    # Preprocessing
    'DataPreprocessor',
    'validate_data_quality',
    'split_features_target',
    'get_feature_info',
    
    # Visualization
    'plot_class_distribution',
    'plot_feature_distributions',
    'plot_correlation_matrix',
    'plot_confusion_matrix',
    'plot_roc_curve',
    'plot_feature_importance',
    'create_interactive_feature_importance',
    'create_interactive_correlation_heatmap',
    'plot_model_comparison'
]

__version__ = '1.0.0'
__author__ = 'Divyanshi Sahu, Deeksha Singh, Chhavi Agrahari, Mishika Kulshrestha'