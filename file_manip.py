def read():
    try:
        with open('.pomodororc', 'r') as pomodororc:
            counter = pomodororc.readlines()
    except FileNotFoundError:
        creater()
    else:
        if counter == []:
            creater()
            return False

        counter = (''.join(counter)).split('\n')
        try:
            counter.remove('')
        except Exception:
            pass
        return counter


def creater():
    write_me = ['completed: 0', 'worked: 00', 'rested: 00', 'total: 0']
    counter = 1
    for x in range(len(write_me)):
        write_me.insert(counter, '\n')
        counter += 2

    try:
        with open('.pomodororc', 'w+') as pomodororc:
            pomodororc.writelines(write_me)
    except Exception as error:
        print(f'occurred an error trying to create the file: {error}')


def write(argv):
    try:
        counter = read()
    except Exception:
        raise
    else:
        if counter is False or counter is None:
            counter = read()

        for x in range(len(counter)):  # splits the strings
            counter[x] = [x.strip() for x in counter[x].split(':')]

        if 'total' not in counter[-1][0]:  # add the total if not found
            counter.append(['total', 0])
        print(counter)
        exit()
        counter = [[x[0], int(x[1])] for x in counter]

        a = 0
        for x in counter:
            if 'work' in x[0]:
                x[1] += argv.get('work-time')
                a += x[1]
            elif 'rest' in x[0]:
                x[1] += argv.get('short-break')
                a += x[1]
            elif 'completed' in x[0]:
                x[1] += 1
            elif 'total' in x[0]:
                x[1] = a

        for x in range(len(counter)):
            counter[x] = f'{counter[x][0]}: {counter[x][1]}'  # join strings

        count = 1
        for x in range(len(counter)):  # make a function to do it
            counter.insert(count, '\n')
            count += 2

        try:
            with open('.pomodororc', 'w+') as pomodororc:
                pomodororc.writelines(counter)
        except Exception:
            raise


def file_clean():  # Just an easy way to delete all file content
    try:
        with open('.pomodororc', 'r+') as my_file:
            my_file.truncate(0)
    except Exception:
        raise
    else:
        print('The file is clean.')


# Pegar o tempo rodado no pomodoro e ir somando o valor
# Salvar o tempo caso raise KeyboardInterrupt ex: 17:35 -> somar ao total
# Json file

