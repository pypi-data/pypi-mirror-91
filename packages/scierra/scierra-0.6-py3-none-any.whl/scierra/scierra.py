from scierra.sim import Simulator

def main():
    flag = True
    res = True
    simul = Simulator()

    print('Scierra C++ Interpreter v0.6\nCopyright (c) PerceptronV 2020')
    line = input('\n++> ')
    stripline = line.strip()

    if stripline == '<print>':
        simul.print_code()
    elif stripline == '<restart>':
        simul.restart()
    elif stripline == '<esc>':
        flag = False
    elif stripline == '':
        pass
    else:
        res = simul.addline(line + '\n')

    while (flag):
        if res:
            line = input('\n++> ')
        else:
            line = input('\n--> ')
        stripline = line.strip()

        if stripline == '<print>':
            simul.print_code()
        elif stripline == '<restart>':
            res = True
            simul.restart()
        elif stripline == '<esc>':
            flag = False
        elif stripline == '':
            pass
        else:
            res = simul.addline(line + '\n')
