import os
import hashlib
import argparse
from collections import defaultdict


def calculate_file_hash(filepath):
    hash_md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def find_duplicate_files(directory_path, extensions=None):
    """
    Najde duplicitní soubory v zadaném adresáři.
    
    Args:
        directory_path: Cesta k adresáři, který se má prohledat
        extensions: Seznam přípon souborů, které se mají prohledat (např. ['.txt', '.md'])
                    Pokud je None, prohledají se všechny soubory
    
    Returns:
        Dictionary, kde klíče jsou hashe obsahu a hodnoty jsou seznamy cest k souborům
        se stejným obsahem
    """
    # Defaultdict nám automaticky vytvoří prázdný seznam pro nový klíč
    files_by_hash = defaultdict(list)
    
    # Projdeme všechny soubory v adresáři a jeho podadresářích
    for root, _, files in os.walk(directory_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            
            # Pokud jsou zadány přípony, kontrolujeme, zda soubor má jednu z nich
            if extensions and not any(filename.endswith(ext) for ext in extensions):
                continue
                
            # Přeskočíme, pokud nemůžeme přečíst soubor
            try:
                file_hash = calculate_file_hash(filepath)
                files_by_hash[file_hash].append(filepath)
            except (IOError, PermissionError):
                print(f"Varování: Nelze přečíst soubor {filepath}")
    
    # Vrátíme pouze soubory, které mají alespoň jednu kopii
    return {file_hash: file_paths for file_hash, file_paths in files_by_hash.items() 
            if len(file_paths) > 1}


def main():
    parser = argparse.ArgumentParser(description='Najde duplicitní textové soubory v adresáři.')
    parser.add_argument('directory', help='Adresář, který se má prohledat')
    parser.add_argument('--ext', nargs='+', help='Přípony souborů, které se mají prohledat (např. .txt .md)')
    args = parser.parse_args()
    
    extensions = args.ext if args.ext else None
    
    print(f"Hledání duplicitních souborů v adresáři: {args.directory}")
    if extensions:
        print(f"Hledají se pouze soubory s příponami: {', '.join(extensions)}")
    
    duplicates = find_duplicate_files(args.directory, extensions)
    
    if not duplicates:
        print("\nŽádné duplicitní soubory nebyly nalezeny.")
        return
    
    # Vypíšeme výsledky
    print("\nNalezeny následující duplicitní soubory:")
    for file_hash, file_paths in duplicates.items():
        print(f"\nSkupina duplicitních souborů (hash: {file_hash}):")
        for filepath in file_paths:
            print(f"  - {filepath}")
    
    # Vypíšeme statistiku
    total_duplicates = sum(len(file_paths) - 1 for file_paths in duplicates.values())
    print(f"\nCelkem nalezeno {total_duplicates} duplicitních souborů v {len(duplicates)} skupinách.")


if __name__ == "__main__":
    main()