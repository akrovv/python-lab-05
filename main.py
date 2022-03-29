from tkinter.constants import *
from PIL import Image, ImageTk
from tkinter import Tk, Button, Entry, BooleanVar, Radiobutton, Canvas, Frame
from tkinter.filedialog import askopenfilename
from os import stat
from sys import byteorder

def show_image():
    pass

def recieve_image():
    global link_image
    filetypes = (('image files', '*.bmp'), ('All files', '*.*'))
    link_image = askopenfilename(title='Open a file', initialdir='./', filetypes=filetypes)


def clear_window():
    for widget in steganography.winfo_children()[4::]:
        widget.destroy()


def create_mask(degree):
    text_mask = 0b11111111  # 255
    img_mask = 0b11111111

    text_mask <<= (8 - degree)
    text_mask %= 256  # 0-255

    img_mask >>= degree
    img_mask <<= degree

    return text_mask, img_mask


def extraction_mode_do(link):
    degree = 1

    text = ""
    encoded_bmp = open(link, 'rb')

    encoded_bmp.seek(54)

    text_mask, img_mask = create_mask(degree)
    img_mask = ~img_mask

    while True:
        symbol = 0

        for bits_read in range(0, 8, degree):
            img_byte = int.from_bytes(encoded_bmp.read(1), byteorder) & img_mask

            symbol <<= degree
            symbol |= img_byte

        if symbol < 32 or symbol > 126:
            break

        text += chr(symbol)

    encoded_bmp.close()

    return text


def concealment_mode_do(link, text):
    degree = 1

    if len(text) >= stat(link).st_size * 1 / 8 - 54:
        return 1

    start_bmp = open(link, 'rb')
    encode_bmp = open('encoded.bmp', 'wb')

    first54 = start_bmp.read(54)
    encode_bmp.write(first54)

    text_mask, img_mask = create_mask(degree)

    i = 0
    while i < len(text):
        symbol = ord(text[i])

        for byte_amount in range(0, 8, degree):
            img_byte = int.from_bytes(start_bmp.read(1), byteorder) & img_mask
            bits = symbol & text_mask

            bits >>= (8 - degree)

            img_byte |= bits
            encode_bmp.write(img_byte.to_bytes(1, byteorder))

            symbol <<= degree

        i += 1

    encode_bmp.write(start_bmp.read())

    start_bmp.close()
    encode_bmp.close()

    return 0


def extraction_mode_interface():
    link = Button(text="Выбрать изображение", command=recieve_image, width=20)
    link.place(anchor=N, relx=.5, rely=.2)


def concealment_mode_interface():
    global message
    link = Button(text="Выбрать изображение", command=recieve_image, width=20)

    message = Entry(steganography, width=30)

    message.place(anchor=N, relx=.5, rely=.1)
    link.place(anchor=N, relx=.5, rely=.2)


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

# canvas = Canvas(steganography, width=500, height=500)
# pilImage = Image.open("sample_640×426.bmp").resize((300, 250))
# image = ImageTk.PhotoImage(pilImage)
# imagesprite = canvas.create_image(400, 400, image=image)

# Радио-кнопки
r_var = BooleanVar()
r_var.set(0)
r1 = Radiobutton(text='Сокрытие', command=on_button, variable=r_var, value=0)
r2 = Radiobutton(text='Извлечение', command=on_button, variable=r_var, value=1)

# Кнопки
btn = Button(text="Показать изображение", command=show_image)
save = Button(text="Сохранить преобразованное изображение", command=on_button)

# Расположение
r1.place(anchor=NE, relx=.5)
r2.place(anchor=NW, relx=.5)
save.place(anchor=N, relx=.5, rely=.3)
btn.place(anchor=N, relx=.5, rely=.4)


# Вызов функции
on_button()

# Настройки окна
steganography.geometry('920x700')
steganography.mainloop()
