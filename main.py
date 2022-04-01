from tkinter import  *
from PIL import Image, ImageTk
from tkinter import Tk, Button, Entry, Label, Frame, Canvas
from tkinter.messagebox import showerror
from tkinter.filedialog import askopenfilename
from os import stat
from sys import byteorder

def show_image(link):
    img = ImageTk.PhotoImage(Image.open(link))
    label = Label(steganography, image=img, width=250, height=250)
    label.image_ref = img
    label.grid(row=10, column=2, columnspan=100)

def recieve_image():
    global link_image
    filetypes = (('image files', '*.bmp'), ('All files', '*.*'))
    link_image = askopenfilename(title='Open a file', initialdir='./', filetypes=filetypes)

def clear_img():
    if  len(steganography.winfo_children()) == 10:
        steganography.winfo_children()[-1].destroy()

def clear_message():
    message1.config(state=NORMAL)
    message1.delete(0, END)
    message1.config(state=DISABLED)
    message.delete(0, END)

def show_message(text):
    message1.config(state=NORMAL)
    message1.insert(0, text)
    message1.config(state=DISABLED)

def show_error():
    showerror("Ошибка", "Пустое поле ввода")

def create_mask(degree):
    text_mask = 0b11111111  # 255
    img_mask = 0b11111111

    text_mask <<= (8 - degree)
    text_mask %= 256  # 0-255

    img_mask >>= degree
    img_mask <<= degree

    return text_mask, img_mask


def extraction_mode(link):
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


def concealment_mode(link, text):
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

def on_button(key):
    try:
        link = link_image
    except NameError:
        show_error()
        return 1
    text = message.get()

    if key == 1:
        concealment_mode(link, text)
    elif key == 2:
        link = "encoded.bmp"
        clear_message()
        show_message(extraction_mode(link))
    else:
        clear_img()
        show_image(link)




# Основные настройки
steganography = Tk()
steganography.title('Стеганография')

# Label
lbl1 = Label(text="Сокрытие: ", font="Arial 20")
lbl2 = Label(text="Извлечение: ", font="Arial 20")

# Кнопки
btn = Button(text="Показать изображение", command=lambda : on_button(3))
save = Button(text="Сохранить преобразованное изображение", command=lambda: on_button(1))
sh_m = Button(text="Показать сообщение", command=lambda: on_button(2))

# Извлечение
link2 = Button(text="Выбрать изображение", command=recieve_image, width=20)
message1 = Entry(steganography, width=30)

# Сокрытие
link = Button(text="Выбрать изображение", command=recieve_image, width=20)
message = Entry(steganography, width=30)

# Расположение
lbl1.grid(row=0, column=1)
message.grid(row=1, column=1, columnspan=10)
link.grid(row=2, column=1, columnspan=6)
save.grid(row=3, column=1)
lbl2.grid(row=4, column=1)
link2.grid(row=5, column=1, columnspan=6)
sh_m.grid(row=6, column=1)
message1.grid(row=7, column=1, columnspan=10)
btn.grid(row=8, column=1, columnspan=6)

# Режим
message1.config(state=DISABLED)

# Настройки окна
steganography.geometry('920x700')
steganography.mainloop()