from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image

def recieve_image():
    filetypes = (('image files', '*.bmp'), ('All files', '*.*'))
    link = askopenfilename(title='Open a file', initialdir='./', filetypes=filetypes)
    print(link)
    return link

def change_mode(mode):
    if mode:
        pass


def on_button():
    flag_mode = r_var.get()
    change_mode(flag_mode)
    recieve_image()


# Основные настройки
steganography = Tk()
steganography.title('Стеганография')

# Поле ввода
message = Entry(steganography, width=30)

# Кнопка
link = Button(text="Выбрать изображение", command=recieve_image, width=20)

# Label
strings_message = Label(text="Строка:", width=20, height=10)

# Радио-кнопки
r_var = BooleanVar()
r_var.set(0)
r1 = Radiobutton(text='Сокрытие', command=on_button, variable=r_var, value=0)
r2 = Radiobutton(text='Извлечение', command=on_button, variable=r_var, value=1)

# Расположение кнопок, полей ввода
r1.place(anchor=NE, relx=.5)
r2.place(anchor=NW, relx=.5)
message.place(anchor=N, relx=.5, rely=.1)
strings_message.place(anchor=NE, relx=.4)
link.place(anchor=N, relx=.5, y=100)

# Настройки окна
steganography.geometry('920x700')
steganography.mainloop()
