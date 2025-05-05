import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the results as a nested dictionary for easier maintenance
CONLL_RESULTS = {
    'Random': {
        'without_verification': {
            'GPT-3 (Paper result)': {'Precision': 88.18, 'Recall': 78.54, 'F1': 83.08},
            'GPT-3.5': {'Precision': 51.83, 'Recall': 51.36, 'F1': 51.6},
            'Llama3.1-70b': {'Precision': 21.74, 'Recall': 29.55, 'F1': 25.05},
            'GPT-4o-mini': {'Precision': 60.98, 'Recall': 79.55, 'F1': 69.03},
            #'GPT-4': {'Precision': 61.51, 'Recall': 88.64, 'F1': 72.63},
            'Qwen2.5-72b': {'Precision': 60.3, 'Recall': 90.45, 'F1': 72.36},
	        #'Qwen2.5-14b': {'Precision': 28.89, 'Recall':5.91, 'F1': 9.81}
        },
        'with_verification': {
            'GPT-3 (Paper result)': {'Precision': 88.95, 'Recall': 79.73, 'F1': 84.34},
            'GPT-3.5': {'Precision': 58.55, 'Recall': 51.36, 'F1': 54.72}
        }
    },
    'Sentence': {
        'without_verification': {
            'GPT-3 (Paper result)': {'Precision': 90.47, 'Recall': 95.00, 'F1': 92.68},
            'GPT-3.5': {'Precision': 73.42, 'Recall': 79.09, 'F1': 76.15},
            'Llama3.1-70b': {'Precision': 29.59, 'Recall': 13.18, 'F1': 18.23},
            'GPT-4o-mini': {'Precision': 60.55, 'Recall': 79.55, 'F1': 68.76},
            'Qwen2.5-72b': {'Precision': 74.82, 'Recall': 94.54, 'F1': 83.53},
            #'Qwen2.5-14b': {'Precision': 51.22, 'Recall': 9.55, 'F1': 16.09}
        },
        'with_verification': {
            'GPT-3 (Paper result)': {'Precision': 91.77, 'Recall': 96.36, 'F1': 94.01},
            'GPT-3.5': {'Precision': 80.55, 'Recall': 79.09, 'F1': 79.82}
        }
    }
}

CNEC_RESULTS = {
    'Random': {
        'without_verification': {
            'robeczech-base': {'Precision': 92.72, 'Recall': 80.9, 'F1': 86.44},
            'Qwen2.5-72b-CNEC': {'Precision': 74.5, 'Recall': 62.6, 'F1': 68.1},
            'Qwen2.5-14b-CNEC': {'Precision': 76.83, 'Recall': 50, 'F1': 60.58},
            'Llama3.1-70b-CNEC': {'Precision': 93.33, 'Recall': 11.1, 'F1': 19.85},
            'Deepseek-r1:70b-CNEC': {'Precision': 84, 'Recall': 66.66, 'F1': 74.34},
        }
    }
}

HISTORICAL_RESULTS = {
    'Random': {
        '20-examples': {
            'robeczech': {'Precision': 71.42, 'Recall': 37.23, 'F1': 48.95},
            'Qwen2.5-72b': {'Precision': 56.25, 'Recall': 19.14, 'F1': 28.57},
            'Deepseek-r1:70b': {'Precision': 69.23, 'Recall': 9.57, 'F1': 16.82},
        },
        '154-examples': {
            'robeczech': {'Precision': 55.84, 'Recall': 68.34, 'F1': 61.46},
        }
    }
}

HISTORICAL_RESULTS_ANNOTATORS = {
    'Robeczech results by annotators': {
        '121-examples': {
            'Annotator 1': {'Precision': 65.36, 'Recall': 56.12, 'F1': 60.39},
            'Annotator 2': {'Precision': 61.45, 'Recall': 53.53, 'F1': 57.22},
            'Annotator 3': {'Precision': 68.16, 'Recall': 59.51, 'F1': 63.54}
        }
    }
}

plt.rcParams.update({
    'font.family': 'Arial',  # Or try: 'serif', 'sans-serif', 'monospace'
    'font.size': 16,
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'figure.titlesize': 18
})

def reset_plot_style():
    """Completely reset matplotlib state and set consistent style."""
    plt.close('all')  # Close all existing figures
    plt.rcdefaults()  # Reset to defaults
    plt.figure().clear()  # Clear any existing figure
    plt.close()  # Close it
    sns.set_style("whitegrid")  # Set the style consistently


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

def create_dataframe_from_annotator_results(results_dict):
    """Convert the nested annotator results dictionary into a pandas DataFrame."""
    rows = []
    
    for dataset in results_dict:
        for example_set in results_dict[dataset]:
            for annotator in results_dict[dataset][example_set]:
                for metric, score in results_dict[dataset][example_set][annotator].items():
                    rows.append({
                        'Dataset': dataset,
                        'Example_Set': example_set,
                        'Annotator': annotator,
                        'Metric': metric,
                        'Score': score
                    })
    
    return pd.DataFrame(rows)

def plot_verification_side_by_side(df, output_dir='graphs', format='png', dpi=300):
    """Create plots showing with/without verification results side by side."""
    reset_plot_style()
    
    # Get models that appear in both verification conditions for fair comparison
    with_verification_models = set(df[df['Verification'] == 'with_verification']['Model'].unique())
    without_verification_models = set(df[df['Verification'] == 'without_verification']['Model'].unique())
    common_models = list(with_verification_models & without_verification_models)
    
    # Filter to include only the common models
    filtered_df = df[df['Model'].isin(common_models)].copy()
    
    # Add verification status to model names
    filtered_df.loc[filtered_df['Verification'] == 'with_verification', 'Model'] = \
        filtered_df.loc[filtered_df['Verification'] == 'with_verification', 'Model'] + ' (With Ver.)'
    filtered_df.loc[filtered_df['Verification'] == 'without_verification', 'Model'] = \
        filtered_df.loc[filtered_df['Verification'] == 'without_verification', 'Model'] + ' (No Ver.)'
    
    # Create a single plot for each method
    for method in ['Random', 'Sentence']:
        method_data = filtered_df[filtered_df['Method'] == method]
        
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.set_style("whitegrid")
        
        # Create barplot with all the data
        bars = sns.barplot(
            data=method_data,
            x='Model', y='Score', hue='Metric',
            palette={'Precision': '#2ecc71', 'Recall': '#e74c3c', 'F1': '#3498db'},
            ax=ax,
            errorbar=None,
            edgecolor='lightgray',
            linewidth=0.5
        )
        
        # Add value labels on top of each bar
        for container in ax.containers:
            ax.bar_label(container, fmt='%.2f', padding=3)
        
        ax.set_title(f'Impact of Self-Verification on {method} Retrieval')
        ax.set_ylim(0, 105)
        ax.grid(True, axis='y', linestyle='--', alpha=0.3)
        ax.legend(title='Metric')
        ax.tick_params(axis='x')
        
        plt.tight_layout()
        
        # Save to file
        filename = f'verification_impact_{method.lower()}.{format}'
        filepath = os.path.join(output_dir, filename)
        fig.savefig(filepath, dpi=dpi, bbox_inches='tight', format=format)
        plt.close(fig)
        print(f"Saved verification impact plot to: {filepath}")


def plot_conll_comparison(df, output_dir='graphs', format='png', dpi=300):
    """Create focused comparison plots between Paper (GPT-3) and GPT-3.5 results."""
    plt.rcdefaults()
    # Filter data to include only GPT-3 (Paper) and GPT-3.5
    target_models = ['GPT-3 (Paper result)', 'GPT-3.5']
    filtered_df = df[df['Model'].isin(target_models)]
    
    for verification_status in ['without_verification', 'with_verification']:
        title_suffix = "With Self-Verification" if verification_status == "with_verification" else "Without Self-Verification"
        
        for method in ['Random', 'Sentence']:
            # Skip if no data available for this combination
            data = filtered_df[(filtered_df['Method'] == method) & (filtered_df['Verification'] == verification_status)]
            if data.empty:
                continue
                
            # Create figure
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.set_style("whitegrid")
            
            # Create bar plot
            bars = sns.barplot(
                data=data,
                x='Model', y='Score', hue='Metric',
                palette={'Precision': '#2ecc71', 'Recall': '#e74c3c', 'F1': '#3498db'},
                ax=ax,
                errorbar=None,
                edgecolor='lightgray',
                linewidth=0.5
            )
            
            # Add value labels on top of each bar
            for container in ax.containers:
                ax.bar_label(container, fmt='%.2f', padding=3)
            
            ax.set_title(f'GPT-3 vs GPT-3.5: {method} Retrieval - {title_suffix}')
            ax.set_ylim(0, 105)  # Increased to make room for labels
            ax.grid(True, axis='y', linestyle='--', alpha=0.3)
            ax.legend(title='Metric')
            ax.tick_params(axis='x', rotation=0)
        
            plt.tight_layout()
            
            # Save to file
            filename = f'conll_comparison_{method.lower()}_{verification_status.replace("_", "-")}.{format}'
            filepath = os.path.join(output_dir, filename)
            fig.savefig(filepath, dpi=dpi, bbox_inches='tight', format=format)
            plt.close(fig)
            print(f"Saved comparison plot to: {filepath}")

def plot_conll_results(df, output_dir='graphs', format='png', dpi=300):
    """Create and save plots for CoNLL results, with each method in a separate file."""
    reset_plot_style()
    for verification_status in ['without_verification', 'with_verification']:
        title_suffix = "With Self-Verification" if verification_status == "with_verification" else "Without Self-Verification"
        
        for method in ['Random', 'Sentence']:
            # Create a separate figure for each method
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.set_style("whitegrid")
            
            data = df[(df['Method'] == method) & (df['Verification'] == verification_status)]
            
            # Create barplot
            bars = sns.barplot(
                data=data,
                x='Model', y='Score', hue='Metric',
                palette={'Precision': '#2ecc71', 'Recall': '#e74c3c', 'F1': '#3498db'},
                ax=ax,
                errorbar=None
            )
            
            # Manually set all bar edge colors and widths
            for patch in ax.patches:
                patch.set_edgecolor('lightgray')
                patch.set_linewidth(0.5)
            
            # Add value labels on top of each bar
            for container in ax.containers:
                ax.bar_label(container, fmt='%.2f', padding=3)
            
            ax.set_title(f'{method} Retrieval - {title_suffix}')
            ax.set_ylim(0, 100)
            ax.grid(True, axis='y', linestyle='--', alpha=0.3)
            ax.legend(title='Metric')
            ax.tick_params(axis='x', rotation=0)
        
            plt.tight_layout()
            
            # Save each method to a separate file
            filename = f'conll_metrics_{method.lower()}_{verification_status.replace("_", "-")}.{format}'
            filepath = os.path.join(output_dir, filename)
            fig.savefig(filepath, dpi=dpi, bbox_inches='tight', format=format)
            plt.close(fig)
            print(f"Saved plot to: {filepath}")

def plot_cnec_results(df, output_dir='graphs', format='png', dpi=300):
    """Create and save plots for CNEC results."""
    plt.rcdefaults()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.set_style("whitegrid")
    
    data = df[df['Method'] == 'Random']
    
    sns.barplot(
        data=data,
        x='Model', y='Score', hue='Metric',
        palette={'Precision': '#2ecc71', 'Recall': '#e74c3c', 'F1': '#3498db'},
        ax=ax,
        errorbar=None,
        edgecolor='lightgray', 
        linewidth=0.5  
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

def plot_historical_results(df, output_dir='graphs', format='png', dpi=300):
    """Create and save plots for Historical results."""
    # Get unique example sets (e.g., '20-examples', '154-examples')
    example_sets = df['Verification'].unique()
    
    fig, axes = plt.subplots(1, len(example_sets), figsize=(15, 8))
    # Handle the case when there's only one example set
    if len(example_sets) == 1:
        axes = [axes]
    
    sns.set_style("whitegrid")
    
    for idx, example_set in enumerate(example_sets):
        data = df[df['Verification'] == example_set]
        
        sns.barplot(
            data=data,
            x='Model', y='Score', hue='Metric',
            palette={'Precision': '#2ecc71', 'Recall': '#e74c3c', 'F1': '#3498db'},
            ax=axes[idx],
            errorbar=None
        )
        
        axes[idx].set_title(f'Historical Data - {example_set}')
        axes[idx].set_ylim(0, 100)
        axes[idx].grid(True, axis='y', linestyle='--', alpha=0.3)
        axes[idx].legend(title='Metric')
        axes[idx].tick_params(axis='x', rotation=45)
    
    plt.suptitle(f'Historical NER Performance Metrics', y=1.02, fontsize=16)
    plt.tight_layout()
    
    filename = f'historical_metrics.{format}'
    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight', format=format)
    plt.close(fig)
    print(f"Saved plot to: {filepath}")

def plot_historical_annotator_results(df, output_dir='graphs', format='png', dpi=300):
    """Create and save plots for Historical results by annotators."""
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.set_style("whitegrid")
    
    # Create the bar plot
    bars = sns.barplot(
        data=df,
        x='Annotator', y='Score', hue='Metric',
        palette={'Precision': '#2ecc71', 'Recall': '#e74c3c', 'F1': '#3498db'},
        ax=ax,
        errorbar=None
    )
    
    # Add value labels on top of each bar
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', padding=3)
    
    # Get example count from first row
    example_set = df['Example_Set'].iloc[0]
    
    ax.set_title(f'Historical NER Results by Annotators ({example_set})')
    ax.set_ylim(0, 105)  # Increased to make room for labels
    ax.grid(True, axis='y', linestyle='--', alpha=0.3)
    ax.legend(title='Metric')
    ax.tick_params(axis='x', rotation=0)
    
    plt.tight_layout()
    
    filename = f'historical_annotator_metrics.{format}'
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
df_historical = create_dataframe_from_results(HISTORICAL_RESULTS)
df_historical_annotators = create_dataframe_from_annotator_results(HISTORICAL_RESULTS_ANNOTATORS)


# Save plots and CSV
plot_conll_results(df_conll, format='pdf')
plot_cnec_results(df_cnec, format='pdf')
plot_historical_results(df_historical, format='pdf')
plot_historical_annotator_results(df_historical_annotators, format='pdf')
plot_conll_comparison(df_conll, format='pdf')
plot_verification_side_by_side(df_conll, format='pdf')

export_results_to_csv(df_conll)
export_results_to_csv(df_cnec, 'graphs/cnec_results.csv')
export_results_to_csv(df_historical_annotators, 'graphs/historical_annotator_results.csv')
#export_results_to_csv(df_historical, 'graphs/historical