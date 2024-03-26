import os
import pandas as pd
from pyswip import Prolog
from tabulate import tabulate

kb_path: str = '../knowledge_base/KB.pl'

def crea_kb_file():

    if not os.path.exists(kb_path):
        file = open(kb_path, "x")
        file.close()


def crea_kb(dataset):

    qualifica = ["ausiliare", "OSS", "infermiere", "caposala", "medico"]
    quali_salario_aumento = [["ausiliare", 20907, 700, 7], ["OSS", 22180, 800, 7],
                             ["infermiere", 23653, 1000, 7], ["caposala", 25675, 1200, 8]]
    salario_medico_classificazione = [["incarico professionale", 24143],
                                      ["incarico di responsabile di struttura semplice", 33333],
                                      ["incarico di responsabile di struttura complessa", 45702]]
    salary_range = [20907, 90962]

    with open(kb_path, "w") as file:
        # definizione degli assiomi
        for qu in qualifica:
            file.write(f'qualifiche(\"{qu}\").\n')

        file.write(f'range_stipendio({salary_range[0]}, {salary_range[1]}).\n')

        for index, row in dataset.iterrows():
            file.write(f'matricola(\"{row["matricola"]}\").\n')

        for index, row in dataset.iterrows():
            file.write(f'qualifica(\"{row["qualifica"]}\").\n')

        for index, row in dataset.iterrows():
            file.write(f'qualifica_anzianita(\"{row["qualifica"]}\", {row["anzianita"]}).\n')

        for index, row in dataset.iterrows():
            file.write(f'qualifica_classificazione(\"{row["qualifica"]}\", \"{row["classificazione"]}\").\n')

        for index, row in dataset.iterrows():
            file.write(f'qualifica_stipendio_base(\"{row["qualifica"]}\", {row["stipendio base"]}).\n')

        for index, row in dataset.iterrows():
            file.write(f'qualifica_stipendio(\"{row["qualifica"]}\", {row["stipendio totale"]}).\n')

        for qsa in quali_salario_aumento:
            file.write(f'qualifica_salario_aumento(\"{qsa[0]}\", {qsa[1]}, {qsa[2]}, {qsa[3]}).\n')

        for smc in salario_medico_classificazione:
            file.write(f'qualifica_salario_aumento("medico", 45260, \"{smc[0]}\", {smc[1]}).\n')

        for index, row in dataset.iterrows():
            file.write(f'qualifica_classificazione_stipendio(\"{row["qualifica"]}\", '
                       f'\"{row["classificazione"]}\", {row["stipendio totale"]}).\n')

        for index, row in dataset.iterrows():
            file.write(f'matricola_nome_cognome_qualifica_anzianita_stipendio(\"{row["matricola"]}\", '
                       f'\"{row["nome"]}\", \"{row["cognome"]}\", \"{row["qualifica"]}\", {row["anzianita"]}, '
                       f'{row["stipendio totale"]}).\n')

        for index, row in dataset.iterrows():
            file.write(f'matricola_nome_cognome_qualifica_classificazione_stipendio(\"{row["matricola"]}\", '
                       f'\"{row["nome"]}\", \"{row["cognome"]}\", \"{row["qualifica"]}\", '
                       f'\"{row["classificazione"]}\", {row["stipendio totale"]}).\n')

        for index, row in dataset.iterrows():
            file.write(f'all_data(\"{row["matricola"]}\", \"{row["nome"]}\", \"{row["cognome"]}\", '
                       f'\"{row["qualifica"]}\", {row["anzianita"]}, \"{row["classificazione"]}\", '
                       f'{row["stipendio base"]}, {row["incremento anzianita"]}, {row["bonus incarico"]}, '
                       f'{row["stipendio totale"]}).\n')
    file.close()


def aggiorna_kb_cluster(dataset):

    with open(kb_path, "a") as file:
        for index, row in dataset.iterrows():
            file.write(f'matricola_cluster(\"{row["matricola"]}\", {row["cluster"]}).\n')

    file.close()


def aggiorna_kb_csp(result_path, ti_type, dataset):

    result_list = open(result_path, "r").read().replace("['", "").replace("']", "").split("', '")

    with open(kb_path, "a") as file:
        for index, row in dataset.iterrows():
            if row["matricola"] in result_list:
                file.write(f'matricola_qualifica_ti(\"{row["matricola"]}\", \"{row["qualifica"]}\", \"{ti_type}\").\n')
    file.close()


def crea_regole(dataset_cluster_path):

    with open(kb_path, "a") as file:

        # determina il salario medio in base alla qualifica
        # TipoQualifica: qualifica del personale
        # SalarioMedio: salario medio del personale in base alla qualifica
        file.write(f'''\nsalario_medio_per_qualifica(TipoQualifica, SalarioMedio) :-
                    qualifica(TipoQualifica),
                    findall(Salario, qualifica_stipendio(TipoQualifica, Salario), Salari),
                    length(Salari, Count),
                    sum_list(Salari, Total),
                    SalarioMedio is Total / Count.''')

        # determina l'anzianità media per ogni qualifica
        # TipoQualifica: qualifica del personale
        # AnzianitaMedia: anzianità media del personale in base alla qualifica
        file.write(f'''\n\nanzianita_media_per_qualifica(TipoQualifica,AnzianitaMedia) :-
                    qualifica(TipoQualifica),
                    findall(Anzianita, qualifica_anzianita(TipoQualifica, Anzianita), AnzianitaTotali),
                    length(AnzianitaTotali, Count),
                    sum_list(AnzianitaTotali, Total),
                    AnzianitaMedia is Total / Count.''')

        # determina il salario medio in base alla qualifica e alla classificazione
        # TipoQualifica: qualifica del personale
        # TipoClassificazione: eventuale classificazione del personale
        # SalarioMedio: salario medio del personale in base alla qualifica
        file.write(f'''\n\nsalario_medio_per_qualifica_classificazione(TipoQualifica,TipoClassificazione,SalarioMedio) :-
                    qualifica_classificazione(TipoQualifica,TipoClassificazione),
                    findall(Salario,qualifica_classificazione_stipendio(TipoQualifica,TipoClassificazione,Salario),Salari),
                    length(Salari, Count),
                    sum_list(Salari, Total),
                    SalarioMedio is Total / Count.''')

        # determina il salario medio in base alla qualifica, senza considerare l'anzianità e la classificazione
        # TipoQualifica: qualifica del personale
        # SalarioMedio: salario medio del personale in base alla qualifica
        file.write(f'''\n\nsalario_base_medio_per_qualifica(TipoQualifica, SalarioMedio) :-
                    qualifica(TipoQualifica),
                    findall(Salario, qualifica_stipendio_base(TipoQualifica, Salario), Salari),
                    length(Salari, Count),
                    sum_list(Salari, Total),
                    SalarioMedio is Total / Count.''')

        # determina lo stipendio più alto per qualifica
        # TipoQualifica: qualifica del personale
        # StipendioMassimo: stipendio più alto
        file.write(f'''\n\nstipendio_massimo(TipoQualifica,StipendioMassimo) :-
                    qualifica(TipoQualifica),
                    findall(Salario, qualifica_stipendio(TipoQualifica, Salario), Salari),
                    max(Salari, StipendioMassimo).''')

        # determina lo stipendio più basso per qualifica
        # TipoQualifica: qualifica del personale
        # StipendioMinimo: stipendio più basso
        file.write(f'''\n\nstipendio_minimo(TipoQualifica,StipendioMinimo) :-
                    qualifica(TipoQualifica),
                    findall(Salario, qualifica_stipendio(TipoQualifica, Salario), Salari),
                    min(Salari, StipendioMinimo).''')

        # restituisce una lista di tutto il personale con la stessa qualifica
        # TipoQualifica: qualifica del personale
        # Personale: lista del personale
        file.write(f'''\n\npersonale_qualifiche_con_anzianita(TipoQualifica,Personale) :-
                    qualifica(TipoQualifica),
                    findall(data(Mat, Nom, Cog, Anz, Stip), 
                            matricola_nome_cognome_qualifica_anzianita_stipendio(Mat, Nom, Cog, TipoQualifica, Anz, Stip), 
                            Personale).''')

        # restituisce una lista di tutto il personale con la stessa qualifica
        # TipoQualifica: qualifica del personale
        # Personale: lista del personale
        file.write(f'''\n\npersonale_qualifiche_con_classificazione(TipoQualifica, Personale) :-
                    qualifica(TipoQualifica),
                    findall(data(Mat, Nom, Cog, Clas,Stip), 
                            matricola_nome_cognome_qualifica_classificazione_stipendio(Mat, Nom, Cog, TipoQualifica, Clas, Stip), 
                            Personale).''')

        # restituisce le regole per il calcolo del salario
        # TipoQualifica: qualifica del personale
        # Regola: lista delle regole per il calcolo del salario
        file.write(f'''\n\nregola_salario_personale(TipoQualifica,Regola) :- 
                    qualifica(TipoQualifica), 
                    findall(data(StipendioBase, Aumento, Scatti), 
                            qualifica_salario_aumento(TipoQualifica, StipendioBase, Aumento, Scatti),
                            Regola).''')

        # restituisce le informazioni relative alla persona cercata per matricola
        # Matricola: matricola del personale da cercare
        # Specifica: informazioni relative alla matricola
        file.write(f'''\n\ntrova_personale(Matricola, Specifica) :- 
                    matricola(Matricola),
                    findall(data(Matricola, Nom, Cogn, Qual, Anz, Class, StipB, IncAnz, BonInc, StipTot),
                            all_data(Matricola, Nom, Cogn, Qual, Anz, Class, StipB, IncAnz, BonInc, StipTot),
                            Specifica).''')

        if os.path.exists(dataset_cluster_path):
            # restituisce la lista di cluster del personale
            # Cluster_cercato: tipo di cluster cercato
            # Count: lista dei cluster
            file.write(f'''\n\nconta_cluster(Cluster_cercato, Count) :- 
                                matricola(Matricola),
                                findall(data(Matricola), matricola_cluster(Matricola, Cluster_cercato), Personale),
                                length(Personale, Count).''')

        # restituisce la lista del personale che compone una terapia intensiva
        # TerapiaI: terapia intensiva cercata
        # Personale: lista del personale che compone la terapia intensiva
        file.write(f'''\n\nanalizza_ti(TerapiaI, Personale) :- 
                        findall(data(Mat, Qual), 
                                matricola_qualifica_ti(Mat, Qual, TerapiaI), 
                                Personale).''')

        # confronti per determinare il valore massimo all'interno di una lista
        file.write(f'''\n\nmax([X], X).''')
        file.write(f'''\n\nmax([X, Y|Rest], Max) :- 
                    X=<Y, 
                    max([Y|Rest], Max).''')
        file.write(f'''\n\nmax([X, Y|Rest], Max) :- 
                    Y<X, 
                    max([X|Rest], Max).''')

        # confronti per determinare il valore minimo all'interno di una lista
        file.write(f'''\n\nmin([X], X).''')
        file.write(f'''\n\nmin([X,Y|Rest], Min) :- 
                    X=<Y, 
                    min([X|Rest], Min).''')
        file.write(f'''\n\nmin([X,Y|Rest], Min) :-
                    Y<X, 
                    min([Y|Rest], Min).''')
    file.close()


def query_min_max_stipendio_per_qualifica(prolog):

    flag = True
    qualifiche = ["ausiliare", "OSS", "infermiere", "caposala", "medico"]
    salario_min = "SalarioMin"
    salario_max = "SalarioMax"

    print("\n============ SALARIO MINIMO E MASSIMO PER QUALIFICA ============")
    for x in range(len(qualifiche)):
        print(str(x+1) + ". " + qualifiche[x])
    print("0. Annulla operazione")
    print("Scegli la qualifica per la quale si vuole stampare il salario minimo e massimo: ")

    while flag:
        scelta = input()
        string_scelta = qualifiche[int(scelta)-1]

        match scelta:
            case '1' | '2' | '3' | '4' | '5':
                result = list(prolog.query(f'stipendio_minimo(\"{string_scelta}\", {salario_min})'))
                risultato = float(result[0][salario_min])
                print(f"\nIl salario minimo per la qualifica di \"{string_scelta}\" è %.2f euro." % risultato)

                result = list(prolog.query(f'stipendio_massimo(\"{string_scelta}\", {salario_max})'))
                risultato = float(result[0][salario_max])
                print(f"Il salario massimo per la qualifica di \"{string_scelta}\" è %.2f euro." % risultato)
                flag = False

            case '0':
                print("Annullamento operazione.")
                flag = False

            case _:
                print("Comando inserito errato. Riprova: ")


def query_regola_calcolo_salario(prolog):

    flag = True
    qualifiche = ["ausiliare", "OSS", "infermiere", "caposala", "medico"]
    output = "Regola"

    print("\n============ REGOLA PER IL CALCOLO DEL SALARIO PER QUALIFICA ============")

    for x in range(len(qualifiche)):
        print(str(x + 1) + ". " + qualifiche[x])
    print("0. Annulla operazione")
    print("Scegli la qualifica per la quale si vuole mostrare la regola per il calcolo del salario: ")

    while flag:
        scelta = input()
        string_scelta = qualifiche[int(scelta) - 1]

        match scelta:
            case '1' | '2' | '3' | '4':
                result = list(prolog.query(f'regola_salario_personale(\"{string_scelta}\", {output})'))
                risultato = str(result[0][output]).replace("[data(", "").replace(")]", "")
                stampa_regola_salario(risultato, string_scelta)
                flag = False

            case '5':
                regole = []
                result = list(prolog.query(f'regola_salario_personale(\"{string_scelta}\", {output})'))
                for x in range(3):
                    regole.append(str(result[0][output][x]).replace("data", "").replace("b'", "'"))
                stampa_regola_salario(regole, string_scelta)
                flag = False

            case '0':
                print("Annullamento operazione.")
                flag = False

            case _:
                print("Comando inserito errato. Riprova: ")


def query_qualifiche_remunerative(prolog):

    matrice_qualifiche = [["ausiliare", 0.0], ["OSS", 0.0], ["infermiere", 0.0], ["caposala", 0.0],
                          ["medico con incarico professionale", 0.0],
                          ["medico con incarico di responsabile di struttura semplice", 0.0],
                          ["medico con incarico di responsabile di struttura complessa", 0.0]]
    output = "SalarioMedio"

    print("\n============ QUALIFICHE PIU' REMUNERATIVE ============")
    for x in range(len(matrice_qualifiche)):
        if x > 3:
            splitted_string = str(matrice_qualifiche[x]).split(" con ")
            qualifica = splitted_string[0].replace("['", "")
            class_qualifica = splitted_string[1].replace("', 0.0]", "")

            result = list(prolog.query(f'salario_medio_per_qualifica_classificazione(\"{qualifica}\", '
                                       f'\"{class_qualifica}\", {output})'))
            matrice_qualifiche[x][1] = float(result[0][output])
        else:
            result = list(prolog.query(f'salario_medio_per_qualifica(\"{matrice_qualifiche[x][0]}\", {output})'))
            matrice_qualifiche[x][1] = float(result[0][output])

    for i in range(len(matrice_qualifiche)):
        min_index = i
        for j in range(i+1, len(matrice_qualifiche)):
            if matrice_qualifiche[j][1] > matrice_qualifiche[min_index][1]:
                min_index = j

        matrice_qualifiche[i], matrice_qualifiche[min_index] = matrice_qualifiche[min_index], matrice_qualifiche[i]

    print("Le qualifiche più remunerative in ordine decrescente sono: ")
    for x in range(len(matrice_qualifiche)):
        print(f'{x+1}. {matrice_qualifiche[x][0]}')


def query_media_stipendi_per_qualifica(prolog):

    flag = True
    qualifiche = ["ausiliare", "OSS", "infermiere", "caposala", "medico"]
    classificazioni = ["incarico professionale", "incarico di responsabile di struttura semplice",
                       "incarico di responsabile di struttura complessa"]
    output = "SalarioMedio"

    print("\n============ SALARIO MEDIO PER QUALIFICA ============")
    for x in range(5):
        print(str(x+1) + ". " + qualifiche[x])
    print("0. Annulla operazione")
    print("Scegli la qualifica per la quale si vuole calcolare lo stipendio medio: ")

    while flag:
        scelta = input()
        string_scelta = qualifiche[int(scelta) - 1]

        match scelta:
            case '1' | '2' | '3' | '4':
                result = list(prolog.query(f'salario_medio_per_qualifica(\"{string_scelta}\", {output})'))
                risultato = float(result[0][output])
                print(f"\nIl salario medio per la qualifica di \"{string_scelta}\" è %.2f euro" % risultato)
                flag = False

            case '5':
                print("Scegli la classificazione del medico per il quale si vuole calcolare lo stipendio medio: ")
                classification_flag = True
                scelta_classificazione = 0
                while classification_flag:
                    for y in range(3):
                        print(str(y + 1) + ". " + classificazioni[y])

                    scelta_classificazione = int(input())
                    if (scelta_classificazione > 0) and (scelta_classificazione < 4):
                        classification_flag = False
                    else:
                        print("Scelta inserita errata. Riprovare tra le seguenti: ")

                result = list(prolog.query(
                    f'salario_medio_per_qualifica_classificazione(\"{string_scelta}\", '
                    f'\"{classificazioni[scelta_classificazione - 1]}\", {output})'))

                risultato = float(result[0][output])
                print(f"\nIl salario per la qualifica di \"{string_scelta}\" con "
                      f"\"{classificazioni[int(scelta_classificazione) - 1]}\" è %.2f euro" % risultato)
                flag = False

            case '0':
                print("Annullamento operazione.")
                flag = False

            case _:
                print("Comando inserito errato. Riprova: ")


def query_confronta_qualifiche(prolog):

    flag = True
    qualifiche = ["ausiliare", "OSS", "infermiere", "caposala", "medico"]
    prima_anzianita = 0
    seconda_anzianita = 0
    o_salario = "SalarioMedio"
    o_anzianita = "AnzianitaMedia"

    print("\n============ CONFRONTO FRA QUALIFICHE ============")

    print("Desideri comparare gli stipendi tenendo conto dell'anzianità e della classificazione dei medici?")
    while flag:
        print("1. Si")
        print("2. No")

        scelta = input()
        match scelta:

            case "1":
                class_prima_qualifica = "no"
                class_seconda_qualifica = "no"
                qualifiche = unisci_qualifiche_classificazione(qualifiche)

                print("\nScegli la prima qualifica da confrontare tra le seguenti: ")
                while True:
                    for x in range(len(qualifiche)):
                        print(str(x + 1) + ". " + qualifiche[x])

                    num_scelto = int(input()) - 1
                    if num_scelto in range(len(qualifiche)):
                        break
                    else:
                        print("\nScelta sbagliata. Inserire il numero corretto tra i seguenti: ")

                prima_qualifica = qualifiche[num_scelto]
                qualifiche.remove(prima_qualifica)
                print("\nScegli la seconda qualifica da confrontare tra le seguenti: ")

                while True:
                    for x in range(len(qualifiche)):
                        print(str(x + 1) + ". " + qualifiche[x])

                    num_scelto = int(input()) - 1
                    if num_scelto in range(len(qualifiche)):
                        break
                    else:
                        print("\nScelta sbagliata. Inserire il numero corretto tra i seguenti: ")

                seconda_qualifica = qualifiche[num_scelto]

                if prima_qualifica.startswith("medico"):
                    splitted_string = prima_qualifica.split(" con ")

                    prima_qualifica = splitted_string[0]
                    class_prima_qualifica = splitted_string[1]

                    result = list(prolog.query(f'salario_medio_per_qualifica_classificazione(\"{prima_qualifica}\", '
                                               f'\"{class_prima_qualifica}\", {o_salario})'))
                    primo_salario = float(result[0][o_salario])

                else:
                    result = list(prolog.query(f'salario_medio_per_qualifica(\"{prima_qualifica}\", {o_salario})'))
                    primo_salario = float(result[0][o_salario])
                    result = list(prolog.query(f'anzianita_media_per_qualifica(\"{prima_qualifica}\", {o_anzianita})'))
                    prima_anzianita = float(result[0][o_anzianita])

                if seconda_qualifica.startswith("medico"):
                    splitted_string = seconda_qualifica.split(" con ")

                    seconda_qualifica = splitted_string[0]
                    class_seconda_qualifica = splitted_string[1]

                    result = list(prolog.query(f'salario_medio_per_qualifica_classificazione(\"{seconda_qualifica}\", '
                                               f'\"{class_seconda_qualifica}\", {o_salario})'))
                    secondo_salario = float(result[0][o_salario])
                else:
                    result = list(prolog.query(f'salario_medio_per_qualifica(\"{seconda_qualifica}\", {o_salario})'))
                    secondo_salario = float(result[0][o_salario])
                    result = list(
                        prolog.query(f'anzianita_media_per_qualifica(\"{seconda_qualifica}\", {o_anzianita})'))
                    seconda_anzianita = float(result[0][o_anzianita])

                confronto_salario_con_classificazione(primo_salario, prima_qualifica, class_prima_qualifica,
                                                      secondo_salario, seconda_qualifica, class_seconda_qualifica)

                if not prima_qualifica == "medico":
                    print(f"Il salario medio per la qualifica di {prima_qualifica} è %.2f euro, "
                          f"con un'anzianità media di %d anni." % (primo_salario, prima_anzianita))
                else:
                    print(f"Il salario per la qualifica di {prima_qualifica} con {class_prima_qualifica} è "
                          f"%.2f euro." % primo_salario)

                if not seconda_qualifica == "medico":
                    print(f"Il salario medio per la qualifica di {seconda_qualifica} è %.2f euro, "
                          f"con un'anzianità media di %d anni." % (secondo_salario, seconda_anzianita))
                else:
                    print(
                        f"Il salario per la qualifica di {seconda_qualifica} con {class_seconda_qualifica} è "
                        f"%.2f euro." % secondo_salario)

                flag = False

            case "2":
                print("\nScegli la prima qualifica da confrontare tra le seguenti: ")
                while True:
                    for x in range(len(qualifiche)):
                        print(str(x + 1) + ". " + qualifiche[x])

                    num_scelto = int(input()) - 1
                    if num_scelto in range(len(qualifiche)):
                        break
                    else:
                        print("\nScelta sbagliata. Inserire il numero corretto tra i seguenti: ")

                prima_qualifica = qualifiche[num_scelto]
                qualifiche.remove(prima_qualifica)
                print("\nScegli la seconda qualifica da confrontare tra le seguenti: ")

                while True:
                    for x in range(len(qualifiche)):
                        print(str(x + 1) + ". " + qualifiche[x])

                    num_scelto = int(input()) - 1
                    if num_scelto in range(len(qualifiche)):
                        break
                    else:
                        print("\nScelta sbagliata. Inserire il numero corretto tra i seguenti: ")

                seconda_qualifica = qualifiche[num_scelto]

                result = list(prolog.query(f'salario_base_medio_per_qualifica(\"{prima_qualifica}\", {o_salario})'))
                primo_salario = float(result[0][o_salario])
                result = list(prolog.query(f'salario_base_medio_per_qualifica(\"{seconda_qualifica}\", {o_salario})'))
                secondo_salario = float(result[0][o_salario])

                confronto_salario(primo_salario, prima_qualifica, secondo_salario, seconda_qualifica)
                print(f"Il salario medio per la qualifica di \"{prima_qualifica}\" è %.2f euro" % primo_salario)
                print(f"Il salario medio per la qualifica di \"{seconda_qualifica}\" è %.2f euro" % secondo_salario)
                flag = False


def query_top_personale_per_qualifica(prolog, tipo_ordinamento):

    flag = True
    qualifiche = ["ausiliare", "OSS", "infermiere", "caposala", "medico"]
    output = "Classifica"

    print("\n============ CLASSIFICA DEL PERSONALE PER STIPENDIO ============")
    for x in range(len(qualifiche)):
        print(str(x + 1) + ". " + qualifiche[x])
    print("0. Annulla operazione")
    print("Scegli la qualifica per la quale si vogliono determinare la graduatoria in base allo stipendio: ")

    while flag:
        scelta = input()
        string_scelta = qualifiche[int(scelta)-1]

        match scelta:
            case '1' | '2' | '3' | '4':
                result = list(prolog.query(f'personale_qualifiche_con_anzianita(\"{string_scelta}\", {output})'))

                for x in range(len(result[0][output])):
                    result[0][output][x] = str(result[0][output][x]).replace("data(", "").replace("b'", "'")
                    result[0][output][x] = result[0][output][x].replace(")", "")

                lista_personale = modifica_lista(result[0][output], string_scelta)
                if tipo_ordinamento == "discendente":
                    selection_sort_discendente(lista_personale)
                elif tipo_ordinamento == "ascendente":
                    selection_sort_ascendente(lista_personale)
                stampa_personale(lista_personale, string_scelta)

                flag = False

            case '5':
                result = list(prolog.query(f'personale_qualifiche_con_classificazione(\"{string_scelta}\", {output})'))

                for x in range(len(result[0][output])):
                    result[0][output][x] = str(result[0][output][x]).replace("data(", "").replace("b'", "'")
                    result[0][output][x] = result[0][output][x].replace(")", "")

                lista_personale = modifica_lista(result[0][output], string_scelta)
                if tipo_ordinamento == "discendente":
                    selection_sort_discendente(lista_personale)
                elif tipo_ordinamento == "ascendente":
                    selection_sort_ascendente(lista_personale)
                stampa_personale(lista_personale, string_scelta)

                flag = False

            case '0':
                print("Annullamento operazione.")
                flag = False

            case _:
                print("Comando inserito errato. Riprova: ")


def query_trova_personale(prolog):

    flag = True
    mat = ""
    output = "Specifica"
    headers_dataset = ["matricola", "nome", "cognome", "qualifica", "anzianità", "classificazione", "stipendio base",
                       "incremento anzianità", "bonus incarico", "stipendio totale"]
    print("\n============ TROVA PERSONALE DALLA MATRICOLA ============")

    print("Inserisci la matricola per cercare le informazioni del personale: ")
    while flag:
        mat = input()
        mat, flag = controlla_matricola(mat, flag)

    result = list(prolog.query(f'trova_personale(\"{mat}\", {output})'))
    lista = string_to_list(str(result[0][output][0]))

    print()
    print(tabulate(lista, headers=headers_dataset))


def query_mostra_cluster(prolog):

    print("\n============ VISUALIZZA NUMERO DI CLUSTER ============")

    result = list(prolog.query('conta_cluster(0, Valore)'))
    cluster_zero = 0
    cluster_uno = 0

    for x in result:
        if x["Valore"] == 1:
            cluster_zero += 1
        elif x["Valore"] == 0:
            cluster_uno += 1

    print(f'Personale appartenente al cluster 0: {cluster_zero}')
    print(f'Personale appartenente al cluster 1: {cluster_uno}')


def query_analizza_terapia_intensiva(prolog):

    csp_type = ['utic', 'rianimazione', 'stroke_unit', 'dialisi', 'respiratoria', 'utin']
    qualifiche = [["ausiliare", 0], ["OSS", 0], ["infermiere", 0], ["caposala", 0], ["medico", 0]]
    result_list = []
    flag = True

    print("\n============ VISUALIZZA ORGANIZZAZIONE DI UNA TERAPIA INTENSIVA ============")
    for x in range(len(csp_type)):
        print(f'{x+1}. {csp_type[x]}')
    print("0. Annulla operazione")
    print("Seleziona la terapia intensiva:")

    while flag:
        scelta = input()

        match scelta:

            case '1' | '2' | '3' | '4' | '5':
                string_scelta = csp_type[int(scelta) - 1]

                result = list(prolog.query(f'analizza_ti(\"{string_scelta}\", Personale)'))[0]['Personale']
                for x in result:
                    result_list.append(str(x).replace("data(", "").replace("b'", "")
                                       .replace(")", "").replace("'", "").split(", "))

                if not result_list:
                    print("\nNessun risultato trovato.")
                else:
                    print("\nOrganizzazione del personale:")
                    for qual in qualifiche:
                        for rl in result_list:
                            if qual[0] == rl[1]:
                                qual[1] += 1

                    for x in range(len(qualifiche)):
                        i = 0
                        if not qualifiche[x][1] == 0:
                            print(f'{qualifiche[x][0]}: {qualifiche[x][1]} -> ', end="")
                            for y in range(len(result_list)):
                                if qualifiche[x][0] == result_list[y][1]:
                                    i += 1
                                    print(f'\"{result_list[y][0]}\"', end="")

                                    if not i == qualifiche[x][1]:
                                        print(', ', end="")
                                    else:
                                        print(';')

                flag = False

            case '0':
                print("Annullamento operazione.")
                flag = False

            case _:
                print("Comando inserito errato. Riprova: ")


def string_to_list(stringa):

    lista_finale = []
    lista = stringa.replace("data(", "").replace("b'", "'").replace(")", "").split(",")

    for x in range(10):
        if x in [4, 6, 7, 8, 9]:
            lista[x] = int(lista[x])
        else:
            lista[x] = lista[x].replace("'", "")
    lista_finale.append(lista)

    return lista_finale


def controlla_matricola(matricola, flag):

    if len(matricola) == 6:
        if matricola[0:1] == "a":
            matricola = matricola.replace("a", "A")
        if not matricola[0:1] == "A":
            print("Matricola inserita errata. Riprovare: ")
        else:
            if (int(matricola[1:6]) > 0) and (int(matricola[1:6]) < 501):
                flag = False
            else:
                print("Matricola inserita errata. Riprovare: ")
    else:
        print("Matricola inserita errata. Riprovare: ")

    return matricola, flag


def confronto_salario_con_classificazione(primo_salario, prima_qualifica, class_prima_qualifica,
                                          secondo_salario, seconda_qualifica, class_seconda_qualifica):

    if primo_salario > secondo_salario:
        resto = primo_salario - secondo_salario
        if class_prima_qualifica == "no" and class_seconda_qualifica == "no":
            print(f'\nIl salario medio della qualifica di {prima_qualifica} è maggiore del salario medio '
                  f'della qualifica di {seconda_qualifica} di %.2f euro.' % resto)
        elif prima_qualifica == "medico" and class_seconda_qualifica == "no":
            print(f'\nIl salario della qualifica di {prima_qualifica} con {class_prima_qualifica} è '
                  f'maggiore del salario medio della qualifica di \"{seconda_qualifica}\" di %.2f euro.' % resto)
        elif class_prima_qualifica == "no" and seconda_qualifica == "medico":
            print(f'\nIl salario medio della qualifica di {prima_qualifica} è maggiore del salario della qualifica'
                  f' di {seconda_qualifica} con {class_seconda_qualifica} di %.2f euro.' % resto)
        elif prima_qualifica == "medico" and seconda_qualifica == "medico":
            print(f'\nIl salario della qualifica di {prima_qualifica} con {class_prima_qualifica} è maggiore'
                  f' del salario della qualifica di {seconda_qualifica} con {class_seconda_qualifica}'
                  f' di %.2f euro.' % resto)
    else:
        resto = secondo_salario - primo_salario
        if class_prima_qualifica == "no" and class_seconda_qualifica == "no":
            print(f'\nIl salario medio della qualifica di {prima_qualifica} è minore del salario medio '
                  f'della qualifica di {seconda_qualifica} di %.2f euro.' % resto)
        elif prima_qualifica == "medico" and class_seconda_qualifica == "no":
            print(f'\nIl salario della qualifica di {prima_qualifica} con {class_prima_qualifica} è '
                  f'minore del salario medio della qualifica di \"{seconda_qualifica}\" di %.2f euro.' % resto)
        elif class_prima_qualifica == "no" and seconda_qualifica == "medico":
            print(f'\nIl salario medio della qualifica di {prima_qualifica} è minore del salario della qualifica'
                  f' di {seconda_qualifica} con {class_seconda_qualifica} di %.2f euro.' % resto)
        elif prima_qualifica == "medico" and seconda_qualifica == "medico":
            print(f'\nIl salario della qualifica di {prima_qualifica} con {class_prima_qualifica} è minore '
                  f'del salario della qualifica di {seconda_qualifica} con {class_seconda_qualifica}'
                  f' di %.2f euro.' % resto)


def confronto_salario(primo_salario, prima_qualifica, secondo_salario, seconda_qualifica):

    if primo_salario > secondo_salario:
        resto = primo_salario - secondo_salario
        print(f'\nIl salario medio della qualifica di \"{prima_qualifica}\" è maggiore del salario medio '
              f'della qualifica di \"{seconda_qualifica}\" di %.2f euro.' % resto)
    elif secondo_salario > primo_salario:
        resto = secondo_salario - primo_salario
        print(f'\nIl salario medio della qualifica di \"{prima_qualifica}\" è minore del salario medio '
              f'della qualifica di \"{seconda_qualifica}\" di %.2f euro.' % resto)


def modifica_lista(lista, qualifica):

    nuova_lista = []
    if not qualifica == "medico":

        for x in range(len(lista)):
            lista[x] = lista[x].split(",")
            lista[x][3] = int(lista[x][3])
            lista[x][4] = int(lista[x][4])

        for x in range(len(lista)):
            temp_lista = ["", "", "", 0, 0]
            for y in range(len(temp_lista)):
                temp_lista[y] = lista[x][y]
            nuova_lista.append(temp_lista)
    else:
        for x in range(len(lista)):
            lista[x] = lista[x].split(",")
            lista[x][4] = int(lista[x][4])

        for x in range(len(lista)):
            temp_lista = ["", "", "", "", 0]
            for y in range(len(temp_lista)):
                temp_lista[y] = lista[x][y]
            nuova_lista.append(temp_lista)

    return nuova_lista


def selection_sort_discendente(lista):

    for i in range(len(lista)):
        min_index = i

        for j in range(i+1, len(lista)):
            if lista[j][4] > lista[min_index][4]:
                min_index = j

        lista[i], lista[min_index] = lista[min_index], lista[i]


def selection_sort_ascendente(lista):

    for i in range(len(lista)):
        min_index = i

        for j in range(i+1, len(lista)):
            if lista[j][4] < lista[min_index][4]:
                min_index = j

        lista[i], lista[min_index] = lista[min_index], lista[i]


def stampa_personale(lista, qualifica):

    lista_finale = []

    if not qualifica == "caposala":
        lunghezza_lista = 10
    else:
        lunghezza_lista = 6

    for x in range(lunghezza_lista):
        lista_finale.append((lista[x]))

    print()
    if not qualifica == "medico":
        print(tabulate(lista_finale, headers=["Matricola", "Nome", "Cognome", "Anzianità", "Salario totale"]))
    else:
        print(tabulate(lista_finale, headers=["Matricola", "Nome", "Cognome", "Classificazione", "Salario totale"]))


def stampa_regola_salario(regola, qualifica):

    dati_regola = []
    if not qualifica == "medico":
        for x in regola.split(","):
            dati_regola.append(int(x))
        print("\nStipendio totale = stipendio base + incremento anzianità")
        print(f"\nLo stipendio base per la qualifica di {qualifica} è: {dati_regola[0]} euro.")
        print("Incremento anzianità: ")
        for x in range(1, dati_regola[2]):
            print(f"Dopo {x*5} anni di anzianità raggiunta, riceverà un aumento di {x*dati_regola[1]} euro, "
                  f"per un totale di {dati_regola[0] + x*dati_regola[1]} euro.")
    else:
        for x in regola:
            dati_regola.append(x.replace("(", "").replace(")", "").split(","))
        print("\nStipendio totale = stipendio base + bonus incarico")
        print(f"\nLo stipendio base per la qualifica di {qualifica} è: {dati_regola[0][0]} euro.")
        print("Bonus incarico: ")
        for x in range(len(dati_regola)):
            print(f"Un medico con un{dati_regola[x][1]} riceverà un bonus incarico di{dati_regola[x][2]} euro, "
                  f"per un totale di {int(dati_regola[x][0]) + int(dati_regola[x][2])} euro.")


def unisci_qualifiche_classificazione(qualifiche):

    classificazioni = ["incarico professionale", "incarico di responsabile di struttura semplice",
                       "incarico di responsabile di struttura complessa"]
    qualifiche_aggiornate = []

    for x in range(5):
        if qualifiche[x] == "medico":
            for y in classificazioni:
                qualifiche_aggiornate.append(qualifiche[x] + " con " + y)
        else:
            qualifiche_aggiornate.append(qualifiche[x])

    return qualifiche_aggiornate


def chiedi_query():

    flag = True
    prolog = Prolog()
    prolog.consult(kb_path)

    while flag:
        print("\n\n============ INTERROGAZIONE DELLA KB ============")
        print("1. Massimo e minimo dello stipendio in base alla qualifica")
        print("2. Visualizza la regola con la quale viene calcolato lo stipendio")
        print("3. Visualizza in ordine decrescente le qualifiche in base allo stipendio")
        print("4. Media degli stipendi in base alla qualifica")
        print("5. Confronto di due qualifiche in base agli stipendi")
        print("6. Visualizza la graduatoria del personale con lo stipendio più alto rispetto alla qualifica")
        print("7. Visualizza la graduatoria del personale con lo stipendio più basso rispetto alla qualifica")
        print("8. Visualizza le caratteristiche del dipendente tramite la sua matricola")
        print("9. Visualizza la suddivisione del personale nei cluster")
        print("10. Visualizza il personale assegnato ad una terapia intensiva")
        print("0. Termina l'interrogazione alla Knowledge Base")
        print("Inserisci il numero della query che si vuole effettuare sulla KB: ")

        scelta = input()
        match scelta:
            case "1":
                query_min_max_stipendio_per_qualifica(prolog)

            case "2":
                query_regola_calcolo_salario(prolog)

            case "3":
                query_qualifiche_remunerative(prolog)

            case "4":
                query_media_stipendi_per_qualifica(prolog)

            case "5":
                query_confronta_qualifiche(prolog)

            case "6":
                query_top_personale_per_qualifica(prolog, "discendente")

            case "7":
                query_top_personale_per_qualifica(prolog, "ascendente")

            case "8":
                query_trova_personale(prolog)

            case "9":
                if os.path.exists('../dataset/dataset+Cluster.csv'):
                    query_mostra_cluster(prolog)
                else:
                    print("Operazione momentaneamente non disponibile. "
                          "Eseguire prima il modulo dell'apprendimento non supervisionato.")

            case "10":
                query_analizza_terapia_intensiva(prolog)

            case "0":
                if os.path.exists(kb_path):
                    os.unlink(kb_path)
                flag = False

            case _:
                print("Comando inserito errato. Riprovare: ")


def inizia_interrogazione():

    dataset_path = '../dataset/dataset.csv'
    dataset_cluster_path = '../dataset/dataset+Cluster.csv'
    results_csp_path = '../CSP/results/csp_'
    ti_type = ['utic', 'rianimazione', 'stroke_unit', 'dialisi', 'respiratoria', 'utin']
    dataset = pd.read_csv(dataset_path)

    if not os.path.exists(kb_path):
        crea_kb_file()
        crea_kb(dataset)

        if os.path.exists(dataset_cluster_path):
            dataset_cluster = pd.read_csv(dataset_cluster_path)
            aggiorna_kb_cluster(dataset_cluster)

        for ti in ti_type:
            path = results_csp_path + ti + '.txt'
            if os.path.exists(path):
                aggiorna_kb_csp(path, ti, dataset)

        crea_regole(dataset_cluster_path)

    chiedi_query()
