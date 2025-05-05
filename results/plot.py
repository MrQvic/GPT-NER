import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_from_config(config_file, data_file='data.json', output_dir='graphs', format='pdf', dpi=300):
    """
    Univerzální funkce pro vytváření grafů na základě konfigurace v JSONu.
    
    Args:
        config_file: Cesta k souboru s konfigurací grafů
        data_file: Cesta k souboru s daty pro grafy
        output_dir: Adresář pro uložení výsledných grafů
        format: Formát výstupních souborů (png, pdf, svg...)
        dpi: Rozlišení obrázků
    """
    # Načtení konfigurace a dat
    with open(config_file, 'r') as f:
        plot_configs = json.load(f)
    
    with open(data_file, 'r') as f:
        data_sets = json.load(f)
    
    # Vytvoření adresáře pro výstupy, pokud neexistuje
    os.makedirs(output_dir, exist_ok=True)
    
    # Vytvoření grafů podle konfigurace
    for plot_id, plot_config in plot_configs.items():
        print(f"Creating plot: {plot_id}")
        
        # Získání dat pro graf
        dataset_name = plot_config.get('dataset')
        if dataset_name not in data_sets:
            print(f"Dataset '{dataset_name}' not found. Skipping plot '{plot_id}'.")
            continue
            
        # Převod na DataFrame
        df = create_dataframe(data_sets[dataset_name], plot_config.get('data_format', 'standard'))
        
        # Filtrování dat podle podmínek
        for filter_key, filter_value in plot_config.get('filters', {}).items():
            if isinstance(filter_value, list):
                df = df[df[filter_key].isin(filter_value)]
            else:
                df = df[df[filter_key] == filter_value]
        
        # Vytvoření grafu
        create_plot(df, plot_config, output_dir, format, dpi)
        
def create_dataframe(data, format_type='standard'):
    """Převede data z JSON na pandas DataFrame podle daného formátu."""
    if format_type == 'standard':
        rows = []
        for method in data:
            for verification in data[method]:
                for model in data[method][verification]:
                    for metric, score in data[method][verification][model].items():
                        rows.append({
                            'Method': method,
                            'Verification': verification,
                            'Model': model,
                            'Metric': metric,
                            'Score': score
                        })
        return pd.DataFrame(rows)
    elif format_type == 'annotators':
        pass
        # Specifický formát pro data s anotátory
        
    return pd.DataFrame()

def create_plot(df, config, output_dir, format, dpi):
    """Vytvoří a uloží graf podle dané konfigurace."""
    # Nastavení stylů
    plt.rcdefaults()
    plt.close('all')
    
    # Vytvoření figury
    fig_size = config.get('figure_size', (10, 8))
    fig, ax = plt.subplots(figsize=fig_size)
    sns.set_style(config.get('style', 'whitegrid'))
    
    # Vytvoření grafu podle typu
    plot_type = config.get('plot_type', 'barplot')
    
    if plot_type == 'barplot':
        # Parametry pro barplot
        x = config.get('x', 'Model')
        y = config.get('y', 'Score')
        hue = config.get('hue', 'Metric')
        palette = config.get('palette', {
            'Precision': '#2ecc71', 
            'Recall': '#e74c3c', 
            'F1': '#3498db'
        })
        
        # Vytvoření barplotu
        bars = sns.barplot(
            data=df,
            x=x, y=y, hue=hue,
            palette=palette,
            ax=ax,
            errorbar=None,
            edgecolor=config.get('edgecolor', 'lightgray'),
            linewidth=config.get('linewidth', 0.5)
        )
        
        # Přidání popisků na sloupce
        if config.get('show_bar_labels', True):
            for container in ax.containers:
                ax.bar_label(container, fmt=config.get('bar_label_format', '%.2f'), 
                             padding=config.get('bar_label_padding', 3))
    
    # Úpravy vzhledu grafu
    ax.set_title(config.get('title', ''))
    ax.set_ylim(config.get('ylim', (0, 100)))
    
    if config.get('show_grid', True):
        ax.grid(True, axis='y', linestyle=config.get('grid_linestyle', '--'), 
                alpha=config.get('grid_alpha', 0.3))
    
    ax.legend(title=config.get('legend_title', 'Metric'))
    ax.tick_params(axis='x', rotation=config.get('x_rotation', 0))
    
    plt.tight_layout()
    
    # Uložení grafu
    filename = config.get('filename', f"plot_{plot_type}")
    filepath = os.path.join(output_dir, f"{filename}.{format}")
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight', format=format)
    plt.close(fig)
    print(f"Saved plot to: {filepath}")


if __name__ == "__main__":
    plot_from_config(
        config_file="plots_config.json",
        data_file="data.json",
        output_dir="graphs",
        format="pdf"
    )