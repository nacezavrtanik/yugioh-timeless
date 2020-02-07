import random
import string
from tabulate import tabulate


# Sporočila napak za uporabo v 'preveri' (spodaj):
napaka1 = 'Ups, prišlo je do napake. Vnesi le 1 ali 2: '
napaka2 = 'Ups, prišlo je do napake. Vnesi ime zmagovalca: '
napaka3 = 'Ime naj vsebuje le črke in presledke.\n{}. igralec: '


# Zahteva določene vrednosti za 'input()':
def preveri(vnos, opcije, napaka, tip):
    if tip == 'ime':
        if vnos.replace(' ','').isalpha():
            return string.capwords(vnos)
        else:
            return(preveri(input(napaka), None, napaka, 'ime'))      
    else:
        vnos = string.capwords(vnos)
        if vnos in opcije:
            return vnos
        else:
            return(preveri(input(napaka), opcije, napaka, None))


# Sestavi in predstavi potek turnirja:
def turnir():

    print('================== *** IME LIGE *** ==================\n')
    print('*** OPIS FORMATOV ***\n')
    print('1 *** Prvi format ***\n2 *** Drugi format ***')
    
    # Kateri decki se bodo igrali:
    decki = [['Normal', 'Dragon', 'Beast', 'Chaos'], ['Warrior', 'Flip', 'Plant', 'Zombie']]
    decki = decki[int(preveri(input('\nKaterega boste igrali? Številka formata: '), ['1', '2'], napaka1, None)) - 1]
    random.shuffle(decki)
    
    print('\n*** TEKST ***\n')

    # Kdo bo igral na turnirju:
    igralci = []
    for i in range(4):
        igralci.append(preveri(input('{}. igralec: '.format(i+1)), None, napaka3.format(i+1), 'ime'))
    random.shuffle(igralci)

    print('\nVeliko zabave pri igranju!')

    # Kdo bo proti komu igral s katerim deckom (vse možnosti):
    matchupi = [[[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]],
                [[0, 1, 3, 2], [0, 1, 3, 2], [1, 0, 2, 3], [1, 0, 2, 3]],
                [[0, 3, 1, 2], [2, 1, 3, 0], [3, 0, 2, 1], [1, 2, 0, 3]],
                [[0, 2, 1, 3], [3, 1, 2, 0], [3, 1, 2, 0], [0, 2, 1, 3]],
                [[0, 2, 3, 1], [3, 1, 0, 2], [1, 3, 2, 0], [2, 0, 1, 3]],
                [[0, 3, 2, 1], [2, 1, 0, 3], [0, 3, 2, 1], [2, 1, 0, 3]],
                [[0, 1, 2, 3], [0, 1, 2, 3], [1, 0, 2, 3], [1, 0, 2, 3]],
                [[0, 1, 3, 2], [0, 1, 3, 2], [0, 1, 2, 3], [0, 1, 2, 3]],
                [[0, 3, 1, 2], [2, 1, 3, 0], [3, 1, 2, 0], [0, 2, 1, 3]],
                [[0, 2, 1, 3], [3, 1, 2, 0], [3, 0, 2, 1], [1, 2, 0, 3]],
                [[0, 2, 3, 1], [3, 1, 0, 2], [0, 3, 2, 1], [2, 1, 0, 3]],
                [[0, 3, 2, 1], [2, 1, 0, 3], [1, 3, 2, 0], [2, 0, 1, 3]],
                [[0, 1, 2, 3], [2, 1, 0, 3], [0, 1, 2, 3], [2, 1, 0, 3]],
                [[0, 1, 3, 2], [2, 1, 3, 0], [1, 0, 2, 3], [1, 2, 0, 3]],
                [[0, 3, 1, 2], [0, 1, 3, 2], [3, 0, 2, 1], [1, 0, 2, 3]],
                [[0, 2, 1, 3], [3, 1, 0, 2], [3, 1, 2, 0], [2, 0, 1, 3]],
                [[0, 2, 3, 1], [3, 1, 2, 0], [1, 3, 2, 0], [0, 2, 1, 3]],
                [[0, 3, 2, 1], [0, 1, 2, 3], [0, 3, 2, 1], [0, 1, 2, 3]],
                [[0, 1, 2, 3], [3, 1, 2, 0], [3, 1, 2, 0], [0, 1, 2, 3]],
                [[0, 1, 3, 2], [3, 1, 0, 2], [1, 3, 2, 0], [1, 0, 2, 3]],
                [[0, 3, 1, 2], [2, 1, 0, 3], [0, 3, 2, 1], [1, 2, 0, 3]],
                [[0, 2, 1, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 2, 1, 3]],
                [[0, 2, 3, 1], [0, 1, 3, 2], [1, 0, 2, 3], [2, 0, 1, 3]],
                [[0, 3, 2, 1], [2, 1, 3, 0], [3, 0, 2, 1], [2, 1, 0, 3]]]
    
    # Kdo bo proti komu igral s katerim deckom (na tem turnirju):
    matchup = random.choice(matchupi)

    # Naključna izbira pairingov v prvih treh rundah (vsak z vsakim):
    pair1_num = [[0, 1, 2, 3], [1, 3, 0, 2], [3, 0, 1, 2]]
    random.shuffle(pair1_num)

    # Pairingi za prve tri runde v obliki za predstavitev s 'tabulate':
    pair1_tab = []
    for i in range(3):
        sez = []
        for j in [0, 2]:
            X = pair1_num[i][j]
            Y = pair1_num[i][j+1]
            sez.append([igralci[X] + ' (' + decki[matchup[X][Y]] + ')', 'VS', igralci[Y] + ' (' + decki[matchup[Y][X]] + ')'])
        pair1_tab.append(sez)
    
    print('\n----------------------PAIRINGI----------------------')

    # Beleži število zmag na igralca:
    zmage = {i : 0 for i in igralci}
    

    # Prikaz pairingov za prve tri runde (vsak z vsakim):
    for i in range(3):
        print('\n{}. runda: \n'.format(i+1))
        print(tabulate(pair1_tab[i], tablefmt='plain'))

        # Prebere imena igralcev v posameznem matchu runde:
        A, B, C, D = [igralci[pair1_num[i][j]] for j in range(4)]

        # Zabeleži zmage:
        zmage[preveri(input('\nKdo je zmagal, {} ali {}? '.format(A,B)), [A, B], napaka2, None)] += 1
        zmage[preveri(input('Kdo je zmagal, {} ali {}? '.format(C,D)), [C, D], napaka2, None)] += 1
        print('----------------------------------------------------')
        

    # Seznam parov (število zmag, igralec), urejen padajoče po zmagah (po treh rundah):
    ur_pari = sorted(list(zip(zmage.values(), zmage.keys())), reverse = 1)
    
    # Pairingi za 4. rundo (v primerih 3210 in 2211):
    if  [ur_pari[i][0] for i in range(4)] in [[3,2,1,0], [2,2,1,1]]:
        print('\n4. runda:\n')

        # Prebere imena igralcev, urejenih padajoče po zmagah:
        A, B, C, D = [ur_pari[i][1] for i in range(4)]

        runda4 = [[A + ' (' + decki[igralci.index(ur_pari[0][1])] + ')', 'VS', B + ' (' + decki[igralci.index(ur_pari[1][1])] + ')'],
                  [C + ' (' + decki[igralci.index(ur_pari[2][1])] + ')', 'VS', D + ' (' + decki[igralci.index(ur_pari[3][1])] + ')']]        
        print(tabulate(runda4, tablefmt='plain'))

        # Zabeleži zmage:
        prvi = preveri(input('\nKdo je zmagal, {} ali {}? '.format(A,B)), [A, B], napaka2, None)
        zmage[prvi] += 1
        tretji = preveri(input('Kdo je zmagal, {} ali {}? '.format(C,D)), [C, D], napaka2, None)
        zmage[tretji] += 1

        # Seznam mest:
        mesta = [1, 2, 3, 4]
        
        # Seznam igralcev, urejen po mestih:
        imena = [prvi]
        if prvi == ur_pari[0][1]:
            imena.append(ur_pari[1][1])
        else:
            imena.append(ur_pari[0][1])
        imena.append(tretji)
        if tretji == ur_pari[2][1]:
            imena.append(ur_pari[3][1])
        else:
            imena.append(ur_pari[2][1])

        # Seznam nagrad, urejen po mestih:
        nagrade = [9, 6, 3, 0]
        for i in range(4):
            if zmage[imena[i]] == 4 - i:
                nagrade[i] += 1          


    # Pairingi za 4. rundo (v primerih 3111 in 2220):    
    else:
        print('\n4. runda:\n')

        # Naključna izbira pairingov:
        pair2_num = [[1, 0, 2, 3], [3, 1, 2, 0], [3, 0, 2, 1]]
        pair2 = random.choice(pair2_num)
        A, B, C, D = [igralci[pair2[i]] for i in range(4)]
        
        runda4 = [[A + ' (' + decki[pair2[0]] + ')', 'VS', B + ' (' + decki[pair2[1]] + ')'],
                  [C + ' (' + decki[pair2[2]] + ')', 'VS', D + ' (' + decki[pair2[3]] + ')']]
        print(tabulate(runda4, tablefmt='plain'))

        # Zabeleži zmage:
        zmage[preveri(input('\nKdo je zmagal, {} ali {}? '.format(A,B)), [A, B], napaka2, None)] += 1
        zmage[preveri(input('Kdo je zmagal, {} ali {}? '.format(C,D)), [C, D], napaka2, None)] += 1

        # Seznam parov (število zmag, igralec), urejen padajoče po zmagah (po štirih rundah):
        ur_pari = sorted(list(zip(zmage.values(), zmage.keys())), reverse = 1)

        # Seznam mest in seznam nagrad, urejenih po mestih:
        mozne_porazdelitve = [[4, 2, 1, 1], [3, 3, 2, 0], [3, 2, 2, 1]]
        mozna_mesta = [[1, 2, 3, 3], [1, 1, 3, 4], [1, 2, 2, 4]]
        mozne_nagrade = [[10, 6, 2, 2], [8, 8, 4, 0], [9, 5, 5, 1]]
        porazdelitev = [x[0] for x in ur_pari]
        for i in range(3):
            if porazdelitev == mozne_porazdelitve[i]:
                mesta = mozna_mesta[i]
                nagrade = mozne_nagrade[i]

        # Seznam igralcev, urejenih po mestih:
        imena = [igr[1] for igr in ur_pari]


    # Standingi v obliki za prikaz s 'tabulate':
    standingi = [[mesta[i], imena[i], str(nagrade[i]) + '€'] for i in range(4)]

    print('----------------------------------------------------')
    print('\nTurnir je zaključen!')
    print('\n----------------------STANDINGI---------------------\n')
    print(tabulate(standingi, headers=['Mesto', 'Igralec', 'Nagrada'], colalign=('center', 'left', 'center')))
    print('\n\nČestitke vsem igralcem!')
    input('\n----------------------------------------------------\n(Za izhod pritisni ENTER.)')
    input('\nPa do naslednjič!')


turnir()
