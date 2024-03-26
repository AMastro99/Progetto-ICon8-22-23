import pandas as pd
import os

dataset_cluster_path: str = "../dataset/datasetForClustering.csv"
dataset_path: str = "../dataset/dataset.csv"

def preprocessing():
    # colonne da eliminare
    colonne_da_eliminare = ["matricola", "nome", "cognome", "data di nascita", "sesso", "numero di cellulare",
                            "residenza", "titolo", "limitazioni lavorative", "reparto", "specializzazione",
                            "stipendio base", "incremento anzianita", "bonus incarico"]

    df = pd.read_csv(dataset_path)

    # crea il nuovo file senza le colonne selezionate
    new_csv = df.drop(columns=colonne_da_eliminare)
    new_csv.to_csv(dataset_cluster_path, index=False)

def elimina_preprocessing():
    if os.path.exists(dataset_cluster_path):
        os.unlink(dataset_cluster_path)
