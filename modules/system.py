from tkinter import Tk
import win32clipboard
import os
import pyautogui as pyautogui

from semanic_memory import Node
from semanic_memory import Action


class Delete_node_action(Action):
    def __init__(self, node):
        self.subject_node = node
        self.mode = 0

    def run(self, params=None):
        if len(params) != 0:
            if type(params[0]) == Node:
                parent = self.subject_node.get_parent_node(params[0].word)
                params[0].delete(parent)
                del params[0]
                return " "
            else:
                return "Нет переменной с именем "+params[0]


class Open_dir_action(Action):
    def __init__(self, node):
        self.subject_node = node
        self.mode = 0

    def run(self, params):
        path = params[0].content
        path = os.path.realpath(path)
        os.startfile(path)
        return " "

class Create_param_action(Action):
    def __init__(self, node):
        self.subject_node = node
        self.mode = 0

    def run(self, params):
        if self.mode == 0:
            if type(params[0]) == Node:
                return "Переменная с именем " + params[0].word + " уже записана"
            param_node = Node()
            param_node.word = params[0]

            content = ""
            for i in range(1, len(params)):
                content += params[i]

            param_node.content = content
            param_node.node_tag = "param node"
            self.subject_node.add_node(param_node)

        elif self.mode == 1:
            pyautogui.hotkey('ctrl', 'c')
            win32clipboard.OpenClipboard()
            content = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            if type(params[0]) != Node:
                param_node = Node()
                param_node.word = params[0]
                param_node.content = content
                param_node.node_tag = "param node"
                self.subject_node.add_node(param_node)
            else:
                param_node = params[0]
                param_node.content = content
        self.mode = 0
        return "Переменная сохранена"


class Create_decorator(Action):
    def __init__(self, action):
        self.decorated_action = action
        self.mode = 1

    def run(self, params=None):
        self.decorated_action.mode = self.mode


class Print_action(Action):
    def __init__(self, node):
        self.subject_node = node

    def run(self, info):
        if type(info[0]) == Node:
            return info[0].content
        else:
            return info[0]


def init_module():
    system = Node(word="система", node_tag="subject domain")

    create_action = Create_param_action(system)
    create_param = Node(word="создать", node_tag="action", action=create_action)

    synonym_create1 = Node(word="сохранить", node_tag="synonym")
    synonym_create1.list_of_related_nodes.append(create_param)

    synonym_create2 = Node(word="запомнить", node_tag="synonym")
    synonym_create2.list_of_related_nodes.append(create_param)

    create_decorator = Node(word="выделить", node_tag="decorator")
    create_decorator.action = Create_decorator(create_action)

    print_node = Node(word="вывести", node_tag="action", action=Print_action(system))

    open_action = Open_dir_action(system)
    open_dir_node = Node(word="открыть", node_tag="action", action=open_action)

    delete_node_action = Delete_node_action(system)
    delete_node = Node(word="удалить", node_tag="action", action=delete_node_action)

    synonym_delete1 = Node(word="забыть", node_tag="synonym")
    synonym_delete1.list_of_related_nodes.append(delete_node)

    system.add_node(create_param)
    system.add_node(print_node)
    system.add_node(synonym_create1)
    system.add_node(synonym_create2)
    system.add_node(create_decorator)
    system.add_node(open_dir_node)
    system.add_node(delete_node)
    system.add_node(synonym_delete1)

    return system

