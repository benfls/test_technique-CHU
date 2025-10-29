import pandas as pd
import numpy as np
import os 

def load_data(file_path: str) -> pd.DataFrame:
    """Charger les données depuis le fichier tsv dans un dataframe pandas."""
    return pd.read_csv(file_path, sep="\t")

def select_pair_id(df: pd.DataFrame, id_column: str) -> pd.DataFrame:
    """Selectionner les lignes avec un id pair."""
    return df[df[id_column] % 2 == 0]

def main():
    # Charger les datasets
    actors_df = load_data('data/imdb_ijs_actors.tsv.gz')
    roles_df = load_data('data/imdb_ijs_roles.tsv.gz')

    # Selectionner les acteurs avec des ID pairs
    actors_pair_df = select_pair_id(actors_df, 'id')

    # Joindre les deux tables sur les colonnes id et actor_id
    df_merge = pd.merge(actors_pair_df, roles_df, left_on='id', right_on='actor_id', how='inner')
    
    # Compter le nombre de rôles par acteur et retourner les top 100
    df_count = (
        df_merge
        .groupby(['id', 'first_name', 'last_name'], as_index=False)
        .size()
        .rename(columns={'size': 'role_count'})
        .sort_values(by='role_count', ascending=False)
        .head(100)
    )

    # Sauvegarder le résultat dans un fichier json
    output_path = 'final_result.json'
    df_count.to_json(output_path, orient='records', force_ascii=False, indent=4)
    print(f"Résultat enregistré dans {os.path.abspath(output_path)}")
    
if __name__ == "__main__":
    main()