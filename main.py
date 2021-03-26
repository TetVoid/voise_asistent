import os

import voise_treatment
from semanic_memory import SemanticMemory
import modules.system as sys
import pickle

if __name__ == '__main__':
    if os.path.exists('memory.pickle') is True:
        with open('memory.pickle', 'rb') as f:
            SM = pickle.load(f)
    else:
        SM = SemanticMemory()
        sys_node = sys.init_module()
        SM.add_node(sys_node)

    while True:
        decorators_list = []
        action_list = []
        words_params = []
        params_list = []

        #string = voise_treatment.recognize_text()

        string = "забудь имя"
        print(string)
        string_list = string.split(" ")

        SM.set_subject_domain(string_list)

        for word in string_list:
            some_node = SM.get_node(word)

            if some_node == "not found":
                words_params.append(word)
            elif some_node.node_tag == "decorator":
                decorators_list.append(some_node)
            elif some_node.node_tag == "action":
                action_list.append(some_node)
            elif some_node.node_tag == "param node":
                params_list.append(some_node)

        for dec in decorators_list:
            dec.action.run()

        params_list.extend(words_params)
        for act in action_list:
            act.action.run(params_list)

        with open('memory.pickle', 'wb') as f:
            pickle.dump(SM, f)
