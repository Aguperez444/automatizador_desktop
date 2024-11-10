import ttkbootstrap as ttk
from tkinter import filedialog
import subprocess


# ----------------------------------------- Funciones ---------------------------------------------

def abrir_explorador(str_var):
    str_var.set(filedialog.askopenfilename())

def crear_exe(name, jar_route, icon_route, categorie):
    subprocess.run(['bash', 'crear_jar_icon.sh', jar_route, name, icon_route, categorie])

def traducir_categoria(categoria):
    categories_hashmap = {
        'Juego': 'Game',
        'Audio Video': 'AudioVideo',
        'Audio': 'Audio',
        'Video': 'Video',
        'Educación': 'Education',
        'Desarrollo': 'Development',
        'Gráficos': 'Graphics',
        'Redes': 'Network',
        'Oficina': 'Office',
        'Ciencia': 'Science',
        'Configuraciones': 'Settings',
        'Sistema': 'System',
        'Utilidad': 'Utility'
    }
    return categories_hashmap[categoria]

# -----------------------------------------ventana_principal------------------------------------------------
window = ttk.Window(themename='journal')
window.title('Automatizador crear exe')
window.geometry('1280x720')

# -----------------------------------------other_variables------------------------------------------------

categorias = ["Juego", "Audio Video", "Audio", "Video", "Educación", "Desarrollo", "Gráficos", "Redes",
              "Oficina", "Ciencia", "Configuraciones", "Sistema", "Utilidad"]
# -----------------------------------------ttk_variables------------------------------------------------


selection = ttk.StringVar()
str_route_icon = ttk.StringVar()
str_route_jar = ttk.StringVar()
str_name = ttk.StringVar()

selection.set(categorias[0])

input_frame = ttk.Frame(master=window)

button_create = ttk.Button(master=input_frame, text='Crear executable', width=18, style='success',
                           command=lambda: crear_exe(str_name.get(), str_route_jar.get(),
                                                    str_route_icon.get(), traducir_categoria(selection.get())))

button_find = ttk.Button(master=input_frame, text='buscar ruta', width=17,
                        command=lambda: abrir_explorador(str_route_jar))

button_find_icon = ttk.Button(master=input_frame, text='buscar ruta', width=17,
                              command=lambda: abrir_explorador(str_route_icon))

# -----------------------------------------bootstrap widgets------------------------------------------------
entry_route = ttk.Entry(master=input_frame, textvariable=str_route_jar, width=50)
entry_name = ttk.Entry(master=input_frame, textvariable=str_name, width=50)
entry_icon_route = ttk.Entry(master=input_frame, textvariable=str_route_icon, width=50)

menu_categories = ttk.OptionMenu(input_frame, selection, *categorias)
menu_categories.configure(width=14)

style = ttk.Style()
style.configure('Treeview', rowheight=30)

label_route = ttk.Label(master=input_frame, text='                 Ruta Jar:    ', anchor='e', font='arial 13')
label_name = ttk.Label(master=input_frame, text='                Nombre:    ', anchor='e', font='arial 13')
label_icon = ttk.Label(master=input_frame, text='                     Ruta Icono:    ', anchor='e', font='arial 13')
label_cat = ttk.Label(master=input_frame, text='                   Categoría:    ', anchor='e', font='arial 13')
label_selected_cat = ttk.Label(master=input_frame, textvariable=selection, anchor='e', font='arial 13')
# -----------------------------------------------packing---------------------------------------------------

#labels
label_name.grid(row=1, column= 0)
label_route.grid(row=2, column=0)
label_icon.grid(row=3, column= 0)
label_cat.grid(row=4, column= 0)
label_selected_cat.grid(row=4, column=1)

#entrys
entry_name.grid(row=1, column=1, pady=2)
entry_route.grid(row=2, column=1, pady=2)
entry_icon_route.grid(row=3, column=1, pady=2)
menu_categories.grid(row=4, column=3, pady=2)

#buttons
button_create.grid(row=5, column=1, padx=5, pady=20)
button_find.grid(row=2, column=3, padx=5, pady=2)
button_find_icon.grid(row=3, column=3, padx=5, pady=2)
input_frame.place(relx=0.5, rely=0.5, anchor='center')


# -----------------------------------------------Main loop---------------------------------------------------
window.mainloop()

