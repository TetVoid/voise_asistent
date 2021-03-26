from semanic_memory import Node, Action


class What(Action):
    def __init__(self, node ):
        self.subject_node = node
        self.mode = 0

    def run(self, info):
        if type(info[0]) == Node:
            if self.mode == 1:
                self.mode = 0
                return info[0].content
            elif self.mode == 2:
                self.mode = 0
                x = info[0].list_of_related_nodes[0].get_node(info[1])
                if x != "not found":
                    return x.content
                else:
                    return "у меня нет интересующий вас информации"

        else:
            return "Я не знаю что такое "+info[0]

class Is_decorator(Action):
    def __init__(self, decorate_node, mode):
        self.decorate_node = decorate_node
        self.mode = mode

    def run(self, params=None):
        self.decorate_node.mode = self.mode


def init_module():
    party = Node(word="вечеринка", node_tag="subject domain")
    what_action = What(party)
    what_node = Node(word="что", node_tag="action", action=what_action)

    is_decorator = Is_decorator(what_action, 2)
    how_many = Node(word="сколько", node_tag=["decorator", "synonym"], action=is_decorator)
    how_many.list_of_related_nodes.append(what_node)

    is_decorator = Is_decorator(what_action, 1)
    is_node = Node(word="такое", node_tag="decorator", action=is_decorator)

    is_synonym = Node(word="есть", node_tag="synonym")
    is_synonym.list_of_related_nodes.append(is_node)

    vodka = Node(word="водка", node_tag="param node", content="Крепкий алкогольный напиток, бесцветный водно-спиртовой раствор с характерным вкусом и ярко выраженным спиртовым запахом.")
    vodka_price = Node(word="стоит", node_tag="param node", content="5-12 рублей")
    vodka.list_of_related_nodes.append(vodka_price)

    hangover = Node(word="похмелье", node_tag="param node", content="Постинтоксикационное состояние вследствие злоупотребления алкогольными напитками")
    bar = Node(word="bar", node_tag="param node", content="Тип предприятия общественного питания, позиционирующаяся на алкогольных напитках")
    dance = Node(word="танец", node_tag="param node", content="Искусство пластических и ритмических движений")
    food = Node(word="закуска", node_tag="param node", content="Еда, которая подаётся перед основным блюдом, либо в качестве самостоятельной лёгкой трапезы")

    jin = Node(word="джин", node_tag="param node", content="Английская водка, перегнанная с можжевёловыми ягодами.")
    jin_price = Node(word="стоит", node_tag="param node", content="15-50 рублей")
    jin.list_of_related_nodes.append(jin_price)

    whiskey = Node(word="виски", node_tag="param node", content="Крепкий ароматный алкогольный напиток, получаемый из различных видов зерна с использованием процессов соложения, брожения, перегонки и длительного выдерживания в дубовых бочках.")
    whiskey_price = Node(word="стоит", node_tag="param node", content="20-60 рублей")
    whiskey.list_of_related_nodes.append(whiskey_price)

    party.add_node(what_node)
    party.add_node(is_node)
    party.add_node(vodka)
    party.add_node(hangover)
    party.add_node(bar)
    party.add_node(dance)
    party.add_node(food)
    party.add_node(jin)
    party.add_node(whiskey)
    party.add_node(how_many)
    party.add_node(is_synonym)

    return party