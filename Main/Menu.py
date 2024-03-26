from knowledge_base import KB
from Cluster import clustering
from CSP import CSP
def start():
    flag = True

    while flag:

        print("\n\n============ Menu' del sistema ============")
        print("1. Creazione e interrogazione della Knowledge Base")
        print("2. Modulo apprendimento non supervisionato")
        print("3. Modulo creazione terapie intensive")
        print("0. Uscita")
        print("Inserire il numero corrispondente alla voce da scegliere: ")

        x = input()

        match x:
            case "1":
                KB.inizia_interrogazione()
            case "2":
                clustering.inizia_clustering()
            case "3":
                CSP.menu_csp()
            case "0":
                print("Chiusura programma...")
                flag = False
            case _:
                print("Comando inserito errato. Riprovare: ")
