from random import randint
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageDraw
from re import findall

def recieve_image():
    global link_image
    filetypes = (('image files', '*.bmp'), ('All files', '*.*'))
    link_image = askopenfilename(title='Open a file', initialdir='./', filetypes=filetypes)

def clear_window():
    for widget in steganography.winfo_children()[3::]:
        widget.destroy()

def extraction_mode_do(link):
    a = []
    keys = []
    img = Image.open(link)
    pix = img.load()
    f = open('keys.txt', 'r')
    y = str([line.strip() for line in f])
    for i in range(len(findall(r'\((\d+)\,', y))):
        keys.append((int(findall(r'\((\d+)\,', y)[i]), int(findall(r'\,\s(\d+)\)', y)[i])))
    for key in keys:
        a.append(pix[tuple(key)][0])
    return ''.join([chr(elem) for elem in a])


def concealment_mode_do(link, text):
    img = Image.open(link)
    draw = ImageDraw.Draw(img)
    width = img.size[0]
    height = img.size[1]
    pix = img.load()
    f = open('keys.txt', 'w')
    for elem in ([ord(elem) for elem in text]):
        key = (randint(1, width - 10), randint(1, height - 10))
        g, b = pix[key][1:3]
        draw.point(key, (elem, g, b))
        f.write(str(key) + '\n')
    img.save("newimage.bmp", "BMP")
    f.close()


def extraction_mode_interface():
    link = Button(text="Выбрать изображение", command=recieve_image, width=20)
    link.place(anchor=N, relx=.5, rely=.2)

def concealment_mode_interface():
    global message
    link = Button(text="Выбрать изображение", command=recieve_image, width=20)
    save = Button(text="Сохранить преобразованное изображение", width=40)

    message = Entry(steganography, width=30)

    message.place(anchor=N, relx=.5, rely=.1)
    link.place(anchor=N, relx=.5, rely=.2)
    save.place(anchor=N, relx=.5, rely=.3)


def on_button():
    flag_mode = r_var.get()
    try:
        link = link_image
        if not flag_mode:
            text = message.get()
    except NameError:
        link = ""
        text = ""

    clear_window()

    if flag_mode:
        extraction_mode_interface()
        if len(link) > 0:
            print(extraction_mode_do(link))
    else:
        concealment_mode_interface()
        if len(link) > 0:
            concealment_mode_do(link, text)

# Основные настройки
steganography = Tk()
steganography.title('Стеганография')

# Радио-кнопки
r_var = BooleanVar()
r_var.set(0)
r1 = Radiobutton(text='Сокрытие', command=on_button, variable=r_var, value=0)
r2 = Radiobutton(text='Извлечение', command=on_button, variable=r_var, value=1)

# Кнопка
btn_send = Button(text='Отправить', command=on_button, width=30)

# Расположение
r1.place(anchor=NE, relx=.5)
r2.place(anchor=NW, relx=.5)
btn_send.place(anchor=N, relx=.5, rely=.4)

# Вызов функции
on_button()


# Настройки окна
steganography.geometry('920x700')
steganography.mainloop()
