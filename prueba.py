from tkinter import *
from tkinter import filedialog as fd
from bitstring import *
from tkinter import messagebox

# Para hacer la interfaz grafica usamos la libreria tkinter que viene con python
window = Tk()
window.title("COMPRESOR LZW")
window.geometry('500x300')

lbl = Label(window, text="")
lbl.grid(column=0, row=1)
lbl2 = Label(window, text="")
lbl2.grid(column=0, row=5)
rutaArchivo=""
rutaArchivo2=""


def clicked():
    # Seleccionamos un archivo con la ayuda de filedialog
    global rutaArchivo
    rutaArchivo = fd.askopenfilename(initialdir="./", title="Seleccione archivo",
                                     filetypes=(("todos los archivos", "*.*"),("WAVE files", "*.wav")))
    if rutaArchivo != '':
        contenido="Archivo Seleccionado: " + rutaArchivo
    else:
        contenido="No ha seleccionado ningún Archivo"

    lbl.config(text=contenido)
    return rutaArchivo

def clicked2():
    # Seleccionamos un archivo con la ayuda de filedialog
    global rutaArchivo2
    rutaArchivo2 = fd.askopenfilename(initialdir="./", title="Seleccione archivo",
                                     filetypes=(("SG files", "*.sg"),("SimonGui", "*.SG")))
    if rutaArchivo2 != '':
        contenido="Archivo Seleccionado: " + rutaArchivo2
    else:
        contenido="No ha seleccionado ningún Archivo"

    lbl2.config(text=contenido)
    return rutaArchivo2

def comprimir():
    # Build the dictionary.
    dict_size = 256
    dictionary = dict((chr(i), i) for i in range(dict_size))
    # in Python 3: dictionary = {chr(i): i for i in range(dict_size)}

    with open(rutaArchivo, "r") as f:

        byte = f.read(1)
        w = ""
        result = BitStream()
        bits = 9
        while byte:
            c = byte
            wc = w + c
            if wc in dictionary:
                w = wc
            else:
                result.append('uint:'+str(bits)+'='+str(dictionary[w]))
                print(dictionary[w])
                print(result.bin)
                dictionary[wc] = dict_size
                dict_size += 1
                if dict_size > pow(2,bits):
                    bits+=1
                w = c
            byte = f.read(1)

        if w:
            result.append('uint:9='+str(dictionary[w]))


        comprimido = open("compri.sg", "wb")
        # comprimido.write(result.tobytes())
        result.tofile(comprimido)
        comprimido.close()



def decompress():
    """Decompress a list of output ks to a string."""
    from io import StringIO

    # Build the dictionary.
    dict_size = 256
    bits=9
    #dictionary = dict((i, chr(i)) for i in range(dict_size))
    dictionary = {i: chr(i) for i in range(dict_size)}
    # in Python 3: dictionary = {i: chr(i) for i in range(dict_size)}

    # use StringIO, otherwise this becomes O(N^2)
    # due to string concatenation in a loop
    result = open("compri.txt", "w")
    compressed= ConstBitStream(filename=rutaArchivo2)
    w = chr(compressed.read('uint:'+str(bits)))
    result.write(w)
    k = compressed.read('uint:'+str(bits))
    while compressed.pos+bits <= compressed.len:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.write(entry)

        # Add w+entry[0] to the dictionary.
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        if dict_size >= pow(2,bits):
            bits += 1

        w = entry

        k=compressed.read('uint:'+str(bits))

    result.write(dictionary[k])
    result.close()



btn = Button(window, text="Seleccionar Archivo a Comprimir", command=clicked, anchor=CENTER)
btn.grid(column=0, row=0)
btn2 = Button(window, text="Comprimir", command=comprimir, anchor=CENTER)
btn2.grid(column=0 ,  row=2)

btn3 = Button(window, text="Seleccionar Archivo a Descomprimir", command=clicked2, anchor=CENTER)
btn3.grid(column=0 ,  row=4)
btn4 = Button(window, text="Descomprimir", command=decompress, anchor=CENTER)
btn4.grid(column=0 ,  row=6)

window.mainloop()



