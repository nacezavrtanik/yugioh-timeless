import random
from tabulate import tabulate

print('================== *** IME LIGE *** ==================\n')
print('*** OPIS FORMATOV ***\n')


def deck(stevilka):
    decki1 = ['Normal', 'Dragon', 'Beast', 'Chaos']
    decki2 = ['Warrior', 'Flip', 'Plant', 'Zombie']
    if stevilka == '1':
        return decki1
    elif stevilka == '2':
        return decki2
    else:
        return(deck(input('\nUps, prišlo je do napake. Vnesi samo 1 ali 2 in pritisni ENTER.\nŠtevilka formata: ')))


decki = deck(input('1 *** Prvi format *** \n2 *** Drugi format *** \n\nKaterega boste igrali? Številka formata: '))

print('\n*** TEKST ***\n')
igr1 = input('1. igralec: ')
igr2 = input('2. igralec: ')
igr3 = input('3. igralec: ')
igr4 = input('4. igralec: ')
print('\nVeliko zabave pri igranju!')


def turnir(ime1, ime2, ime3, ime4):

    igralci = [ime1, ime2, ime3, ime4]
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

    random.shuffle(decki)
    random.shuffle(igralci)
    
    matchup = random.choice(matchupi)

    pairingi1 = []
    pairingi2 = []

    pairing1 = [[0, 1, 2, 3], [1, 3, 0, 2], [3, 0, 1, 2]]
    pairing2 = [[1, 0, 2, 3], [3, 1, 2, 0], [3, 0, 2, 1]]

    for i in range(3):
        sez1 = []
        sez2 = []
        for j in [0, 2]:
            a1 = pairing1[i][j]
            b1 = pairing1[i][j+1]
            a2 = pairing2[i][j]
            b2 = pairing2[i][j+1] 
            sez1.append([ igralci[a1] + ' (' + decki[matchup[a1][b1]] + ')', 'VS', igralci[b1] + ' (' + decki[matchup[b1][a1]] + ')' ])
            sez2.append([ igralci[a2] + ' (' + decki[a2] + ')', 'VS', igralci[b2] + ' (' + decki[b2] + ')' ])
        pairingi1.append(sez1)
        pairingi2.append(sez2)

    random.shuffle(pairingi1)
    random.shuffle(pairingi2)
    
    print('\n----------------------PAIRINGI----------------------')

    zmage1 = {i : 0 for i in igralci}
    
    for i in range(3):
        
        print('\n' + str(i+1) +  '. runda: \n')
        print(tabulate(pairingi1[i], tablefmt='plain'))

        A, B, C, D = [pairingi1[i][0][0].split(' (')[0], pairingi1[i][0][2].split(' (')[0], pairingi1[i][1][0].split(' (')[0], pairingi1[i][1][2].split(' (')[0]]
        
        zmage1[str(input('\nKdo je zmagal, {} ali {}? '.format(A,B)))] += 1
        zmage1[str(input('Kdo je zmagal, {} ali {}? '.format(C,D)))] += 1
        print('----------------------------------------------------')

    zmage2 = sorted(list(zip(zmage1.values(), zmage1.keys())), reverse = 1)

    if  [zmage2[i][0] for i in range(4)] == [3,2,1,0] or [zmage2[i][0] for i in range(4)] == [2,2,1,1]:
        print('\n4. runda:\n')

        A, B, C, D = [zmage2[i][1] for i in range(4)]
        
        table = [[A + ' (' + decki[igralci.index(zmage2[0][1])] + ')', 'VS', B + ' (' + decki[igralci.index(zmage2[1][1])] + ')'],
                [C + ' (' + decki[igralci.index(zmage2[2][1])] + ')', 'VS', D + ' (' + decki[igralci.index(zmage2[3][1])] + ')']]
        
        print(tabulate(table, tablefmt='plain'))

        prvi = input('\nKdo je zmagal, {} ali {}? '.format(A,B))
        zmage1[prvi] += 1
        tretji = input('Kdo je zmagal, {} ali {}? '.format(C,D))
        zmage1[tretji] += 1

        print('----------------------------------------------------')

        stand = [prvi]
        
        if prvi == zmage2[0][1]:
            stand.append(zmage2[1][1])
        else:
            stand.append(zmage2[0][1])
        stand.append(tretji)
        if tretji == zmage2[2][1]:
            stand.append(zmage2[3][1])
        else:
            stand.append(zmage2[2][1])

        nagrade = [9, 6, 3, 0]
        for i in range(4):
            if zmage1[stand[i]] == 4 - i:
                nagrade[i] += 1
                
        print('\nTurnir je zaključen!')
        print('\n----------------------STANDINGI---------------------\n')
        
        table = [[i+1, stand[i], str(nagrade[i]) + '€'] for i in range(4)]
        print(tabulate(table, headers=['Mesto', 'Igralec', 'Nagrada'], colalign=('center', 'left', 'center')))
                
        
    else:
        print('\n4. runda:\n')
        print(tabulate(pairingi2[0], tablefmt='plain'))

        A, B, C, D = [pairingi2[0][0][0].split(' (')[0], pairingi2[0][0][2].split(' (')[0], pairingi2[0][1][0].split(' (')[0], pairingi2[0][1][2].split(' (')[0]]

        zmage1[str(input('\nKdo je zmagal, {} ali {}? '.format(A,B)))] += 1
        zmage1[str(input('Kdo je zmagal, {} ali {}? '.format(C,D)))] += 1
        
        print('----------------------------------------------------')

        zmage3 = sorted(list(zip(zmage1.values(), zmage1.keys())), reverse = 1)

        razporedi = [[4, 2, 1, 1], [3, 3, 2, 0], [3, 2, 2, 1]]
        razpored = [x[0] for x in zmage3]
        
        if razporedi.index(razpored) == 0:
            pozicija = [1, 2, 3, 3]
            nagrade = [10, 6, 2, 2]
        elif razporedi.index(razpored) == 1:
            pozicija = [1, 1, 3, 4]
            nagrade = [8, 8, 4, 0]
        else:
            pozicija = [1, 2, 2, 4]
            nagrade = [9, 5, 5, 1]
            
        print('\nTurnir je zaključen!')
        print('\n----------------------STANDINGI---------------------\n')

        table = [[pozicija[i], zmage3[i][1], str(nagrade[i]) + '€'] for i in range(4)]
        print(tabulate(table, headers=['Mesto', 'Igralec', 'Nagrada'], colalign=('center', 'left', 'center')))

    print('\n\nČestitke vsem igralcem!')
    input('\n----------------------------------------------------\n(Za izhod pritisni ENTER.)')
    input('\nPa do naslednjič!')


turnir(igr1, igr2, igr3, igr4)
