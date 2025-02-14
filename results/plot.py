import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the results as a nested dictionary for easier maintenance
CONLL_RESULTS = {
    'Random': {
        'without_verification': {
            'GPT-3 (Paper result)': {'Precision': 88.18, 'Recall': 78.54, 'F1': 83.08},
            'GPT3.5': {'Precision': 51.83, 'Recall': 51.36, 'F1': 51.6},
            'Llama3.1-70b': {'Precision': 21.74, 'Recall': 29.55, 'F1': 25.05},
            'GPT-4o-mini': {'Precision': 60.98, 'Recall': 79.55, 'F1': 69.03},
            #'GPT-4': {'Precision': 61.51, 'Recall': 88.64, 'F1': 72.63},
            'Qwen2.5-72b': {'Precision': 60.3, 'Recall': 90.45, 'F1': 72.36},
	        #'Qwen2.5-14b': {'Precision': 28.89, 'Recall':5.91, 'F1': 9.81}
        },
        'with_verification': {
            'GPT-3': {'Precision': 88.95, 'Recall': 79.73, 'F1': 84.34},
            'GPT3.5': {'Precision': 58.55, 'Recall': 51.36, 'F1': 54.72}
        }
    },
    'Sentence': {
        'without_verification': {
            'GPT-3 (Paper result)': {'Precision': 90.47, 'Recall': 95.00, 'F1': 92.68},
            'GPT3.5': {'Precision': 73.42, 'Recall': 79.09, 'F1': 76.15},
            'Llama3.1-70b': {'Precision': 29.59, 'Recall': 13.18, 'F1': 18.23},
            'GPT-4o-mini': {'Precision': 60.55, 'Recall': 79.55, 'F1': 68.76},
            'Qwen2.5-72b': {'Precision': 74.82, 'Recall': 94.54, 'F1': 83.53},
            #'Qwen2.5-14b': {'Precision': 51.22, 'Recall': 9.55, 'F1': 16.09}
        },
        'with_verification': {
            'GPT-3': {'Precision': 91.77, 'Recall': 96.36, 'F1': 94.01},
            'GPT3.5': {'Precision': 80.55, 'Recall': 79.09, 'F1': 79.82}
        }
    }
}

CNEC_RESULTS = {
    'Random': {
        'without_verification': {
            'Qwen2.5-72b-CNEC': {'Precision': 74.5, 'Recall': 62.6, 'F1': 68.1},
            'Qwen2.5-14b-CNEC': {'Precision': 76.83, 'Recall': 50, 'F1': 60.58},
            'Llama3.1-70b-CNEC': {'Precision': 93.33, 'Recall': 11.1, 'F1': 19.85},
            'Deepseek-r1:70b-CNEC': {'Precision': 84, 'Recall': 66.66, 'F1': 74.34},
        }
    }
}


def create_dataframe_from_results(results_dict):
    """Convert the nested results dictionary into a pandas DataFrame."""
    rows = []
    
    for method in results_dict:
        for verification_type in results_dict[method]:
            for model in results_dict[method][verification_type]:
                for metric, score in results_dict[method][verification_type][model].items():
                    rows.append({
                        'Method': method,
                        'Verification': verification_type,
                        'Model': model,
                        'Metric': metric,
                        'Score': score
                    })
    
    return pd.DataFrame(rows)

def plot_conll_results(df, output_dir='graphs', format='png', dpi=300):
    """Create and save plots for CoNLL results."""
    for verification_status in ['without_verification', 'with_verification']:
        fig, axes = plt.subplots(1, 2, figsize=(20, 8))
        sns.set_style("whitegrid")
        
        title_suffix = "With Self-Verification" if verification_status == "with_verification" else "Without Self-Verification"
        
        for idx, method in enumerate(['Random', 'Sentence']):
            data = df[(df['Method'] == method) & (df['Verification'] == verification_status)]
            
            sns.barplot(
                data=data,
                x='Model', y='Score', hue='Metric',
                palette={'Precision': '#2ecc71', 'Recall': '#e74c3c', 'F1': '#3498db'},
                ax=axes[idx],
                errorbar=None
            )
            
            axes[idx].set_title(f'{method} Retrieval - {title_suffix}')
            axes[idx].set_ylim(0, 100)
            axes[idx].grid(True, axis='y', linestyle='--', alpha=0.3)
            axes[idx].legend(title='Metric')
            axes[idx].tick_params(axis='x', rotation=0)
        
        plt.suptitle(f'CoNLL NER Performance Metrics {title_suffix}', y=1.02, fontsize=16)
        plt.tight_layout()
        
        filename = f'conll_metrics_{verification_status.replace("_", "-")}.{format}'
        filepath = os.path.join(output_dir, filename)
        fig.savefig(filepath, dpi=dpi, bbox_inches='tight', format=format)
        plt.close(fig)
        print(f"Saved plot to: {filepath}")

def plot_cnec_results(df, output_dir='graphs', format='png', dpi=300):
    """Create and save plots for CNEC results."""
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.set_style("whitegrid")
    
    data = df[df['Method'] == 'Random']
    
    sns.barplot(
        data=data,
        x='Model', y='Score', hue='Metric',
        palette={'Precision': '#2ecc71', 'Recall': '#e74c3c', 'F1': '#3498db'},
        ax=ax,
        errorbar=None
    )
    
    ax.set_title('CNEC Dataset - Random Retrieval')
    ax.set_ylim(0, 100)
    ax.grid(True, axis='y', linestyle='--', alpha=0.3)
    ax.legend(title='Metric')
    ax.tick_params(axis='x', rotation=0)
    
    plt.tight_layout()
    
    filename = f'cnec_metrics.{format}'
    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight', format=format)
    plt.close(fig)
    print(f"Saved plot to: {filepath}")

def export_results_to_csv(df, output_dir='graphs'):
    """Export results to CSV file."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, 'ner_results.csv')
    df.to_csv(filepath, index=False)
    print(f"Saved results to: {filepath}")

# Create DataFrames and plot
df_conll = create_dataframe_from_results(CONLL_RESULTS)
df_cnec = create_dataframe_from_results(CNEC_RESULTS)

# Save plots and CSV
plot_conll_results(df_conll, format='png')
plot_cnec_results(df_cnec, format='png')
export_results_to_csv(df_conll)
export_results_to_csv(df_cnec, 'graphs/cnec_results.csv')

# Example of how to add a new model and regenerate plots:
"""
# Add new model results
RESULTS['Random']['without_verification']['NewModel'] = {
    'Precision': 85.5,
    'Recall': 82.3,
    'F1': 83.9
}

# Recreate and save visualizations with new data
df = create_dataframe_from_results(RESULTS)
plot_and_save_results(df)
export_results_to_csv(df)
"""