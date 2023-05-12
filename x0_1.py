def hello():
    print('______________________')
    print('Добро пожаловать')
    print('в игру крестики-нолики')
    print('______________________')
    print('чтобы сделать ход')
    print('укажите координаты ячейки через пробел:')
    print('первая цифра - номер строки')
    print('вторая цифра - номер стобца')
    print('_______________________')



def game():
    print()
    print('  | 0 | 1 | 2 |')
    print('_________________')
    for i, row in enumerate(field):
        row_str= f"{i} |{'  |'.join(row)}  |"
        print(row_str)
        print('_________________')
    print()

def ask_coord():
    while True:
        coord_inp=input('введите координаты: ')
        coords=coord_inp.split()
        if len(coords) !=2:
            print('введите две координаты: ')
            continue
        x,y=coords
        if not(x.isdigit()) or not(y.isdigit()):
            print('введите числа! ')
            continue

        x,y=int(x), int(y)

        if any([0>x, x >2, 0>y, y>2]):
            print('координаты вне диапазона игрового поля!')
            continue

        if field[x][y] !=' ':
            print('клетка занята')
            continue

        return x,y

def win():
    for i in range(3):
        win_row=[]
        for j in range(3):
            win_row.append(field[i][j])
        if win_row==['x', 'x', 'x']:
            print('выиграл х!')
            return True
        if win_row==['0', '0', '0']:
            print('выиграл 0!')
            return True


    for i in range (3):
        win_colomn=[]
        for j in range(3):
            win_colomn.append(field[j][i])
        if win_colomn == ['x', 'x', 'x']:
                print('выиграл х!')
                return True
        if win_colomn == ['0', '0', '0']:
                print('выиграл 0!')
                return True



    win_diag=[]
    for i in range(3):
        win_diag.append(field[i][i])
    if win_diag== ['x','x','x']:
        print('выиграл х!')
        return True
    if win_diag == ['0', '0', '0']:
        print('выиграл 0!')
        return True



    win_diag=[]
    for j in range(3):
        win_diag.append(field[j][2-j])
    if win_diag == ['x', 'x', 'x']:
        print('выиграл х!')
        return True
    if win_diag == ['0', '0', '0']:
        print('выиграл 0!')
        return True
    return False

hello()
field=[[' ']*3 for i in range(3)]

for i in range(10):
    i +=1
    game()
    if i%2==1:
        print('ходят крестики')
        x,y=ask_coord()
        field[x][y]='x'
    else:
        print('ходят нолики')
        x,y=ask_coord()
        field[x][y]='0'
    if win():
        game()
        break
    if i==9:
        game()
        print('ничья')
        break
