from constraint import *
import pandas as pd
from tabulate import tabulate
import csv
import os

def menu_csp():

    flag = True

    while flag:
        print("\n============ CREAZIONE E VISUALIZZAZIONE DELLE TERAPIE INTENSIVE ============")
        print("1. Creazione terapia intensiva")
        print("2. Visualizzazione terapie intensive create")
        print("0. Torna al menu' principale")

        scelta = input()

        match scelta:
            case "1":
                start_csp()

            case "2":
                vedi_risultati()

            case "0":
                print("Ritorno al menu' principale...")
                flag = False

            case _:
                print("Inserire un numero valido")


def start_csp():

    print("Benvenuto nel processo di creazione di una terapia intensiva, "
          "scegliere il reparto di terapia intensiva che si vuole aprire.")
    if not os.path.exists("../dataset/datasetCSP.csv"):
        crea_colonna_assegnato()

    if not os.path.exists("../CSP/results"):
        os.mkdir("../CSP/results")

    flag = True

    while flag:

        print("\n============ Scelta reparti di terapia intensiva ============")
        print("1. UNITA' TERAPIA INTENSIVA CORONARICA (UTIC)")
        print("2. RIANIMAZIONE E RIANIMAZIONE POST-OPERATORIA")
        print("3. STROKE-UNIT")
        print("4. DIALISI")
        print("5. TERAPIA INSTENSIVA RESPIRATORIA")
        print("6. UNITA' TERAPIA INTENSIVA NEONATALE (UTIN)")
        print("0. Torna indietro.")
        print("Inserire il numero corrispondente al reparto che si desidera creare: ")

        terapia = input()

        match terapia:
            case "1":
                path = "../CSP/results/csp_utic.txt"
                if not os.path.exists(path):
                    print("Inizio processo di apertura del reparto di terapia intensiva UTIC")
                    csp_info_utic(path)
                else:
                    if scelta_eliminazione():
                        elimina_terapia(path)

            case "2":
                path = "../CSP/results/csp_rianimazione.txt"
                if not os.path.exists(path):
                    print("Inizio processo di apertura del reparto di terapia intensiva "
                          "RIANIMAZIONE E RIANIMAZIONE POST-OPERATORIA")
                    csp_info_rianimazione(path)
                else:
                    if scelta_eliminazione():
                        elimina_terapia(path)

            case "3":
                path = "../CSP/results/csp_stroke_unit.txt"
                if not os.path.exists(path):
                    print("Inizio processo di apertura del reparto di terapia intensiva STROKE-UNIT")
                    csp_info_stroke_unit(path)
                else:
                    if scelta_eliminazione():
                        elimina_terapia(path)

            case "4":
                path = "../CSP/results/csp_dialisi.txt"
                if not os.path.exists(path):
                    print("Inizio processo di apertura del reparto di terapia intensiva DIALISI")
                    csp_info_dialisi(path)
                else:
                    if scelta_eliminazione():
                        elimina_terapia(path)

            case "5":
                path = "../CSP/results/csp_respiratoria.txt"
                if not os.path.exists(path):
                    print("Inizio processo di apertura del reparto di terapia intensiva "
                          "TERAPIA INSTENSIVA RESPIRATORIA")
                    csp_info_respiratoria(path)
                else:
                    if scelta_eliminazione():
                        elimina_terapia(path)

            case "6":
                path = "../CSP/results/csp_utin.txt"
                if not os.path.exists(path):
                    print("Inizio processo di apertura del reparto di terapia intensiva UTIN")
                    csp_info_utin(path)
                else:
                    if scelta_eliminazione():
                        elimina_terapia(path)

            case "0":
                print("Ritorno indietro...")
                flag = False
            case _:
                print("Inserire un numero valido")


def prendi_cap(indirizzo, lista):

    lista.append(indirizzo[1][-5:])
    return lista


def trova_cap():

    dataset_path = '../dataset/dataset.csv'
    lista_cap = []

    with open(dataset_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first = True
        for riga in csv_reader:
            if first:
                first = False
                continue
            lista_cap = prendi_cap(riga[6].split(","), lista_cap)

    return lista_cap


def scelta_infermieri():

    print("\n\nScegliere se si preferisce inserire infermieri giovani o in base all'esperienza maturata in servizio.")
    flag = True
    preferenza_infermieri = 2

    while flag:

        print("\n============ Preferenza anzianita' di serivzio degli infermieri ============")
        print("1. Infermieri sotto i 20 anni di anzianita' ")
        print("2. Infermieri uguali o superiori a 20 anni di anzianita' ")
        print("0. Torna indietro ")
        print("Inserire il numero corrispondente alla preferenza da scegliere: ")

        pref = input()

        match pref:
            case "1":
                print("Selezionato infermieri sotto i 20 anni di anzianita' ")
                preferenza_infermieri = 1
                flag = False
            case "2":
                print("Selezionato infermieri con 20 o piu' anni di anzianita' ")
                preferenza_infermieri = 0
                flag = False
            case "0":
                flag = False
            case _:
                print("Inserire un numero valido")

    return preferenza_infermieri


def scelta_medico():

    print("\n\nScegliere se si vuole inserire un medico responsabile di struttura semplice o di struttura complessa "
          "a seconda della valenza strategica che si intende assegnare alla struttura. ")
    flag = True
    medico_responsabile = 2

    while flag:

        print("\n============ Preferenza classificazione medico responsabile ============")
        print("1. Medico con classificazione di responsabile di stuttura semplice ")
        print("2. Medico con classificazione di responsabile di stuttura complessa ")
        print("0. Torna indietro ")
        print("Inserire il numero corrispondente alla preferenza da scegliere: ")

        responsabile = input()

        match responsabile:
            case "1":
                print("Selezionato medico con classificazione di responsabile di stuttura semplice \n")
                medico_responsabile = 1
                flag = False
            case "2":
                print("Selezionato medico con classificazione di responsabile di stuttura complessa \n")
                medico_responsabile = 0
                flag = False
            case "0":
                flag = False
            case _:
                print("Inserire un numero valido")

    return medico_responsabile


def csp_info_utic(path):

    print("Inserire il numero di posti letto disponibili all'interno della terapia intensiva: ")
    bed_number = int(input())
    while bed_number < 1 or bed_number > 10:
        print("Inserire un numero valido di posti letto.")
        bed_number = int(input())

    print("Inserire il budget disponibile per la creazione della terapia intensiva (esclusi oneri): ")
    budget = int(input())
    if 1 <= bed_number <= 3:
        while budget < 310000:
            print("La cifra inserita non è sufficiente per aprire un reparto di terapia intensiva UTIC con "
                  "il numero di posti letto inseriti.")
            budget = int(input())
    if 4 <= bed_number <= 7:
        while budget < 510000:
            print("La cifra inserita non è sufficiente per aprire un reparto di terapia intensiva UTIC con "
                  "il numero di posti letto inseriti.")
            budget = int(input())
    if 8 <= bed_number <= 10:
        while budget < 650000:
            print("La cifra inserita non è sufficiente per aprire un reparto di terapia intensiva UTIC con "
                  "il numero di posti letto inseriti.")
            budget = int(input())

    preferenza_infermieri = scelta_infermieri()
    if not preferenza_infermieri == 2:
        medico_responsabile = scelta_medico()
        if not medico_responsabile == 2:

            n_responsabili = 0
            n_medici = 0
            n_oss = 0
            n_infermieri = 0
            n_caposala = 0

            if 1 <= bed_number <= 3:
                n_responsabili = 1
                n_medici = 1
                n_oss = 1
                n_infermieri = 5
            if 4 <= bed_number <= 7:
                n_responsabili = 1
                n_medici = 2
                n_oss = 1
                n_infermieri = 10
            if 8 <= bed_number <= 10:
                n_responsabili = 1
                n_medici = 3
                n_caposala = 1
                n_oss = 1
                n_infermieri = 13

            print("Avvio ricerca...")
            csp_utic(n_responsabili, n_medici, n_oss, n_infermieri, n_caposala,
                     preferenza_infermieri, medico_responsabile, budget, path)


def csp_info_rianimazione(path):

    print("Inserire il numero di posti letto disponibili all'interno della terapia intensiva: ")
    bed_number = int(input())
    while bed_number < 1 or bed_number > 10:
        print("Inserire un numero valido di posti letto.")
        bed_number = int(input())

    print("Inserire il budget disponibile per la creazione della terapia intensiva (esclusi oneri): ")
    budget = int(input())
    if 1 <= bed_number <= 3:
        while budget < 337000:
            print("La cifra inserita non è sufficiente per aprire un reparto di terapia intensiva Rianimazione con "
                  "il numero di posti letto inseriti.")
            budget = int(input())
    if 4 <= bed_number <= 7:
        while budget < 564000:
            print("La cifra inserita non è sufficiente per aprire un reparto di terapia intensiva Rianimazione con "
                  "il numero di posti letto inseriti.")
            budget = int(input())
    if 8 <= bed_number <= 10:
        while budget < 731000:
            print("La cifra inserita non è sufficiente per aprire un reparto di terapia intensiva Rianimazione con "
                  "il numero di posti letto inseriti.")
            budget = int(input())

    preferenza_infermieri = scelta_infermieri()
    if not preferenza_infermieri == 2:
        medico_responsabile = scelta_medico()
        if not medico_responsabile == 2:

            n_responsabili = 0
            n_medici = 0
            n_oss = 0
            n_infermieri = 0
            n_caposala = 0

            if 1 <= bed_number <= 3:
                n_responsabili = 1
                n_medici = 1
                n_oss = 1
                n_infermieri = 6
            if 4 <= bed_number <= 7:
                n_responsabili = 1
                n_medici = 2
                n_oss = 1
                n_infermieri = 12
            if 8 <= bed_number <= 10:
                n_responsabili = 1
                n_medici = 3
                n_caposala = 1
                n_oss = 1
                n_infermieri = 16

            print("Avvio ricerca...")
            csp_rianimazione(n_responsabili, n_medici, n_oss, n_infermieri, n_caposala, preferenza_infermieri,
                             medico_responsabile, budget, path)


def csp_info_stroke_unit(path):

    print("Inserire il numero di posti letto disponibili all'interno della terapia intensiva: ")
    bed_number = int(input())
    while bed_number < 1 or bed_number > 10:
        print("Inserire un numero valido di posti letto.")
        bed_number = int(input())

    print("Inserire il budget disponibile per la creazione della terapia intensiva (esclusi oneri): ")
    budget = int(input())
    if 1 <= bed_number <= 3:
        while budget < 310000:
            print("La cifra inserita non è sufficiente per aprire un reparto di terapia intensiva Stoke-Unit con "
                  "il numero di posti letto inseriti.")
            budget = int(input())
    if 4 <= bed_number <= 7:
        while budget < 510000:
            print("La cifra inserita non è sufficiente per aprire un reparto di terapia intensiva Stroke-Unit con "
                  "il numero di posti letto inseriti.")
            budget = int(input())
    if 8 <= bed_number <= 10:
        while budget < 650000:
            print("La cifra inserita non è sufficiente per aprire un reparto di terapia intensiva Stroke-Unit con "
                  "il numero di posti letto inseriti.")
            budget = int(input())

    preferenza_infermieri = scelta_infermieri()
    if not preferenza_infermieri == 2:
        medico_responsabile = scelta_medico()
        if not medico_responsabile == 2:

            n_responsabili = 0
            n_medici = 0
            n_oss = 0
            n_infermieri = 0
            n_caposala = 0

            if 1 <= bed_number <= 3:
                n_responsabili = 1
                n_medici = 1
                n_oss = 1
                n_infermieri = 5
            if 4 <= bed_number <= 7:
                n_responsabili = 1
                n_medici = 2
                n_oss = 1
                n_infermieri = 10
            if 8 <= bed_number <= 10:
                n_responsabili = 1
                n_medici = 3
                n_caposala = 1
                n_oss = 1
                n_infermieri = 13

            print("Avvio ricerca...")
            csp_stroke_unit(n_responsabili, n_medici, n_oss, n_infermieri, n_caposala, preferenza_infermieri,
                            medico_responsabile, budget, path)


def csp_info_dialisi(path):

    print("Inserire il numero di posti letto disponibili all'interno della terapia intensiva: ")
    bed_number = int(input())
    while bed_number < 1 or bed_number > 10:
        print("Inserire un numero valido di posti letto.")
        bed_number = int(input())

    print("Inserire il budget disponibile per la creazione della terapia intensiva (esclusi oneri): ")
    budget = int(input())
    if 1 <= bed_number <= 3:
        while budget < 232000:
            print("La cifra inserita non è sufficiente per aprire un reparto di terapia intensiva Dialisi con "
                  "il numero di posti letto inseriti.")
            budget = int(input())
    if 4 <= bed_number <= 7:
        while budget < 432000:
            print("La cifra inserita non è sufficiente per aprire un reparto di terapia intensiva Dialisi con "
                  "il numero di posti letto inseriti.")
            budget = int(input())
    if 8 <= bed_number <= 10:
        while budget < 545000:
            print("La cifra inserita non è sufficiente per aprire un reparto di terapia intensiva Dialisi con "
                  "il numero di posti letto inseriti.")
            budget = int(input())

    preferenza_infermieri = scelta_infermieri()
    if not preferenza_infermieri == 2:
        medico_responsabile = scelta_medico()
        if not medico_responsabile == 2:

            n_responsabili = 0
            n_medici = 0
            n_oss = 0
            n_infermieri = 0
            n_caposala = 0

            if 1 <= bed_number <= 3:
                n_responsabili = 1
                n_medici = 1
                n_oss = 0
                n_infermieri = 3
            if 4 <= bed_number <= 7:
                n_responsabili = 1
                n_medici = 2
                n_oss = 0
                n_infermieri = 8
            if 8 <= bed_number <= 10:
                n_responsabili = 1
                n_medici = 3
                n_caposala = 1
                n_oss = 0
                n_infermieri = 10

            print("Avvio ricerca...")
            csp_dialisi(n_responsabili, n_medici, n_oss, n_infermieri, n_caposala,
                        preferenza_infermieri, medico_responsabile, budget, path)


def csp_info_respiratoria(path):

    print("Inserire il numero di posti letto disponibili all'interno della terapia intensiva: ")
    bed_number = int(input())
    while bed_number < 1 or bed_number > 10:
        print("Inserire un numero valido di posti letto.")
        bed_number = int(input())

    print("Inserire il budget disponibile per la creazione della terapia intensiva (esclusi oneri): ")
    budget = int(input())
    if 1 <= bed_number <= 3:
        while budget < 310000:
            print("La cifra inserita non è sufficiente per aprire un reparto di terapia intensiva Respiratoria con "
                  "il numero di posti letto inseriti.")
            budget = int(input())
    if 4 <= bed_number <= 7:
        while budget < 510000:
            print("La cifra inserita non è sufficiente per aprire un reparto di terapia intensiva Respiratoria con "
                  "il numero di posti letto inseriti.")
            budget = int(input())
    if 8 <= bed_number <= 10:
        while budget < 650000:
            print("La cifra inserita non è sufficiente per aprire un reparto di terapia intensiva Respiratoria con "
                  "il numero di posti letto inseriti.")
            budget = int(input())

    preferenza_infermieri = scelta_infermieri()
    if not preferenza_infermieri == 2:
        medico_responsabile = scelta_medico()
        if not medico_responsabile == 2:

            n_responsabili = 0
            n_medici = 0
            n_oss = 0
            n_infermieri = 0
            n_caposala = 0

            if 1 <= bed_number <= 3:
                n_responsabili = 1
                n_medici = 1
                n_oss = 1
                n_infermieri = 5
            if 4 <= bed_number <= 7:
                n_responsabili = 1
                n_medici = 2
                n_oss = 1
                n_infermieri = 10
            if 8 <= bed_number <= 10:
                n_responsabili = 1
                n_medici = 3
                n_caposala = 1
                n_oss = 1
                n_infermieri = 13

            print("Avvio ricerca...")
            csp_respiratoria(n_responsabili, n_medici, n_oss, n_infermieri, n_caposala, preferenza_infermieri,
                             medico_responsabile, budget, path)


def csp_info_utin(path):

    print("Inserire il numero di posti letto disponibili all'interno della terapia intensiva: ")
    bed_number = int(input())
    while bed_number < 1 or bed_number > 10:
        print("Inserire un numero valido di posti letto.")
        bed_number = int(input())

    print("Inserire il budget disponibile per la creazione della terapia intensiva (esclusi oneri): ")
    budget = int(input())
    if 1 <= bed_number <= 3:
        while budget < 286000:
            print("La cifra inserita non è sufficiente per aprire un reparto di terapia intensiva UTIC con "
                  "il numero di posti letto inseriti.")
            budget = int(input())
    if 4 <= bed_number <= 7:
        while budget < 486000:
            print("La cifra inserita non è sufficiente per aprire un reparto di terapia intensiva UTIC con "
                  "il numero di posti letto inseriti.")
            budget = int(input())
    if 8 <= bed_number <= 10:
        while budget < 626000:
            print("La cifra inserita non è sufficiente per aprire un reparto di terapia intensiva UTIC con "
                  "il numero di posti letto inseriti.")
            budget = int(input())

    preferenza_infermieri = scelta_infermieri()
    if not preferenza_infermieri == 2:
        medico_responsabile = scelta_medico()
        if not medico_responsabile == 2:

            n_responsabili = 0
            n_medici = 0
            n_oss = 0
            n_infermieri = 0
            n_caposala = 0

            if 1 <= bed_number <= 3:
                n_responsabili = 1
                n_medici = 1
                n_oss = 0
                n_infermieri = 5
            if 4 <= bed_number <= 7:
                n_responsabili = 1
                n_medici = 2
                n_oss = 0
                n_infermieri = 10
            if 8 <= bed_number <= 10:
                n_responsabili = 1
                n_medici = 3
                n_caposala = 1
                n_oss = 0
                n_infermieri = 13

            print("Avvio ricerca...")
            csp_utin(n_responsabili, n_medici, n_oss, n_infermieri, n_caposala,
                     preferenza_infermieri, medico_responsabile, budget, path)


def csp_utic(n_responsabili, n_medici, n_oss, n_infermieri, n_caposala, preferenza_infermieri,
             medico_responsabile, budget, path):

    n_personale = n_responsabili + n_medici + n_oss + n_infermieri + n_caposala
    csp_type = 1
    limitrofi_ba = [0, 1]
    spec_utic = ["Cardioangiopatie", "Angiologia", "Fisiopatologia cardiocircolatoria/ cardiovascolare",
                 "Malattie cardiovascolari", "Cardiologia e malattie dei vasi"]

    problem_utic = def_csp_utic()
    lista_temp, budget = csp_responsabili(csp_type, n_responsabili, medico_responsabile,
                                          spec_utic, problem_utic, budget)
    lista_personale = [lista_temp]

    problem_utic = def_csp_utic()
    lista_temp, budget = csp_medici(csp_type, n_medici, spec_utic, problem_utic, budget)
    lista_personale.append(lista_temp)

    problem_utic = def_csp_utic()
    lista_temp, budget = csp_oss(csp_type, n_oss, problem_utic, budget)
    lista_personale.append(lista_temp)

    problem_utic = def_csp_utic()
    lista_temp, budget = csp_infermieri(csp_type, n_infermieri, preferenza_infermieri,
                                        limitrofi_ba, problem_utic, budget)
    lista_personale.append(lista_temp)

    problem_utic = def_csp_utic()
    lista_temp, budget = csp_caposala(csp_type, n_caposala, problem_utic, budget)
    lista_personale.append(lista_temp)

    if controlla_lista(lista_personale, n_personale):
        salva_lista(lista_personale, csp_type)
        visualizza_lista(path)
        print()
    else:
        print("Impossibile terminare la il processo di creazione della terapia intensiva. Aumentare il budget.")


def csp_rianimazione(n_responsabili, n_medici, n_oss, n_infermieri, n_caposala, preferenza_infermieri,
                     medico_responsabile, budget, path):

    n_personale = n_responsabili + n_medici + n_oss + n_infermieri + n_caposala
    csp_type = 2
    limitrofi_ba = [0, 1]
    spec_rianimazione = ["Anestesiologia e rianimazione", "Anestesiologia rianimazione e terapia intensiva",
                         "Servizio sanitario d’urgenza ed emergenza", "Terapia del dolore", "Terapia intensiva"]

    problem_rianimazione = def_csp_rianimazione()
    lista_temp, budget = csp_responsabili(csp_type, n_responsabili, medico_responsabile,
                                          spec_rianimazione, problem_rianimazione, budget)
    lista_personale = [lista_temp]

    problem_rianimazione = def_csp_rianimazione()
    lista_temp, budget = csp_medici(csp_type, n_medici, spec_rianimazione, problem_rianimazione, budget)
    lista_personale.append(lista_temp)

    problem_rianimazione = def_csp_rianimazione()
    lista_temp, budget = csp_oss(csp_type, n_oss, problem_rianimazione, budget)
    lista_personale.append(lista_temp)

    problem_rianimazione = def_csp_rianimazione()
    lista_temp, budget = csp_infermieri(csp_type, n_infermieri, preferenza_infermieri, limitrofi_ba,
                                        problem_rianimazione, budget)
    lista_personale.append(lista_temp)

    problem_rianimazione = def_csp_rianimazione()
    lista_temp, budget = csp_caposala(csp_type, n_caposala, problem_rianimazione, budget)
    lista_personale.append(lista_temp)

    if controlla_lista(lista_personale, n_personale):
        salva_lista(lista_personale, csp_type)
        visualizza_lista(path)
    else:
        print("Impossibile terminare la terapia. Aumentare il budget")


def csp_stroke_unit(n_responsabili, n_medici, n_oss, n_infermieri, n_caposala, preferenza_infermieri,
                    medico_responsabile, budget, path):

    n_personale = n_responsabili + n_medici + n_oss + n_infermieri + n_caposala
    csp_type = 3
    limitrofi_ba = [0, 1]
    spec_stroke_unit = ["Neurofisiologia clinica", "Neurologia d’urgenza", "Semeiotica neurologica",
                        "Terapia neurologica"]

    problem_stroke_unit = def_csp_stroke_unit()
    lista_temp, budget = csp_responsabili(csp_type, n_responsabili, medico_responsabile,
                                          spec_stroke_unit, problem_stroke_unit, budget)
    lista_personale = [lista_temp]

    problem_stroke_unit = def_csp_stroke_unit()
    lista_temp, budget = csp_medici(csp_type, n_medici, spec_stroke_unit, problem_stroke_unit, budget)
    lista_personale.append(lista_temp)

    problem_stroke_unit = def_csp_stroke_unit()
    lista_temp, budget = csp_oss(csp_type, n_oss, problem_stroke_unit, budget)
    lista_personale.append(lista_temp)

    problem_stroke_unit = def_csp_stroke_unit()
    lista_temp, budget = csp_infermieri(csp_type, n_infermieri, preferenza_infermieri,
                                        limitrofi_ba, problem_stroke_unit, budget)
    lista_personale.append(lista_temp)

    problem_stroke_unit = def_csp_stroke_unit()
    lista_temp, budget = csp_caposala(csp_type, n_caposala, problem_stroke_unit, budget)
    lista_personale.append(lista_temp)

    if controlla_lista(lista_personale, n_personale):
        salva_lista(lista_personale, csp_type)
        visualizza_lista(path)
    else:
        print("Impossibile terminare la terapia. Aumentare il budget")


def csp_dialisi(n_responsabili, n_medici, n_oss, n_infermieri, n_caposala, preferenza_infermieri,
                medico_responsabile, budget, path):

    n_personale = n_responsabili + n_medici + n_oss + n_infermieri + n_caposala
    csp_type = 4
    limitrofi_ba = [0, 1]
    spec_dialisi = ["Emodialisi", "Malattie del rene del sangue e del ricambio", "Nefrologia e dialisi"]

    problem_dialisi = def_csp_dialisi()
    lista_temp, budget = csp_responsabili(csp_type, n_responsabili, medico_responsabile,
                                          spec_dialisi, problem_dialisi, budget)
    lista_personale = [lista_temp]

    problem_dialisi = def_csp_dialisi()
    lista_temp, budget = csp_medici(csp_type, n_medici, spec_dialisi, problem_dialisi, budget)
    lista_personale.append(lista_temp)

    problem_dialisi = def_csp_dialisi()
    lista_temp, budget = csp_oss(csp_type, n_oss, problem_dialisi, budget)
    lista_personale.append(lista_temp)

    problem_dialisi = def_csp_dialisi()
    lista_temp, budget = csp_infermieri(csp_type, n_infermieri, preferenza_infermieri,
                                        limitrofi_ba, problem_dialisi, budget)
    lista_personale.append(lista_temp)

    problem_dialisi = def_csp_dialisi()
    lista_temp, budget = csp_caposala(csp_type, n_caposala, problem_dialisi, budget)
    lista_personale.append(lista_temp)

    if controlla_lista(lista_personale, n_personale):
        salva_lista(lista_personale, csp_type)
        visualizza_lista(path)
    else:
        print("Impossibile terminare la terapia. Aumentare il budget")


def csp_respiratoria(n_responsabili, n_medici, n_oss, n_infermieri, n_caposala, preferenza_infermieri,
                     medico_responsabile, budget, path):

    n_personale = n_responsabili + n_medici + n_oss + n_infermieri + n_caposala
    csp_type = 5
    limitrofi_ba = [0, 1]
    spec_respiratoria = ["Fisiopatologia respiratoria", "Malattie dell’apparato respiratorio", "Pneumologia",
                         "Tisiologia"]

    problem_respiratoria = def_csp_respiratoria()
    lista_temp, budget = csp_responsabili(csp_type, n_responsabili, medico_responsabile,
                                          spec_respiratoria, problem_respiratoria, budget)
    lista_personale = [lista_temp]

    problem_respiratoria = def_csp_respiratoria()
    lista_temp, budget = csp_medici(csp_type, n_medici, spec_respiratoria, problem_respiratoria, budget)
    lista_personale.append(lista_temp)

    problem_respiratoria = def_csp_respiratoria()
    lista_temp, budget = csp_oss(csp_type, n_oss, problem_respiratoria, budget)
    lista_personale.append(lista_temp)

    problem_respiratoria = def_csp_respiratoria()
    lista_temp, budget = csp_infermieri(csp_type, n_infermieri, preferenza_infermieri,
                                        limitrofi_ba, problem_respiratoria, budget)
    lista_personale.append(lista_temp)

    problem_respiratoria = def_csp_respiratoria()
    lista_temp, budget = csp_caposala(csp_type, n_caposala, problem_respiratoria, budget)
    lista_personale.append(lista_temp)

    if controlla_lista(lista_personale, n_personale):
        salva_lista(lista_personale, csp_type)
        visualizza_lista(path)
    else:
        print("Impossibile terminare la terapia. Aumentare il budget")


def csp_utin(n_responsabili, n_medici, n_oss, n_infermieri, n_caposala, preferenza_infermieri,
             medico_responsabile, budget, path):

    n_personale = n_responsabili + n_medici + n_oss + n_infermieri + n_caposala
    csp_type = 6
    limitrofi_ba = [0, 1]
    spec_utin = ["Patologia neonatale", "Terapia intensiva neonatale"]

    problem_utin = def_csp_utin()
    lista_temp, budget = csp_responsabili(csp_type, n_responsabili, medico_responsabile,
                                          spec_utin, problem_utin, budget)
    lista_personale = [lista_temp]

    problem_utin = def_csp_utin()
    lista_temp, budget = csp_medici(csp_type, n_medici, spec_utin, problem_utin, budget)
    lista_personale.append(lista_temp)

    problem_utin = def_csp_utin()
    lista_temp, budget = csp_oss(csp_type, n_oss, problem_utin, budget)
    lista_personale.append(lista_temp)

    problem_utin = def_csp_utin()
    lista_temp, budget = csp_infermieri(csp_type, n_infermieri, preferenza_infermieri,
                                        limitrofi_ba, problem_utin, budget)
    lista_personale.append(lista_temp)

    problem_utin = def_csp_utin()
    lista_temp, budget = csp_caposala(csp_type, n_caposala, problem_utin, budget)
    lista_personale.append(lista_temp)

    if controlla_lista(lista_personale, n_personale):
        salva_lista(lista_personale, csp_type)
        visualizza_lista(path)
    else:
        print("Impossibile terminare la terapia. Aumentare il budget.")


def def_csp_utic():

    problem_utic = Problem()
    problem_utic.addVariable("qualifica", ["OSS", "infermiere", "caposala", "medico"])
    problem_utic.addVariable("classificazione", ["incarico professionale",
                                                 "incarico di responsabile di struttura semplice",
                                                 "incarico di responsabile di struttura complessa", "no"])
    problem_utic.addVariable("specializzazione", ["Cardioangiopatie", "Cardiologia e malattie dei vasi",
                                                  "Cardiologia e reumatologia", "Cardiologia pediatrica",
                                                  "Fisiopatologia cardiocircolatoria/ cardiovascolare",
                                                  "Malattie cardiovascolari", "Malattie cardiovascolari e reumatiche",
                                                  "Semeiotica cardiovascolare", "Allergologia e immunologia clinica",
                                                  "Angiologia", "Geriatria", "Malattie metaboliche e Diabetologia",
                                                  "Malattie dell’apparato respiratorio",
                                                  "Medicina e Chirurgia d’accettazione e d’urgenza", "Medicina Interna",
                                                  "Medicina dello Sport", "Reumatologia", "no"])
    problem_utic.addVariable("anzianita", range(0, 44))
    problem_utic.addVariable("limitazioni", [0, 1])
    problem_utic.addVariable("titolo", ["diploma operatore socio-sanitario",
                                        "laurea scienze infermieristiche", "laurea magistrale infermieristica",
                                        "laurea medicina"])
    problem_utic.addVariable("limitrofo", [0, 1])

    return problem_utic


def def_csp_rianimazione():

    problem_rianimazione = Problem()
    problem_rianimazione.addVariable("qualifica", ["OSS", "infermiere", "caposala", "medico"])
    problem_rianimazione.addVariable("classificazione", ["incarico professionale",
                                                         "incarico di responsabile di struttura semplice",
                                                         "incarico di responsabile di struttura complessa", "no"])
    problem_rianimazione.addVariable("specializzazione", ["Anestesia", "Anestesiologia",
                                                          "Anestesiologia e rianimazione",
                                                          "Anestesiologia generale e speciale odontostomatologica",
                                                          "Anestesiologia rianimazione e terapia intensiva",
                                                          "Medicina subacquea ed iperbarica",
                                                          "Servizio sanitario d’urgenza ed emergenza",
                                                          "Terapia del dolore", "Terapia intensiva", "no"])
    problem_rianimazione.addVariable("anzianita", range(0, 44))
    problem_rianimazione.addVariable("limitazioni", [0, 1])
    problem_rianimazione.addVariable("titolo", ["diploma operatore socio-sanitario",
                                                "laurea scienze infermieristiche", "laurea magistrale infermieristica",
                                                "laurea medicina"])
    problem_rianimazione.addVariable("limitrofo", [0, 1])

    return problem_rianimazione


def def_csp_stroke_unit():

    problem_stroke_unit = Problem()
    problem_stroke_unit.addVariable("qualifica", ["OSS", "infermiere", "caposala", "medico"])
    problem_stroke_unit.addVariable("classificazione", ["incarico professionale",
                                                        "incarico di responsabile di struttura semplice",
                                                        "incarico di responsabile di struttura complessa", "no"])
    problem_stroke_unit.addVariable("specializzazione", ["Clinica neurologica", "Malattie nervose",
                                                         "Malattie nervose e mentali", "Neurofisiologia clinica",
                                                         "Neurologia d’urgenza", "Neurologia e psichiatria",
                                                         "Neuropsichiatria", "Neuroriabilitazione",
                                                         "Semeiotica neurologica",
                                                         "Terapia neurologica",
                                                         "Medicina fisica e della riabilitazione",
                                                         "Neurofisiologia clinica", "Neurofisiopatologia",
                                                         "Neuropatologia",
                                                         "Neuropsichiatria infantile", "Neuroradiologia",
                                                         "Psichiatria", "no"])
    problem_stroke_unit.addVariable("anzianita", range(0, 44))
    problem_stroke_unit.addVariable("limitazioni", [0, 1])
    problem_stroke_unit.addVariable("titolo", ["diploma operatore socio-sanitario",
                                               "laurea scienze infermieristiche", "laurea magistrale infermieristica",
                                               "laurea medicina"])
    problem_stroke_unit.addVariable("limitrofo", [0, 1])

    return problem_stroke_unit


def def_csp_dialisi():

    problem_dialisi = Problem()
    problem_dialisi.addVariable("qualifica", ["OSS", "infermiere", "caposala", "medico"])
    problem_dialisi.addVariable("classificazione", ["incarico professionale",
                                                    "incarico di responsabile di struttura semplice",
                                                    "incarico di responsabile di struttura complessa", "no"])
    problem_dialisi.addVariable("specializzazione", ["Emodialisi",
                                                     "Malattie del rene del sangue e del ricambio",
                                                     "Nefrologia e dialisi", "Nefrologia medica",
                                                     "Nefrologia pediatrica",
                                                     "Allergologia ed Immunologia Clinica Geriatria",
                                                     "Medicina Interna", "Urologia", "no"])
    problem_dialisi.addVariable("anzianita", range(0, 44))
    problem_dialisi.addVariable("limitazioni", [0, 1])
    problem_dialisi.addVariable("titolo", ["diploma operatore socio-sanitario",
                                           "laurea scienze infermieristiche", "laurea magistrale infermieristica",
                                           "laurea medicina"])
    problem_dialisi.addVariable("limitrofo", [0, 1])

    return problem_dialisi


def def_csp_respiratoria():

    problem_respiratoria = Problem()
    problem_respiratoria.addVariable("qualifica", ["OSS", "infermiere", "caposala", "medico"])
    problem_respiratoria.addVariable("classificazione", ["incarico professionale",
                                                         "incarico di responsabile di struttura semplice",
                                                         "incarico di responsabile di struttura complessa", "no"])
    problem_respiratoria.addVariable("specializzazione", ["Fisiopatologia e fisiochinesiterapia respiratoria",
                                                          "Fisiopatologia respiratoria",
                                                          "Malattie dell’apparato respiratorio", "Pneumologia",
                                                          "Tisiologia", "Allergologia ed Immunologia Clinica",
                                                          "Cardiologia", "Geriatria", "Malattie Infettive",
                                                          "Medicina e Chirurgia di Accettazione ed Urgenza",
                                                          "Medicina Interna", "Medicina dello Sport",
                                                          "Oncologia", "no"])
    problem_respiratoria.addVariable("anzianita", range(0, 44))
    problem_respiratoria.addVariable("limitazioni", [0, 1])
    problem_respiratoria.addVariable("titolo", ["diploma operatore socio-sanitario",
                                                "laurea scienze infermieristiche", "laurea magistrale infermieristica",
                                                "laurea medicina"])
    problem_respiratoria.addVariable("limitrofo", [0, 1])

    return problem_respiratoria


def def_csp_utin():

    problem_utin = Problem()
    problem_utin.addVariable("qualifica", ["OSS", "infermiere", "caposala", "medico"])
    problem_utin.addVariable("classificazione", ["incarico professionale",
                                                 "incarico di responsabile di struttura semplice",
                                                 "incarico di responsabile di struttura complessa", "no"])
    problem_utin.addVariable("specializzazione", ["Clinica pediatrica", "Patologia neonatale",
                                                  "Pediatria", "Pediatria e puericultura",
                                                  "Pediatria preventiva e puericultura",
                                                  "Pediatria preventiva e sociale", "Pediatria sociale e puericultura",
                                                  "Puericultura", "Puericultura e dietetica infantile",
                                                  "Puericultura ed igiene infantile",
                                                  "Puericultura dietetica infantile "
                                                  "ed assistenza sociale dell’infanzia",
                                                  "Terapia intensiva neonatale", "Pediatria", "no"])
    problem_utin.addVariable("anzianita", range(0, 44))
    problem_utin.addVariable("limitazioni", [0, 1])
    problem_utin.addVariable("sesso", [0, 1])
    problem_utin.addVariable("titolo", ["diploma operatore socio-sanitario",
                                        "laurea scienze infermieristiche", "laurea magistrale infermieristica",
                                        "laurea medicina"])
    problem_utin.addVariable("limitrofo", [0, 1])

    return problem_utin


def csp_responsabili(csp_type, n_responsabili, medico_responsabile, spec, csp_problem, budget):

    role = 1
    if not n_responsabili == 0:
        if medico_responsabile == 1:
            csp_problem.addConstraint(lambda qualifica, titolo, specializzazione, anzianita, classificazione:
                                      qualifica == "medico"
                                      and titolo == "laurea medicina"
                                      and specializzazione in spec
                                      and anzianita in range(0, 44)
                                      and classificazione == "incarico di responsabile di struttura semplice",
                                      ("qualifica", "titolo", "specializzazione", "anzianita", "classificazione"))
        else:
            csp_problem.addConstraint(lambda qualifica, titolo, specializzazione, anzianita, classificazione:
                                      qualifica == "medico"
                                      and titolo == "laurea medicina"
                                      and specializzazione in spec
                                      and anzianita in range(0, 44)
                                      and classificazione == "incarico di responsabile di struttura complessa",
                                      ("qualifica", "titolo", "specializzazione", "anzianita", "classificazione"))
    else:
        print("Non vi sono medici responsabili all'interno della terapia intensiva selezionata\n")

    csp_problem.setSolver(BacktrackingSolver())

    solutions_list = csp_problem.getSolutions()

    csp_problem.reset()
    print("Inizio ricerca responsabili...")
    risultati, budget = csp_search(solutions_list, csp_type, role, n_responsabili, budget)
    return risultati, budget


def csp_medici(csp_type, n_medici, spec, csp_problem, budget):

    role = 2
    if not n_medici == 0:
        csp_problem.addConstraint(lambda qualifica, titolo, specializzazione, classificazione:
                                  qualifica == "medico"
                                  and titolo == "laurea medicina"
                                  and specializzazione in spec
                                  and classificazione == "incarico professionale",
                                  ("qualifica", "titolo", "specializzazione", "classificazione"))
    else:
        print("Non vi sono medici all'interno della terapia intensiva selezionata\n")

    csp_problem.setSolver(BacktrackingSolver())

    solutions_list = csp_problem.getSolutions()

    csp_problem.reset()
    print("Inizio ricerca medici...")
    return csp_search(solutions_list, csp_type, role, n_medici, budget)


def csp_oss(csp_type, n_oss, csp_problem, budget):

    role = 3
    if not n_oss == 0:
        csp_problem.addConstraint(lambda qualifica, titolo, limitazioni:
                                  qualifica == "OSS"
                                  and titolo == "diploma operatore socio-sanitario"
                                  and limitazioni == 0, ("qualifica", "titolo", "limitazioni"))

        csp_problem.setSolver(BacktrackingSolver())
        solutions_list = csp_problem.getSolutions()
        csp_problem.reset()
        print("Inizio ricerca OSS...")
        return csp_search(solutions_list, csp_type, role, n_oss, budget)
    else:
        print("Non vi sono operatori socio-sanitari all'interno della terapia intensiva selezionata\n")
        return [], budget


def csp_infermieri(csp_type, n_infermieri, preferenza_infermieri, limitrofi_ba, csp_problem, budget):

    role = 4
    if csp_type == 4:
        if not n_infermieri == 0:
            if preferenza_infermieri == 1:
                csp_problem.addConstraint(lambda qualifica, titolo, limitazioni, anzianita:
                                          qualifica == "infermiere"
                                          and titolo == "laurea scienze infermieristiche"
                                          and limitazioni == 0
                                          and anzianita in range(0, 20),
                                          ("qualifica", "titolo", "limitazioni", "anzianita"))
            else:
                csp_problem.addConstraint(lambda qualifica, titolo, limitazioni, anzianita:
                                          qualifica == "infermiere"
                                          and titolo == "laurea scienze infermieristiche"
                                          and limitazioni == 0
                                          and anzianita in range(20, 44),
                                          ("qualifica", "titolo", "limitazioni", "anzianita"))
        else:
            print("Non vi sono infermieri all'interno della terapia intensiva selezionata\n")

    elif csp_type == 6:
        if not n_infermieri == 0:
            if preferenza_infermieri == 1:
                csp_problem.addConstraint(lambda sesso, limitrofo, qualifica, titolo, limitazioni, anzianita:
                                          sesso == 0
                                          and limitrofo in limitrofi_ba
                                          and qualifica == "infermiere"
                                          and titolo == "laurea scienze infermieristiche"
                                          and limitazioni == 0
                                          and anzianita in range(0, 20),
                                          ("sesso", "limitrofo", "qualifica", "titolo", "limitazioni", "anzianita"))
            else:
                csp_problem.addConstraint(lambda sesso, limitrofo, qualifica, titolo, limitazioni, anzianita:
                                          sesso == 0
                                          and limitrofo in limitrofi_ba
                                          and qualifica == "infermiere"
                                          and titolo == "laurea scienze infermieristiche"
                                          and limitazioni == 0
                                          and anzianita in range(20, 44),
                                          ("sesso", "limitrofo", "qualifica", "titolo", "limitazioni", "anzianita"))
        else:
            print("Non vi sono infermieri all'interno della terapia intensiva selezionata\n")

    else:
        if not n_infermieri == 0:
            if preferenza_infermieri == 1:
                csp_problem.addConstraint(lambda limitrofo, qualifica, titolo, limitazioni, anzianita:
                                          limitrofo in limitrofi_ba
                                          and qualifica == "infermiere"
                                          and titolo == "laurea scienze infermieristiche"
                                          and limitazioni == 0
                                          and anzianita in range(0, 20),
                                          ("limitrofo", "qualifica", "titolo", "limitazioni", "anzianita"))
            else:
                csp_problem.addConstraint(lambda limitrofo, qualifica, titolo, limitazioni, anzianita:
                                          limitrofo in limitrofi_ba
                                          and qualifica == "infermiere"
                                          and titolo == "laurea scienze infermieristiche"
                                          and limitazioni == 0
                                          and anzianita in range(20, 44),
                                          ("limitrofo", "qualifica", "titolo", "limitazioni", "anzianita"))
        else:
            print("Non vi sono infermieri all'interno della terapia intensiva selezionata\n")

    csp_problem.setSolver(BacktrackingSolver())

    solutions_list = csp_problem.getSolutions()

    csp_problem.reset()
    print("Inizio ricerca infermieri...")
    return csp_search(solutions_list, csp_type, role, n_infermieri, budget)


def csp_caposala(csp_type, n_caposala, csp_problem, budget):

    role = 5
    if not n_caposala == 0:
        '''csp_problem.addConstraint(lambda titolo, qualifica:
                                  titolo == "laurea magistrale infermieristica" and
                                  qualifica == "caposala" or qualifica == "infermiere", ("titolo", "qualifica"))'''
        csp_problem.addConstraint(lambda titolo, qualifica, specializzazione, classificazione:
                                  titolo == "laurea magistrale infermieristica" and
                                  qualifica == "caposala" or qualifica == "infermiere" and
                                  specializzazione == "no" and
                                  classificazione == "no",
                                  ("titolo", "qualifica", "specializzazione", "classificazione"))

        csp_problem.setSolver(BacktrackingSolver())
        solutions_list = csp_problem.getSolutions()
        csp_problem.reset()
        print("Inizio ricerca caposala...")
        return csp_search(solutions_list, csp_type, role, n_caposala, budget)
    else:
        print("Non vi sono caposala all'interno della terapia intensiva selezionata\n")
        return [], budget


def csp_search(solutions_list, csp_type, role, n_personale, budget):

    dataset_path = '../dataset/datasetCSP.csv'
    reader = pd.read_csv(dataset_path)
    personell_list = []
    matricole_assegnate = []
    lista_criteri = analizza_lista(solutions_list)
    n = 0
    for i in range(len(lista_criteri)):
        if role == 1:
            for index, row in reader.iterrows():
                if (
                    row['qualifica'] in lista_criteri[i] and
                    row['anzianita'] == lista_criteri[i][4] and
                    row['classificazione'] in lista_criteri[i] and
                    row['specializzazione'] in lista_criteri[i] and
                    row['assegnato'] == 0 and
                    row['matricola'] not in matricole_assegnate and
                    budget >= row['stipendio totale']
                ):
                    matricole_assegnate.append(row['matricola'])
                    row['assegnato'] = 1
                    budget = budget - row['stipendio totale']
                    personell_list.append(row)
                    n = n + 1
                if n == n_personale:
                    print("Ricerca completata.\n")
                    return personell_list, budget

        if role == 2:
            for index, row in reader.iterrows():
                if (
                    row['qualifica'] in lista_criteri[i] and
                    row['classificazione'] in lista_criteri[i] and
                    row['specializzazione'] in lista_criteri[i] and
                    row['assegnato'] == 0 and
                    row['matricola'] not in matricole_assegnate and
                    budget >= row['stipendio totale']
                ):
                    matricole_assegnate.append(row['matricola'])
                    row['assegnato'] = 1
                    budget = budget - row['stipendio totale']
                    personell_list.append(row)
                    n = n + 1
                if n == n_personale:
                    print("Ricerca completata.\n")
                    return personell_list, budget

        if role == 3:
            for index, row in reader.iterrows():
                if (
                        row['qualifica'] in lista_criteri[i] and
                        row['limitazioni lavorative'] == lista_criteri[i][0] and
                        row['assegnato'] == 0 and
                        row['matricola'] not in matricole_assegnate and
                        budget >= row['stipendio totale']
                ):
                    matricole_assegnate.append(row['matricola'])
                    personell_list.append(row)
                    n = n + 1
                    budget = budget - row['stipendio totale']
                    row['assegnato'] = 1
                    if n == n_personale:
                        print("Ricerca completata.\n")
                        return personell_list, budget

        if role == 4:
            if csp_type == 4:
                for index, row in reader.iterrows():
                    if (
                            row['qualifica'] in lista_criteri[i] and
                            row['anzianita'] == lista_criteri[i][3] and
                            row['limitazioni lavorative'] == lista_criteri[i][0] and
                            row['assegnato'] == 0 and
                            row['matricola'] not in matricole_assegnate and
                            budget >= row['stipendio totale']
                    ):
                        matricole_assegnate.append(row['matricola'])
                        personell_list.append(row)
                        n = n + 1
                        budget = budget - row['stipendio totale']
                        row['assegnato'] = 1
                        if n == n_personale:
                            print("Ricerca completata.\n")
                            return personell_list, budget

            if csp_type == 6:
                for index, row in reader.iterrows():
                    if (
                            row['qualifica'] in lista_criteri[i] and
                            row['limitrofo'] == lista_criteri[i][1] and
                            row['limitazioni lavorative'] == lista_criteri[i][0] and
                            row['anzianita'] == lista_criteri[i][5] and
                            row['sesso'] == lista_criteri[i][2] and
                            row['assegnato'] == 0 and
                            row['matricola'] not in matricole_assegnate and
                            budget >= row['stipendio totale']
                    ):
                        matricole_assegnate.append(row['matricola'])
                        personell_list.append(row)
                        n = n + 1
                        budget = budget - row['stipendio totale']
                        row['assegnato'] = 1
                        if n == n_personale:
                            print("Ricerca completata.\n")
                            return personell_list, budget

            else:
                for index, row in reader.iterrows():
                    if (
                            row['qualifica'] in lista_criteri[i] and
                            row['limitrofo'] == lista_criteri[i][1] and
                            row['limitazioni lavorative'] == lista_criteri[i][0] and
                            row['anzianita'] == lista_criteri[i][4] and
                            row['assegnato'] == 0 and
                            row['matricola'] not in matricole_assegnate and
                            budget >= row['stipendio totale']
                    ):
                        matricole_assegnate.append(row['matricola'])
                        personell_list.append(row)
                        n = n + 1
                        budget = budget - row['stipendio totale']
                        row['assegnato'] = 1
                        if n == n_personale:
                            print("Ricerca completata.\n")
                            return personell_list, budget

        if role == 5:
            for index, row in reader.iterrows():
                if n <= n_personale:
                    if (
                            row['qualifica'] in lista_criteri[i] and
                            row['titolo'] in lista_criteri[i] and
                            row['assegnato'] == 0 and
                            row['matricola'] not in matricole_assegnate and
                            budget >= row['stipendio totale']
                    ):
                        matricole_assegnate.append(row['matricola'])
                        personell_list.append(row)
                        n = n + 1
                        budget = budget - row['stipendio totale']
                        row['assegnato'] = 1
                        if n == n_personale:
                            print("Ricerca completata.\n")
                            return personell_list, budget
    if not n == n_personale:
        return [], budget


def vedi_risultati():

    flag = True

    while flag:

        print("\n============ Visualizzazione reparti di terapia intensiva ============")
        print("1. UNITA' TERAPIA INTENSIVA CORONARICA (UTIC)")
        print("2. RIANIMAZIONE E RIANIMAZIONE POST-OPERATORIA")
        print("3. STROKE-UNIT")
        print("4. DIALISI")
        print("5. TERAPIA INSTENSIVA RESPIRATORIA")
        print("6. UNITA' TERAPIA INTENSIVA NEONATALE (UTIN)")
        print("0. Torna indietro.")
        print("Inserire il numero corrispondente al reparto che si desidera visualizzare il risultato creato: ")

        terapia = input()

        match terapia:
            case "1":
                path = "../CSP/results/csp_utic.txt"
                if os.path.exists(path):
                    visualizza_lista(path)
                else:
                    print("\nNon è stata ancora creata la terapia intensiva selezionata.")

            case "2":
                path = "../CSP/results/csp_rianimazione.txt"
                if os.path.exists(path):
                    visualizza_lista(path)
                else:
                    print("\nNon è stata ancora creata la terapia intensiva selezionata.")

            case "3":
                path = "../CSP/results/csp_stroke_unit.txt"
                if os.path.exists(path):
                    visualizza_lista(path)
                else:
                    print("\nNon è stata ancora creata la terapia intensiva selezionata.")

            case "4":
                path = "../CSP/results/csp_dialisi.txt"
                if os.path.exists(path):
                    visualizza_lista(path)
                else:
                    print("\nNon è stata ancora creata la terapia intensiva selezionata.")

            case "5":
                path = "../CSP/results/csp_respiratoria.txt"
                if os.path.exists(path):
                    visualizza_lista(path)
                else:
                    print("\nNon è stata ancora creata la terapia intensiva selezionata.")

            case "6":
                path = "../CSP/results/csp_utin.txt"
                if os.path.exists(path):
                    visualizza_lista(path)
                else:
                    print("\nNon è stata ancora creata la terapia intensiva selezionata.")

            case "0":
                print("Ritorno indietro...")
                flag = False

            case _:
                print("Inserire un numero valido")


def analizza_lista(lista):

    criteri_ricerca = []
    for dizionario in lista:
        riga = []
        for campo, valore in dizionario.items():
            if campo == 'anzianità' or campo == 'sesso' or campo == 'limitazioni':
                riga.append(int(valore))
            else:
                riga.append(valore)
        criteri_ricerca.append(riga)
    return criteri_ricerca


def visualizza_lista(path_risultati):

    lista_personale = []
    f = open(path_risultati, "r")
    lista = f.read().replace("['", "").replace("']", "").split("', '")
    f.close()

    with open("../dataset/dataset.csv") as file_obj:
        next(file_obj)
        reader_obj = csv.reader(file_obj)

        for row in reader_obj:
            if row[0] in lista:
                lista_personale.append(row)

    print()
    print(tabulate(lista_personale, headers=["Matricola", "Nome", "Cognome", "Data di nascita", "Sesso",
                                             "Numero di cellulare", "Residenza", "Qualifica", "Titolo",
                                             "Limitazioni lavorative", "Reparto", "Specializzazione", "Anzianità",
                                             "Classificazione", "Stipendio base", "Incremento anzianità",
                                             "Bonus incarico", "Salario totale"]))


def salva_lista(lista, csp_type):

    temp_lista = []
    lista_matricole = []
    flag = False
    for qualifiche in lista:
        for x in qualifiche:
            df = x.to_frame()
            temp_lista.append(str(df.iloc[0]).split(" ")[4].split("\n")[0])

    temp_lista = sorted(temp_lista)
    for x in temp_lista:
        lista_matricole.append(int(x.replace("A", "")))

    match csp_type:
        case 1:
            if not os.path.exists("../CSP/results/csp_utic.txt"):
                with open('../CSP/results/csp_utic.txt', 'w') as f:
                    f.write(str(temp_lista))
                    f.close()
                flag = True

        case 2:
            if not os.path.exists("../CSP/results/csp_rianimazione.txt"):
                with open('../CSP/results/csp_rianimazione.txt', 'w') as f:
                    f.write(str(temp_lista))
                    f.close()
                flag = True

        case 3:
            if not os.path.exists("../CSP/results/csp_stroke_unit.txt"):
                with open('../CSP/results/csp_stroke_unit.txt', 'w') as f:
                    f.write(str(temp_lista))
                    f.close()
                flag = True

        case 4:
            if not os.path.exists("../CSP/results/csp_dialisi.txt"):
                with open('../CSP/results/csp_dialisi.txt', 'w') as f:
                    f.write(str(temp_lista))
                    f.close()
                flag = True
        case 5:
            if not os.path.exists("../CSP/results/csp_respiratoria.txt"):
                with open('../CSP/results/csp_respiratoria.txt', 'w') as f:
                    f.write(str(temp_lista))
                    f.close()
                    f.close()
                flag = True

        case 6:
            if not os.path.exists("../CSP/results/csp_utin.txt"):
                with open('../CSP/results/csp_utin.txt', 'w') as f:
                    f.write(str(temp_lista))
                    f.close()
                flag = True

    if flag:
        df = pd.read_csv("../dataset/datasetCSP.csv")
        for x in lista_matricole:
            df.loc[x-1, 'assegnato'] = 1
        df.to_csv("../dataset/datasetCSP.csv", index=False)


def elimina_terapia(path):

    f = open(path, "r")
    lista = f.read().replace("['", "").replace("']", "").split("', '")
    f.close()

    df = pd.read_csv("../dataset/datasetCSP.csv")
    for x in lista:
        df.loc[int(x.replace("A", ""))-1, 'assegnato'] = 0
    df.to_csv("../dataset/datasetCSP.csv", index=False)

    os.remove(path)


def scelta_eliminazione():

    flag = True
    while flag:
        print("La terapia intensiva selezionata è già presente. Vuoi eliminarla per crearne una nuova?")
        print("1. Si")
        print("2. No")
        scelta = input()
        if scelta == "1":
            return True
        elif scelta == "2":
            print("Non verrà creata una nuova terapia intensiva.")
            return False
        else:
            print("La scelta inserita è errata. Riprova:")


def controlla_lista(lista, n_personale):

    lista_matricole = []
    for qualifiche in lista:
        for x in qualifiche:
            df = x.to_frame()
            lista_matricole.append(str(df.iloc[0]).split(" ")[4].split("\n")[0])

    if len(lista_matricole) == n_personale:
        return True
    else:
        return False


def lista_valori():

    valori_assegnato = []
    for x in range(500):
        valori_assegnato.append(0)
    return valori_assegnato


def trova_limitrofe():

    lista_cap = trova_cap()
    lista_limitrofe = []

    for x in lista_cap:
        if int(x) == 70100 or int(x) in range(70121, 70133):
            lista_limitrofe.append(1)
        else:
            lista_limitrofe.append(0)

    return lista_limitrofe


def crea_colonna_assegnato():

    dataset_path = '../dataset/dataset.csv'
    dataset = pd.read_csv(dataset_path)
    dataset['limitrofo'] = trova_limitrofe()
    dataset['assegnato'] = lista_valori()
    dataset.to_csv("../dataset/datasetCSP.csv", index=False)
