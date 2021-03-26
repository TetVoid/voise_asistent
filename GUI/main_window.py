import os
import pickle
import modules.system as sys
from tkinter import Tk, Label, Entry, StringVar
from PIL import Image, ImageTk

import voise_treatment
from modules import party
from semanic_memory import SemanticMemory

SM = None
if os.path.exists('memory.pickle') is True:
    with open('memory.pickle', 'rb') as f:
        SM = pickle.load(f)
else:
    SM = SemanticMemory()
    sys_node = sys.init_module()
    party_node = party.init_module()
    SM.add_node(sys_node)
    SM.add_node(party_node)

root = Tk()
root.geometry("+%s+%s" % (1600, 200))

root["bg"] = "blue"
x = 0
y = 0


def StartMove(event):
    global x, y
    x = event.x
    y = event.y


def StopMove(event):
    global x, y
    x = None
    y = None


def OnMotion(event, window):
    global x, y
    deltax = event.x - x
    deltay = event.y - y
    x1 = window.winfo_x() + deltax
    y1 = window.winfo_y() + deltay
    window.geometry("+%s+%s" % (x1, y1))


buttoms_flag = True


def create_buttoms(event, buttoms, window):
    global buttoms_flag
    x = window.winfo_x()
    y = window.winfo_y()
    positions = [(0, 1), (2, 1), (1, 0), (1, 2)]
    if buttoms_flag:
        for index in range(len(buttoms)):
            buttoms[index].grid(row=positions[index][0], column=positions[index][1])
        buttoms_flag = False
        window.geometry("+%s+%s" % (x - 51, y - 51))
    else:
        for buttom in buttoms:
            buttom.grid_forget()
        buttoms_flag = True
        window.geometry("+%s+%s" % (x + 51, y + 51))


def Exit(event, window):
    SM.set_subject_domain([""])
    some_node = SM.get_node("пока")
    if some_node == "not found":
        with open('memory.pickle', 'wb') as f:
            pickle.dump(SM, f)
        window.quit()
    else:
        some_node.action.run("")
        with open('memory.pickle', 'wb') as f:
            pickle.dump(SM, f)
        window.quit()


voice_flag = False


def Voice_on_of(event, voice):
    global voice_flag
    if voice_flag:
        image = ImageTk.PhotoImage(Image.open("voise.png"))
        voice.configure(image=image)
        voice.image = image
        voice_flag = False
    else:
        image = ImageTk.PhotoImage(Image.open("voise_rec.png"))
        voice.configure(image=image)
        voice.image = image
        voice_flag = True


entry_flag = True


def show_entry(event, entry, buttom):
    global entry_flag
    if entry_flag:
        entry_image = ImageTk.PhotoImage(Image.open("entry.png"))
        buttom.configure(image=entry_image)
        buttom.image = entry_image
        buttom.grid(row=2, column=0, columnspan=3)
        entry.grid(row=2, column=0, columnspan=3)
        entry_flag = False
    else:
        entry_image = ImageTk.PhotoImage(Image.open("entry_def.png"))
        buttom.configure(image=entry_image)
        buttom.image = entry_image
        buttom.grid(row=2, column=1, columnspan=1)
        entry.grid_forget()
        entry_flag = True


output_flag = True


def show_output(event, entry, buttom):
    global output_flag
    if output_flag:
        entry_image = ImageTk.PhotoImage(Image.open("entry.png"))
        buttom.configure(image=entry_image)
        buttom.image = entry_image
        buttom.grid(row=0, column=0, columnspan=3)
        entry.grid(row=0, column=0, columnspan=3)
        output_flag = False
    else:
        entry_image = ImageTk.PhotoImage(Image.open("Ellipse.png"))
        buttom.configure(image=entry_image)
        buttom.image = entry_image
        buttom.grid(row=0, column=1, columnspan=1)
        entry.grid_forget()
        output_flag = True


def get_text(event, comand, entry, output):
    global entry_flag
    global SM
    global voice_flag
    if not entry_flag:
        decorators_list = []
        action_list = []
        words_params = []
        params_list = []

        if voice_flag:
            string = voise_treatment.recognize_text()
        else:
            string = comand.get()
        string_list = string.split(" ")

        SM.set_subject_domain(string_list)

        for word in string_list:
            some_nodes = SM.get_node(word)

            if type(some_nodes) == tuple:
                for some_node in some_nodes:
                    if some_node == "not found":
                        words_params.append(word)
                    elif "decorator" in some_node.node_tag:
                        decorators_list.append(some_node)
                    elif "action" in some_node.node_tag:
                        action_list.append(some_node)
                    elif "param node" in some_node.node_tag:
                        params_list.append(some_node)
            else:
                if some_nodes == "not found":
                    words_params.append(word)
                elif some_nodes.node_tag == "decorator":
                    decorators_list.append(some_nodes)
                elif some_nodes.node_tag == "action":
                    action_list.append(some_nodes)
                elif some_nodes.node_tag == "param node":
                    params_list.append(some_nodes)

        for dec in decorators_list:
            dec.action.run()

        result = ""
        params_list.extend(words_params)
        for act in action_list:
            result += " " + act.action.run(params_list)

        with open('memory.pickle', 'wb') as f:
            pickle.dump(SM, f)

        entry.delete(0, 'end')
        output.delete(0, 'end')
        output.insert(0, result)


button_list = []

image1 = ImageTk.PhotoImage(Image.open("Ellipse.png"))
image2 = ImageTk.PhotoImage(Image.open("entry_def.png"))
image3 = ImageTk.PhotoImage(Image.open("voise.png"))
image4 = ImageTk.PhotoImage(Image.open("exit.png"))

buttom1 = Label(root, image=image1, bg="blue")
output = Entry(root, width=16, font='Times 11')
buttom1.bind("<Button-1>", lambda e, r=output, b=buttom1: show_output(e, r, b))

buttom2 = Label(root, image=image2, bg="blue")
command = StringVar()
entry = Entry(root, width=16, font='Times 11', textvariable=command)
output.insert(0, "Приветствую")
buttom2.bind("<Button-1>", lambda e, r=entry, b=buttom2: show_entry(e, r, b))

buttom3 = Label(root, image=image3, bg="blue")
buttom3.bind("<Button-1>", lambda e, b=buttom3: Voice_on_of(e, b))

buttom4 = Label(root, image=image4, bg="blue")
buttom4.bind("<Button-1>", lambda e, r=root: Exit(e, r))

button_list.append(buttom1)
button_list.append(buttom2)
button_list.append(buttom3)
button_list.append(buttom4)

background = ImageTk.PhotoImage(Image.open("background.png"))
panel = Label(root, image=background, bg="blue")
panel.grid(row=1, column=1)

panel.bind("<ButtonPress-1>", StartMove)
panel.bind("<ButtonRelease-1>", StopMove)
panel.bind("<B1-Motion>", lambda e, f=root: OnMotion(e, f))

panel.bind("<Button-3>", lambda e, l=button_list, r=root: create_buttoms(e, l, r))

root.bind('<Return>', lambda e, c=command, i=entry, o=output: get_text(e, c, i, o))

root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.wm_attributes("-transparentcolor", "blue")
root.mainloop()
