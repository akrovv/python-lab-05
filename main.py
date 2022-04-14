from tkinter import *
from PIL import Image, ImageTk
from tkinter import Tk, Button, Entry, Label
from tkinter.messagebox import showerror
from tkinter.filedialog import askopenfilename, asksaveasfilename


def show_image(img):
    img = ImageTk.PhotoImage(img)
    label = Label(steganography, image=img, width=250, height=250)
    label.image_ref = img
    label.grid(row=10, column=2, columnspan=100)


def save_img(img):
    files = (('image files', '*.bmp'), ('All files', '*.*'))
    lk = asksaveasfilename(title=u'save file ', initialdir='./', filetypes=files)
    img.save(str(lk))


def recieve_image():
    global link_image
    filetypes = (('image files', '*.bmp'), ('All files', '*.*'))
    link_image = askopenfilename(title='Open a file', initialdir='./', filetypes=filetypes)
    success_for_selected()


def clear_image():
    if len(steganography.winfo_children()) == 11:
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


def extraction_mode(pixels, create_mask):
    length = pixels[-1][2]
    degree = 1

    text_mask, img_mask = create_mask
    img_mask = ~img_mask

    k = 0
    kk = 0
    i = 0

    text = ''

    while i < length:
        symbol = 0
        for bits_read in range(0, 8, degree):
            img_byte = pixels[k][kk] & img_mask

            symbol <<= degree
            symbol |= img_byte

            kk += 1

            if kk == 3:
                kk = 0
                k += 1

        k += 1
        i += 1
        kk = 0

        text += chr(symbol)

    return text


def receive_byte_map(image, width, height):
    bytemap = []
    for i in range(width):
        for j in range(height):
            px = image.getpixel((i, j))
            x_1, x_2, x_3 = px
            bytemap.append([x_1, x_2, x_3])
    return bytemap


def put_modified_byte_map(image, width, height, res):
    k = 0
    for i in range(width):
        for j in range(height):
            px = tuple(res[k])
            image.putpixel((i, j), px)
            k += 1


def concealment_mode(image, pixels, text, create_mask):
    degree = 1
    text_mask, img_mask = create_mask

    k = 0
    kk = 0
    i = 0

    while i < len(text):
        symbol = ord(text[i])
        for byte_amount in range(0, 8, degree):
            img_byte = pixels[k][kk] & img_mask
            bits = symbol & text_mask

            bits >>= (8 - degree)

            img_byte |= bits
            pixels[k][kk] = img_byte

            symbol <<= degree

            kk += 1

            if kk == 3:
                kk = 0
                k += 1

        k += 1
        i += 1
        kk = 0

    pixels[-1][2] = len(text)
    return image


def success_for_save():
    lbl = Label(text="Успех сохранения: ")
    lbl.grid(row=3, column=0)


def success_for_selected():
    lbl = Label(text="Успех выбора: ")
    lbl1 = Label(text="Успех выбора: ")

    lbl.grid(row=5, column=0)
    lbl1.grid(row=2, column=0)



def success_for_concealment():
    lbl = Label(text="Успех сокрытия: ")
    lbl.grid(row=0, column=0)


def success_for_extraction():
    lbl = Label(text="Успех извлечения: ")
    lbl.grid(row=4, column=0)


def upload_image(link):
    image = Image.open(link)
    image = image.convert("RGB")
    width, height = image.size
    return image, width, height


def on_button(key):
    try:
        link = link_image
    except NameError:
        show_error()
        return 1

    text = message.get()
    img, width, height = upload_image(link)
    byte_map = receive_byte_map(img, width, height)

    if key == 1:
        concealment = concealment_mode(img, byte_map, text, create_mask(1))
        put_modified_byte_map(img, width, height, byte_map)
        save_img(concealment)
        success_for_save()
        success_for_concealment()
    elif key == 2:
        clear_message()
        show_message(extraction_mode(byte_map, create_mask(1)))
        success_for_extraction()
    else:
        clear_image()
        show_image(img)


# Основные настройки
steganography = Tk()
steganography.title('Стеганография')

# Label
lbl1 = Label(text="Сокрытие: ", font="Arial 20")
lbl2 = Label(text="Извлечение: ", font="Arial 20")
lbl3 = Label(text="Текст:")

# Кнопки
btn = Button(text="Показать изображение", command=lambda: on_button(3))
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
lbl3.grid(row=1, column=0)
link.grid(row=2, column=1, columnspan=10)
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
