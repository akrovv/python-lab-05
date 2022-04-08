from tkinter import *
from PIL import Image, ImageTk
from tkinter import Tk, Button, Entry, Label
from tkinter.messagebox import showerror
from tkinter.filedialog import askopenfilename, asksaveasfilename
from os import stat
from sys import byteorder

def show_image(link):
    img = ImageTk.PhotoImage(Image.open('newimage.bmp'))
    label = Label(steganography, image=img, width=250, height=250)
    label.image_ref = img
    label.grid(row=10, column=2, columnspan=100)

def save_img():
    files = (('image files', '*.bmp'), ('All files', '*.*'))
    lk = asksaveasfilename(title=u'save file ', initialdir='./' ,filetypes=files)
    return lk

def recieve_image():
    global link_image
    filetypes = (('image files', '*.bmp'), ('All files', '*.*'))
    link_image = askopenfilename(title='Open a file', initialdir='./', filetypes=filetypes)

def clear_img():
    if len(steganography.winfo_children()) == 10:
        steganography.winfo_children()[-1].destroy()

def clear_message():
    message1.config(state=NORMAL)
    message1.delete(0, END)
    message1.config(state=DISABLED)
    message.delete(0, END)

def show_message(text):
    text = text[:-1]
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

def get_pixel(width,height,image):
    res = []
    temp = []
    for i in range(width):
        for j in range(height):
            px = image.getpixel((i, j))
            x_1, x_2, x_3 = px
            temp.append(x_1)
            temp.append(x_2)
            temp.append(x_3)
            res.append(temp)
            temp = []
    return res

def concealment_mode_save(link, name, array):
    start_bmp = open(link, 'rb')
    encode_bmp = open(name, 'wb')

    first54 = start_bmp.read(54)
    encode_bmp.write(first54)

    for i in range(len(array)):
        encode_bmp.write(array[i])

    encode_bmp.write(start_bmp.read())

    start_bmp.close()
    encode_bmp.close()

def concealment_mode(link, text):
    degree = 1

    if len(text) >= stat(link).st_size * 1 / 8 - 54:
        return 0

    text_mask, img_mask = create_mask(degree)

    image = Image.open(link)
    width, height = image.size
    pixels = get_pixel(width, height, image)
    array_pixels = []

    i = 0
    j = 0

    while i < len(text):
        symbol = ord(text[i])
        px = pixels[i][j]
        for byte_amount in range(0, 8, degree):
            img_byte = px & img_mask
            bits = symbol & text_mask

            bits >>= (8 - degree)

            img_byte |= bits
            array_pixels.append(img_byte.to_bytes(1, byteorder))

            symbol <<= degree

        i += 1
        j += 1
        if j >= 2:
            j = 0

    return array_pixels

def on_button(key):
    try:
        link = link_image
    except NameError:
        show_error()
        return 1
    text = message.get()

    if key == 1:
        concealment = concealment_mode(link, text)
        if type(concealment) == int:
            return 1
        name = save_img()
        concealment_mode_save(link, name, concealment)
    elif key == 2:
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
lbl3 = Label(text="Текст:")

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
message.grid(row=2, column=1, columnspan=10)
lbl3.grid(row=1, column=1)
link.grid(row=3, column=1, columnspan=10)
save.grid(row=4, column=1)
lbl2.grid(row=5, column=1)
link2.grid(row=6, column=1, columnspan=6)
sh_m.grid(row=7, column=1)
message1.grid(row=8, column=1, columnspan=10)
btn.grid(row=9, column=1, columnspan=6)

# Режим
message1.config(state=DISABLED)

# Настройки окна
steganography.geometry('920x700')
steganography.mainloop()