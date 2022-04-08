from tkinter import *
import numpy as np
from PIL import Image, ImageTk
from tkinter import Tk, Button, Entry, Label
from tkinter.messagebox import showerror
from tkinter.filedialog import askopenfilename, asksaveasfilename

def show_image(link):
    img = ImageTk.PhotoImage(Image.open(link))
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
    message1.config(state=NORMAL)
    message1.insert(0, text)
    message1.config(state=DISABLED)

def show_error():
    showerror("Ошибка", "Пустое поле ввода")

def extraction_mode(src):
    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))
    n = 3

    total_pixels = array.size // n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i + 8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    for i in range(len(hidden_bits)):
        if message[-5:] == "$t3g0":
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    if "$t3g0" in message:
        return message[:-5]

def concealment_mode(src, message):
    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))
    n = 3

    total_pixels = array.size // n

    message += "$t3g0"
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    if req_pixels > total_pixels:
        return 0
    else:
        index = 0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                    index += 1

        array = array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
    return enc_img

def concealment_mode_save(dest, enc):
    enc.save(dest)

def on_button(key):
    try:
        link = link_image
    except NameError:
        show_error()
        return 1
    text = message.get()

    if key == 1:
        name = save_img()
        concealment = concealment_mode(link, text)
        concealment_mode_save(name, concealment)
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