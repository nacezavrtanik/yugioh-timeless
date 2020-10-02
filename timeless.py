import random
import string
from tabulate import tabulate


# Sporočila napak za uporabo v 'preveri' (spodaj):
napaka1 = 'Ups, prišlo je do napake. Vnesi le 1 ali 2: '
napaka2 = 'Ups, prišlo je do napake. Ime zmagovalca: '
napaka3 = 'Ime naj vsebuje le črke in presledke.\n{}. igralec: '
napaka4 = 'Ime naj bo krajše od 30 znakov.\n{}. igralec: '
napaka5 = 'Ups, prišlo je do napake. Vnesi le 1, 2 ali 3: '


# Zahteva določene vrednosti za 'input()':
def preveri(vnos, opcije, napaka, tip):
    if tip == 'ime':
        if not vnos.replace(' ','').isalpha():
            return(preveri(input(napaka[0]), None, napaka, 'ime'))
        elif len(string.capwords(vnos)) < 30:
            return string.capwords(vnos)
        else:
            return(preveri(input(napaka[1]), None, napaka, 'ime'))
    else:
        vnos = string.capwords(vnos)
        if vnos in opcije:
            return vnos
        else:
            return(preveri(input(napaka), opcije, napaka, None))


# Sestavi in predstavi potek turnirja:
def turnir():


    print('''====================== TIMELESS ======================

Timeless je poseben turnirski format za štiri igralce.
Ti se pomerijo v treh predrundah (vsak z vsakim), nato
pa sledi še finalna runda. Nobena izmed teh ni časovno
omejena. Igra se z naborom štirih deckov, ki so med
igralce razdeljeni naključno. Po vsaki rundi se decki
ponovno naključno razdelijo med igralce, in sicer tako,
da v štirih rundah vsak igralec igra z vsakim izmed
štirih deckov natanko enkrat. Na voljo sta dva nabora
deckov:

 1) BASIC
 2) EXTRA''')

    
    # Kateri decki se bodo igrali:
    nabori = [('BASIC', [' (Spellcaster)', ' (Dragon)', ' (Beast)', ' (Chaos)']), ('EXTRA', [' (Warrior)', ' (Flip)', ' (Zombie)', ' (Beatdown)'])]
    izbira = int(preveri(input('\nS katerim želite igrati? Številka nabora: '), ['1', '2'], napaka1, None)) - 1
    decki = nabori[izbira][1]
    random.shuffle(decki)


    print('''
Dobro, igral se bo Timeless {}. Kaj pa prijavnina?
Ta gre v celoti v nagradni sklad in se na koncu glede
na dosežke razdeli nazaj med igralce.

 1) 5 €
 2) 10 €
 3) brez'''.format(nabori[izbira][0]))


    # Prijavnina:
    prijavnina = int(preveri(input('\nŠtevilka opcije: '), ['1', '2', '3'], napaka5, None))
    
    print('\nVnesi samo še imena igralcev in turnir se lahko začne.\n')

    # Kdo bo igral na turnirju:
    igralci = [preveri(input('{}. igralec: '.format(i+1)), None, [napaka3.format(i+1), napaka4.format(i+1)], 'ime') for i in range(4)]
    random.shuffle(igralci)

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
    pairingi = [[0, 1, 2, 3], [1, 3, 0, 2], [3, 0, 1, 2]]
    random.shuffle(pairingi)

    # Beleži število zmag na igralca:
    zmage = {igr : 0 for igr in igralci}
    

    print('''
Veliko zabave pri igranju!


================== TIMELESS {} ==================

----------------------PAIRINGI----------------------'''.format(nabori[izbira][0]))


    # Prikaz pairingov za prve tri runde (vsak z vsakim):
    for i in range(3):
        
        print('\n{}. runda: \n'.format(i+1))

        # Igralci, decki:
        X, Y, Z, W = [pairingi[i][j] for j in range(4)]
        A, B, C, D = [igralci[X], igralci[Y], igralci[Z], igralci[W]]
        dA, dB, dC, dD = [decki[matchup[X][Y]], decki[matchup[Y][X]], decki[matchup[Z][W]], decki[matchup[W][Z]]]

        runda = [[A + dA, 'VS', B + dB], [C + dC, 'VS', D + dD]]
        print(tabulate(runda, tablefmt='plain'))

        # Zabeleži zmage:
        zmage[preveri(input('\nKdo je zmagal, {} ali {}? '.format(A,B)), [A, B], napaka2, None)] += 1
        zmage[preveri(input('Kdo je zmagal, {} ali {}? '.format(C,D)), [C, D], napaka2, None)] += 1
        print('----------------------------------------------------')
        

    # Seznam parov (število zmag, igralec), urejen padajoče po zmagah (po treh rundah):
    ur_pari = sorted(list(zip(zmage.values(), zmage.keys())), reverse = 1)
    
    # Pairingi za 4. rundo (v primerih 3210 in 2211):
    if  [ur_pari[i][0] for i in range(4)] in [[3,2,1,0], [2,2,1,1]]:
        
        print('\n4. runda:\n')

        # Igralci, decki:
        A, B, C, D = [ur_pari[i][1] for i in range(4)]
        dA, dB, dC, dD = [decki[igralci.index(ur_pari[i][1])] for i in range(4)]

        runda4 = [[A + dA, 'VS', B + dB], [C + dC, 'VS', D + dD]]        
        print(tabulate(runda4, tablefmt='plain'))

        # Zabeleži zmage:
        prvi = preveri(input('\nKdo je zmagal, {} ali {}? '.format(A,B)), [A, B], napaka2, None)
        zmage[prvi] += 1
        tretji = preveri(input('Kdo je zmagal, {} ali {}? '.format(C,D)), [C, D], napaka2, None)
        zmage[tretji] += 1

        # Mesta:
        mesta = [1, 2, 3, 4]
        
        # Imena:
        imena = [prvi]
        if prvi == A:
            imena.append(B)
        else:
            imena.append(A)
        imena.append(tretji)
        if tretji == C:
            imena.append(D)
        else:
            imena.append(C)

        # Nagrade:
        if prijavnina == 3:
            nagrade = ['Večna čast in slava.', 'Naziv \'skoraj najboljši\'.', 'Nič, a vsaj zadnji nisi.', 'Nič. Noob.']
        else:
            nagrade = [j * prijavnina for j in [9, 6, 3, 0]]
            for i in range(4):
                if zmage[imena[i]] == 4 - i:
                    nagrade[i] += prijavnina
            nagrade = [str(i) + ' €' for i in nagrade]


    # Pairingi za 4. rundo (v primerih 3111 in 2220):    
    else:
        
        print('\n4. runda:\n')

        # Naključna izbira pairingov:
        pairing = random.choice([[1, 0, 2, 3], [3, 1, 2, 0], [3, 0, 2, 1]])
        
        # Igralci, decki:
        A, B, C, D = [igralci[pairing[i]] for i in range(4)]
        dA, dB, dC, dD = [decki[pairing[i]] for i in range(4)]
        
        runda4 = [[A + dA, 'VS', B + dB], [C + dC, 'VS', D + dD]]
        print(tabulate(runda4, tablefmt='plain'))

        # Zabeleži zmage:
        zmage[preveri(input('\nKdo je zmagal, {} ali {}? '.format(A,B)), [A, B], napaka2, None)] += 1
        zmage[preveri(input('Kdo je zmagal, {} ali {}? '.format(C,D)), [C, D], napaka2, None)] += 1

        # Seznam parov (število zmag, igralec), urejen padajoče po zmagah (po štirih rundah):
        ur_pari = sorted(list(zip(zmage.values(), zmage.keys())), reverse = 1)

        # Mesta, nagrade:
        porazdelitev = [st_zmag[0] for st_zmag in ur_pari]
        mozne_porazdelitve = [[4, 2, 1, 1], [3, 3, 2, 0], [3, 2, 2, 1]]
        mozna_mesta = [[1, 2, 3, 3], [1, 1, 3, 4], [1, 2, 2, 4]]
        mozne_nagrade1 = [[10, 6, 2, 2], [8, 8, 4, 0], [9, 5, 5, 1]]
        mozne_nagrade2 = [['Večna čast in slava.', 'Naziv \'skoraj najboljši\'.', 'Pol bronaste medalje.', 'Pol bronaste medalje.'],
                          ['Pol zlate medalje.', 'Pol zlate medalje.', 'Nič, a vsaj zadnji nisi.', 'Nič. Noob.'],
                          ['Večna čast in slava.', 'Pol srebrne medalje.', 'Pol srebrne medalje.', 'Nič. Noob.']]
        for i in range(3):
            if porazdelitev == mozne_porazdelitve[i]:
                mesta = mozna_mesta[i]
                if prijavnina == 3:
                    nagrade = mozne_nagrade2[i]
                else:
                    nagrade = [str(j * prijavnina) + ' €' for j in mozne_nagrade1[i]]

        # Imena:
        imena = [igr[1] for igr in ur_pari]


    # Standingi v obliki za prikaz s 'tabulate':
    standingi = [[mesta[i], imena[i], nagrade[i]] for i in range(4)]
    

    print('''----------------------------------------------------

Turnir je zaključen!

----------------------STANDINGI---------------------
''')

    print(tabulate(standingi, headers=['Mesto', 'Igralec', 'Nagrada'], colalign=('center', 'left', 'left' if prijavnina == 3 else 'center')))

    print('\n\nČestitke vsem igralcem!')
    input('\n====================================================\n(Za izhod pritisni ENTER.)')
    input('\nPa do naslednjič!')


turnir()
