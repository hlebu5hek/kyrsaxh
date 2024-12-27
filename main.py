from tkinter import *
from checkers.game import Game
from checkers.constants import X_SIZE, Y_SIZE, CELL_SIZE
import checkers.constants as const
import checkers.enums as enums

def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def CodePassword(pass_: str, login_: str):
    key = ''
    npass_ = ''
    for i, char in enumerate(login_):
        key += format(ord(char), 'b')[i]
    for char in pass_:
        bn = format(ord(char), 'b')
        bn = int(bn, 2)
        npass_ += (str)(int(key, 2) + bn) + ' '

    return npass_[0:-1:1]


def DecodePassword(pass_: str, login_: str):
    ints = pass_.split(' ')
    dpass_ = ''
    key = ''
    for i, char in enumerate(login_):
        key += format(ord(char), 'b')[i]
    for char in ints:
        bn = int(char)
        dpass_ += chr(bn - int(key, 2))

    return dpass_


def SavePassword(pass_: str, login_: str):
    f = open('login/password.txt', 'a')
    f.write(login_ + ':' + pass_ + '\n')

def LoadPassword():
    f = open('login/password.txt', 'r')
    d = {}
    for line in f.readlines():
        a = line.split(':')
        d[a[0]] = a[1]
    return d

in_log_process = False
log_root = None

login_txt = None
pass_txt = None

def main():
    # Создание окна
    start_window = Tk()
    start_window.title('Шашки-поддавки')
    start_window.resizable(0, 0)
    start_window.geometry("250x495")

    instruction = Label(text='Инструкция:\n'
                             'Первым ходят белые\n'
                             'Ход только по диагонали\n'
                             '    в сторону противника\n'
                             '    на одну клетку\n'
                             'Есть фигуры можно,\n'
                             '    прыгая через неё по\n'
                             '    диагонали в любую сторону\n'
                             'Дойдя до крайней линии\n'
                             '    противоположной стороны\n'
                             '    шашка становиться королевой\n'
                             'Королева ходит на любое\n'
                             '    количество клеток',
                        justify='left')
    instruction.place(x=25,y=280)

    lang = StringVar(value="'Выбор стороны")

    header_side = Label(textvariable=lang)
    header_side.place(x=25,y=10)

    white_btn = Radiobutton(text='Белые', value='Белые', variable=lang)
    white_btn.place(x=25,y=40)

    black_btn = Radiobutton(text='Черные', value='Черные', variable=lang)
    black_btn.place(x=140,y=40)

    acc_info = Label(text='Войти в аккаунт')
    acc_info.place(x=25,y=220)

    # Создание холста
    def start_game(diff: int, side: enums.SideType, bot: bool):
        start_window.destroy()

        main_window = Tk()
        main_window.title('Шашки')
        main_window.resizable(0, 0)

        main_canvas = Canvas(main_window, width=CELL_SIZE * X_SIZE, height=CELL_SIZE * Y_SIZE)
        main_canvas.pack()

        game = Game(main_canvas, X_SIZE, Y_SIZE, diff, side, bot, main_window, main)

        main_canvas.bind("<Motion>", game.mouse_move)
        main_canvas.bind("<Button-1>", game.mouse_down)

        center(main_window)
        main_window.mainloop()

    def start_easy_bot():
        s = enums.SideType.BLACK if lang.get() == 'Черные' else enums.SideType.WHITE
        start_game(1, s, True)

    def start_middle_bot():
        s = enums.SideType.BLACK if lang.get() == 'Черные' else enums.SideType.WHITE
        start_game(3, s, True)

    def start_hard_bot():
        s = enums.SideType.BLACK if lang.get() == 'Черные' else enums.SideType.WHITE
        start_game(5, s, True)

    def start_players():
        start_game(1, enums.SideType.WHITE, False)

    def Login():
        global log_root
        global in_log_process
        global login_txt, pass_txt

        if in_log_process:
            lt = login_txt.get()
            pt = pass_txt.get()

            if lt != '' and pt != '':
                d = LoadPassword()
                if lt in d.keys():
                    pass_ = DecodePassword(d[lt], lt)
                    if(pass_ == pt):
                        print('Login Successful, user : ' + lt)
                        acc_info.config(text='Пользователь: ' + lt)

            in_log_process = False

            log_root.destroy()
            start_window.deiconify()
        else:
            start_window.withdraw()
            log_root = Tk()
            log_root.title('Вход в аккаунт')
            log_root.resizable(0, 0)
            log_root.geometry("200x125")

            login_lab = Label(log_root, text='Логин:')
            login_lab.place(x=20, y=15)

            login_txt = Entry(log_root)
            login_txt.place(x=75, y=15, width=100, height=20)

            pass_lab = Label(log_root, text='Пароль:')
            pass_lab.place(x=20, y=45)

            pass_txt = Entry(log_root)
            pass_txt.place(x=75, y=45, width=100, height=20)

            in_log_process = True

            login_btn = Button(log_root, text='Войти', command=Login)
            login_btn.place(x=50, y=80, width=100,height=30)

            center(log_root)
            log_root.mainloop()

    def Register():
        global log_root
        global in_log_process
        global login_txt, pass_txt
        if in_log_process:
            lt = login_txt.get()
            pt = pass_txt.get()

            if lt != '' and pt != '':
                pt = CodePassword(pt, lt)
                SavePassword(pt, lt)
                print('Register Successful, user : ' + lt)
                acc_info.config(text='Пользователь: ' + lt)

            in_log_process = False

            log_root.destroy()
            start_window.deiconify()
        else:
            start_window.withdraw()
            log_root = Tk()
            log_root.title('Регистрация')
            log_root.resizable(0, 0)
            log_root.geometry("200x125")

            login_lab = Label(log_root, text='Логин:')
            login_lab.place(x=20, y=15)

            login_txt = Entry(log_root)
            login_txt.place(x=75, y=15, width=100, height=20)

            pass_lab = Label(log_root, text='Пароль:')
            pass_lab.place(x=20, y=45)

            pass_txt = Entry(log_root)
            pass_txt.place(x=75, y=45, width=100, height=20)

            in_log_process = True

            login_btn = Button(log_root, text='Регистрация', command=Register)
            login_btn.place(x=50, y=80, width=100, height=30)

            center(log_root)
            log_root.mainloop()


    login_btn = Button(text='Войти', command=Login)
    login_btn.place(x=25,y=240,width=100,height=30)

    reg_btn = Button(text='Регистрация', command=Register)
    reg_btn.place(x=125,y=240,width=100,height=30)

    start_pl_btn = Button(text='Против игрока', command=start_players)
    start_pl_btn.place(x=25, y=75, width=200, height=30)

    start_pl_btn = Button(text='Против компьютера (легко)', command=start_easy_bot)
    start_pl_btn.place(x=25, y=110, width=200, height=30)

    start_pl_btn = Button(text='Против компьютера (средне)', command=start_middle_bot)
    start_pl_btn.place(x=25, y=145, width=200, height=30)

    start_pl_btn = Button(text='Против компьютера (тяжело)', command=start_hard_bot)
    start_pl_btn.place(x=25, y=180, width=200, height=30)

    center(start_window)
    start_window.mainloop()

if __name__ == '__main__':
    main()
