import ttkbootstrap as ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from screeninfo import get_monitors
import subprocess
import os


# ----------------------------------------- Funciones ---------------------------------------------

def abrir_ventana_alerta(parent_window, success, error_type=0):
    def aceptar():
        alert_window.destroy()
        parent_window.focus_set()
        parent_window.grab_set()
        return

    monitors = get_monitors()

    window_width = monitors[1].width // 4
    window_heigth = monitors[1].height // 6
    window_x = monitors[1].x + monitors[1].x // 3
    window_y = monitors[1].y + monitors[1].y // 3

    # ventana

    alert_window = ttk.Toplevel(parent_window)
    alert_window.title('alerta - Error')
    if success:
        alert_window.title('alerta - lanzador creado exitosamente')
    alert_window.geometry(f'{window_width}x{window_heigth}+{window_x}+{window_y}')
    alert_window.focus_set()
    alert_window.grab_set()
    # alert_window.iconbitmap(parent_window.parent.icon_path)
    # self.iconbitmap(parent.icon_path) funciona en windows no en linux
    alert_window.wm_iconphoto(False, set_icon())

    # label

    label_alerta = ttk.Label(master=alert_window, text='Algo salio mal :(')
    if success:
        label_alerta = ttk.Label(master=alert_window, text='Lanzador creado exitosamente')
    label_alerta.configure(font='Arial 20 bold')

    msg = ttk.StringVar()
    label_msg = ttk.Label(master=alert_window, textvariable=msg, font='Arial 12 bold', wraplength=250)

    match error_type:
        case 1:
            msg.set('Debe ingresar un nombre para la aplicación')
        case 2:
            msg.set('Debe ingresar la ruta del ejecutable.jar')
        case 3:
            msg.set('Debe seleccionar una categoría (¿como mierda conseguiste llegar a este mensaje flaco?)')
        case _:
            msg.set('Error desconocido')
    # confirm_button

    button_confirm = ttk.Button(master=alert_window, text='Aceptar', style='success')
    button_confirm.configure(width=15, command=aceptar)

    # widget placing

    label_alerta.pack()
    button_confirm.place(relx=0.5, rely=0.8, anchor='center', width=100, height=40)
    if not success:
        label_msg.pack()
    # gestion de eventos

    alert_window.bind('<Return>', lambda *args: aceptar())

    # mainloop

    alert_window.mainloop()


def abrir_explorador(str_var):
    str_var.set(filedialog.askopenfilename())


def crear_exe(p_window, name, jar_route, icon_route, categorie):
    if icon_route == '':
        base_route = os.path.abspath('.')
        icon_route = os.path.join(base_route, 'AutoJar.png')
    error = 0
    if '' in (name, jar_route, categorie):
        if name == '':
            error = 1
        elif jar_route == '':
            error = 2
        elif categorie == '':
            error = 3
        abrir_ventana_alerta(parent_window=p_window, success=False, error_type=error)
    else:
        subprocess.run(['bash', 'crear_jar_icon.sh', jar_route, name, icon_route, categorie])
        abrir_ventana_alerta(parent_window=p_window, success=True)


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


# esto tiene que ser una función porque sino el garbage collector decide matar la referencia a img = Image.open() (Bruh)
def set_icon():
    img = Image.open('AutoJar_desk.png')
    icon = ImageTk.PhotoImage(img)
    return icon


def set_screen_geometry():
    monitores = get_monitors()
    pantalla_principal = monitores[1]
    win_width = pantalla_principal.width
    win_height = pantalla_principal.height
    center_x = pantalla_principal.x + win_width // 4
    center_y = pantalla_principal.y + win_height // 4

    return f'{win_width // 2}x{win_height // 2}+{center_x}+{center_y}'


# -----------------------------------------ventana_principal------------------------------------------------
window = ttk.Window(themename='journal')
window.title('Auto Jar')
window.geometry(set_screen_geometry())
window.wm_iconphoto(True, set_icon())

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
                           command=lambda: crear_exe(window, str_name.get(), str_route_jar.get(),
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

# labels
label_name.grid(row=1, column=0)
label_route.grid(row=2, column=0)
label_icon.grid(row=3, column=0)
label_cat.grid(row=4, column=0)
label_selected_cat.grid(row=4, column=1)

# entrys
entry_name.grid(row=1, column=1, pady=2)
entry_route.grid(row=2, column=1, pady=2)
entry_icon_route.grid(row=3, column=1, pady=2)
menu_categories.grid(row=4, column=3, pady=2)

# buttons
button_create.grid(row=5, column=1, padx=5, pady=20)
button_find.grid(row=2, column=3, padx=5, pady=2)
button_find_icon.grid(row=3, column=3, padx=5, pady=2)
input_frame.place(relx=0.5, rely=0.5, anchor='center')

# -----------------------------------------------Main loop---------------------------------------------------
window.mainloop()
