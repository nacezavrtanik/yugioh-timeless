import random

print('================== *** IME LIGE *** ==================\n') # TIMELESS LIGA?
print('*** OPIS FORMATOV ***\n')

def deck(stevilka):
    decki1 = ['Normal', 'Dragon', 'Beast', 'Chaos']
    decki2 = ['Warrior', 'Flip', 'Plant', 'Zombie']
    if stevilka == '1':
        return (decki1, '1')
    elif stevilka == '2':
        return (decki2, '2')
    else:
        return(deck(input('\nUps, prišlo je do napake. Vnesi samo 1 ali 2 in pritisni ENTER.\nŠtevilka formata: ')))

(decki, izbrani) = deck(input('1 *** Prvi format *** \n2 *** Drugi format *** \n\nKaterega boste igrali? Številka formata: '))

##if izbrani == '1':
##    izbira = 'Stari'
##    ocena = 'Odlična'
##else:
##    izbira = 'Novi'
##    ocena = 'Dobra'
##
##print('\n' + izbira + ' format torej? ' + ocena + ''' izbira. Zdaj pa samo
##še vnesi imena posameznih igralcev in program
##ti bo izpisal pairinge.\n''')

print('\n*** TEKST ***\n')
igr1 = input('1. igralec: ')
igr2 = input('2. igralec: ')
igr3 = input('3. igralec: ')
igr4 = input('4. igralec: ')
print('\nVeliko zabave pri igranju!')

def turnir(ime1, ime2, ime3, ime4):

    igralcifix = [ime1, ime2, ime3, ime4]
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

    pairingi = [ igralci[0] + ' (' + str(decki[matchup[1][0]]) + ')   VS   '
                 + igralci[1] + ' (' + str(decki[matchup[1][1]]) + ')\n'
                 + igralci[2] + ' (' + str(decki[matchup[1][2]]) + ')   VS   '
                 + igralci[3] + ' (' + str(decki[matchup[1][3]]) + ')',

                 igralci[1] + ' (' + str(decki[matchup[2][1]]) + ')   VS   '
                 + igralci[3] + ' (' + str(decki[matchup[2][3]]) + ')\n'
                 + igralci[0] + ' (' + str(decki[matchup[2][0]]) + ')   VS   '
                 + igralci[2] + ' (' + str(decki[matchup[2][2]]) + ')',

                 igralci[3] + ' (' + str(decki[matchup[3][3]]) + ')   VS   '
                 + igralci[0] + ' (' + str(decki[matchup[3][0]]) + ')\n'
                 + igralci[1] + ' (' + str(decki[matchup[3][1]]) + ')   VS   '
                 + igralci[2] + ' (' + str(decki[matchup[3][2]]) + ')'
                 ]

    print('\n----------------------PAIRINGI----------------------\n')
    
    mesta = [0, 1, 2]

    zmage = {i : 0 for i in igralci}
    print(zmage)
    print('')
    
    for i in range(3):
        
        print(str(i+1) +  '. runda: \n')
        mesto = random.choice(mesta)
        mesta.remove(mesto)
        print(pairingi[mesto] + '\n')

        zmage[str(input('Kdo je zmagal? '))] += 1
        print('')
        print(zmage)
        print('')
        

    print('Decki v 4. rundi:\n')
    
    zadnja = {}
    
    for i in range(4):
        zadnja[igralci[i]] = ' (' + str(decki[matchup[0][i]]) + ')'
        
    for igr in igralcifix:
        print(igr + zadnja[igr])
        
    print('\n----------------------------------------------------\n(Za izhod pritisni ENTER.)')

turnir(igr1, igr2, igr3, igr4)

input()
input('POZOR! Si prepričan, da želiš zapreti okno?\n')
input('Pa do naslednjič! :)\n')















