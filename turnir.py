import random


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
    matchupi = [[[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]],
                [[0, 1, 2, 3], [1, 0, 3, 2], [3, 2, 1, 0], [2, 3, 0, 1]],
                [[0, 1, 2, 3], [3, 2, 1, 0], [1, 0, 3, 2], [2, 3, 0, 1]],
                [[0, 1, 2, 3], [2, 3, 0, 1], [1, 0, 3, 2], [3, 2, 1, 0]],
                [[0, 1, 2, 3], [2, 3, 0, 1], [3, 2, 1, 0], [1, 0, 3, 2]],
                [[0, 1, 2, 3], [3, 2, 1, 0], [2, 3, 0, 1], [1, 0, 3, 2]],
                [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 1, 0], [3, 2, 0, 1]],
                [[0, 1, 2, 3], [1, 0, 3, 2], [3, 2, 0, 1], [2, 3, 1, 0]],
                [[0, 1, 2, 3], [3, 2, 0, 1], [1, 0, 3, 2], [2, 3, 1, 0]],
                [[0, 1, 2, 3], [2, 3, 1, 0], [1, 0, 3, 2], [3, 2, 0, 1]],
                [[0, 1, 2, 3], [2, 3, 1, 0], [3, 2, 0, 1], [1, 0, 3, 2]],
                [[0, 1, 2, 3], [3, 2, 0, 1], [2, 3, 1, 0], [1, 0, 3, 2]],
                [[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]],
                [[0, 1, 2, 3], [1, 2, 3, 0], [3, 0, 1, 2], [2, 3, 0, 1]],
                [[0, 1, 2, 3], [3, 0, 1, 2], [1, 2, 3, 0], [2, 3, 0, 1]],
                [[0, 1, 2, 3], [2, 3, 0, 1], [1, 2, 3, 0], [3, 0, 1, 2]],
                [[0, 1, 2, 3], [2, 3, 0, 1], [3, 0, 1, 2], [1, 2, 3, 0]],
                [[0, 1, 2, 3], [3, 0, 1, 2], [2, 3, 0, 1], [1, 2, 3, 0]],
                [[0, 1, 2, 3], [1, 3, 0, 2], [2, 0, 3, 1], [3, 2, 1, 0]],
                [[0, 1, 2, 3], [1, 3, 0, 2], [3, 2, 1, 0], [2, 0, 3, 1]],
                [[0, 1, 2, 3], [3, 2, 1, 0], [1, 3, 0, 2], [2, 0, 3, 1]],
                [[0, 1, 2, 3], [2, 0, 3, 1], [1, 3, 0, 2], [3, 2, 1, 0]],
                [[0, 1, 2, 3], [2, 0, 3, 1], [3, 2, 1, 0], [1, 3, 0, 2]],
                [[0, 1, 2, 3], [3, 2, 1, 0], [2, 0, 3, 1], [1, 3, 0, 2]]]

    random.shuffle(decki)
    random.shuffle(igralci)
    
    matchup = random.choice(matchupi)

    pairingi = [ igralci[0] + ' (' + str(decki[matchup[1][0]]) + ')\tVS\t'
                 + igralci[1] + ' (' + str(decki[matchup[1][1]]) + ')\n'
                 + igralci[2] + ' (' + str(decki[matchup[1][2]]) + ')\tVS\t'
                 + igralci[3] + ' (' + str(decki[matchup[1][3]]) + ')',

                 igralci[1] + ' (' + str(decki[matchup[2][1]]) + ')\tVS\t'
                 + igralci[3] + ' (' + str(decki[matchup[2][3]]) + ')\n'
                 + igralci[0] + ' (' + str(decki[matchup[2][0]]) + ')\tVS\t'
                 + igralci[2] + ' (' + str(decki[matchup[2][2]]) + ')',

                 igralci[3] + ' (' + str(decki[matchup[3][3]]) + ')\tVS\t'
                 + igralci[0] + ' (' + str(decki[matchup[3][0]]) + ')\n'
                 + igralci[1] + ' (' + str(decki[matchup[3][1]]) + ')\tVS\t'
                 + igralci[2] + ' (' + str(decki[matchup[3][2]]) + ')'
                 ]

    pairingi2 = [ igralci[1] + ' (' + str(decki[matchup[0][1]]) + ')\tVS\t'
             + igralci[0] + ' (' + str(decki[matchup[0][0]]) + ')\n'
             + igralci[2] + ' (' + str(decki[matchup[0][2]]) + ')\tVS\t'
             + igralci[3] + ' (' + str(decki[matchup[0][3]]) + ')',

             igralci[3] + ' (' + str(decki[matchup[0][3]]) + ')\tVS\t'
             + igralci[1] + ' (' + str(decki[matchup[0][1]]) + ')\n'
             + igralci[2] + ' (' + str(decki[matchup[0][2]]) + ')\tVS\t'
             + igralci[0] + ' (' + str(decki[matchup[0][0]]) + ')',

             igralci[3] + ' (' + str(decki[matchup[0][3]]) + ')\tVS\t'
             + igralci[0] + ' (' + str(decki[matchup[0][0]]) + ')\n'
             + igralci[2] + ' (' + str(decki[matchup[0][2]]) + ')\tVS\t'
             + igralci[1] + ' (' + str(decki[matchup[0][1]]) + ')'
             ]
    
    print('\n----------------------PAIRINGI----------------------')
    
    mesta = [0, 1, 2]

    zmage1 = {i : 0 for i in igralci}
    
    for i in range(3):
        
        print('\n' + str(i+1) +  '. runda: \n')
        mesto = random.choice(mesta)
        mesta.remove(mesto)
        print(pairingi[mesto] + '\n')

        zmage1[str(input('Kdo je zmagal prvi match? '))] += 1
        zmage1[str(input('Kdo je zmagal drugi match? '))] += 1
        print('----------------------------------------------------')

    zmage2 = sorted(list(zip(zmage1.values(), zmage1.keys())), reverse = 1)

    if [zmage2[0][0], zmage2[1][0], zmage2[2][0], zmage2[3][0]] == [3,2,1,0] or [zmage2[0][0], zmage2[1][0], zmage2[2][0], zmage2[3][0]] == [2,2,1,1]:
        print('\n4. runda:\n')
        print(zmage2[0][1] + ' (' + decki[igralci.index(zmage2[0][1])] + ')\tVS\t' + zmage2[1][1] + ' (' + decki[igralci.index(zmage2[1][1])] + ')\n' +
              zmage2[2][1] + ' (' + decki[igralci.index(zmage2[2][1])] + ')\tVS\t' + zmage2[3][1] + ' (' + decki[igralci.index(zmage2[3][1])] + ')')

        prvi = input('\nKdo je zmagal prvi match? ')
        zmage1[prvi] += 1
        tretji = input('Kdo je zmagal drugi match? ')
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
                
        print('\nČestitke vsem igralcem!')
        print('\n----------------------STANDINGI---------------------\n')

        for i in range(4):
            print(str(i+1) + '. mesto:\t' + stand[i] + '\t(' + str(nagrade[i]) + '€)')
                
        
    else:
        print('\n4. runda:\n')
        print(random.choice(pairingi2))

        zmage1[str(input('\nKdo je zmagal prvi match? '))] += 1
        zmage1[str(input('Kdo je zmagal drugi match? '))] += 1
        
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
            
        print('\nČestitke vsem igralcem!')
        print('\n----------------------STANDINGI---------------------\n')

        for i in range(4):
            print(str(pozicija[i]) + '. mesto:\t' + zmage3[i][1] + '\t(' + str(nagrade[i]) + '€)')

    print('\n----------------------------------------------------\n(Za izhod pritisni ENTER.)')


turnir(igr1, igr2, igr3, igr4)

input()
input('Pa do naslednjič!\n')
