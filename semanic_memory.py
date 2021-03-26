from abc import ABC, abstractmethod
from pymorphy2 import MorphAnalyzer

class Action(ABC):
    @abstractmethod
    def run(self, params):
        pass


class Node:
    def __init__(self, word="", node_tag="", content="", action=None):
        self.word = word
        self.node_tag = node_tag
        self.content = content
        self.action = action
        self.list_of_related_nodes = []
        self.left_node = None
        self.right_node = None

    def validate(self, node_name):
        morph = MorphAnalyzer()
        list = morph.parse(node_name)
        for i in list:
            if i.normal_form == self.word:
                return True

    def add_node(self, node):
        if self.word > node.word:
            if self.left_node is None:
                self.left_node = node
            else:
                self.left_node.add_node(node)
        else:
            if self.right_node is None:
                self.right_node = node
            else:
                self.right_node.add_node(node)

    def get_node(self, string):
        if self.word == string:
            return self
        else:
            if self.word > string:
                if self.left_node is not None:
                    return self.left_node.get_node(string)
            else:
                if self.right_node is not None:
                    return self.right_node.get_node(string)
        return "not found"

    def get_parent_node(self, string):
        if self.left_node is not None:
            if self.left_node.word == string:
                return self
        if self.right_node is not None:
            if self.right_node.word == string:
                return self

        if self.word > string:
            if self.left_node is not None:
                return self.left_node.get_parent_node(string)
        else:
            if self.right_node is not None:
                return self.right_node.get_parent_node(string)
        return "not found"

    def delete(self, parent):
        if parent.right_node is not None:
            if parent.right_node.word == self.word:
                if self.right_node is not None:
                    parent.right_node = self.right_node
                    if self.left_node is not None:
                        self.right_node.add_node(self.left_node)
                else:
                    parent.right_node = None
                    if self.left_node is not None:
                        parent.right_node = self.left_node

        if parent.left_node is not None:
            if parent.left_node.word == self.word:
                if self.left_node is not None:
                    parent.left_node = self.left_node
                    if self.right_node is not None:
                        self.left_node.add_node(self.right_node)
                else:
                    parent.left_node = None
                    if self.right_node is not None:
                        parent.left_node = self.right_node

class Init_action(Action):
    def __init__(self, head, root, SM):
        self.head = head
        self.root = root
        self.SM = SM

    def run(self, params):
        self.head = self.root
        if self.SM.mode:
            self.SM.mode = False
            return "Надеюсь я смогла вам помочь."
        else:
            self.SM.mode = True
            return "Чем я могу вам помочь?"



class SemanticMemory:
    def __init__(self):
        self.mode = False
        self.root_node = Node()
        self.head_node = Node()

        init_action = Init_action(self.head_node, self.root_node, self)
        self.hello_node = Node(word="привет", node_tag="action", action=init_action)

        synonym_hello1 = Node(word="здравствуй", node_tag="synonym")
        synonym_hello1.list_of_related_nodes.append(self.hello_node)

        synonym_hello2 = Node(word="приведствие", node_tag="synonym")
        synonym_hello2.list_of_related_nodes.append(self.hello_node)


        self.hello_node.add_node(synonym_hello1)
        self.hello_node.add_node(synonym_hello2)


    def add_node(self, node):
        if self.root_node.word == "":
            self.root_node = node
            close_action = Init_action(self.head_node, self.hello_node, self)
            by_node = Node(word="пока", node_tag="action", action=close_action)

            synonym_by = Node(word="прощай", node_tag="synonym")
            synonym_by.list_of_related_nodes.append(by_node)

            self.add_node(by_node)
            self.add_node(synonym_by)
        else:
            self.root_node.add_node(node)

    def get_node(self, string):
        morph = MorphAnalyzer()
        list_of_words = morph.parse(string)
        words = []
        for i in list_of_words:
            if i.normal_form not in words:
                words.append(i.normal_form)
        words.append(string)
        answer = None

        for i in words:
            answer = self.head_node.get_node(i)
            if answer != "not found":
                if type(answer.node_tag) == list:
                    if "synonym" in answer.node_tag:
                        return answer.list_of_related_nodes[0], answer
                if "synonym" == answer.node_tag:
                    return answer.list_of_related_nodes[0]
                else:
                    break

        return answer

    def set_subject_domain(self, words):
        if self.mode:
            subject_domain = self.root_node
        else:
            subject_domain = self.hello_node

        for word in words:
            answer = subject_domain.get_node(word)
            if answer != "not found":
                if answer.node_tag == "subject domain":
                    subject_domain = answer
                if answer.node_tag == "synonym":
                    for synonym_of in answer.list_of_related_nodes:
                        if synonym_of.node_tag == "subject domain":
                            subject_domain = synonym_of


        self.head_node = subject_domain





