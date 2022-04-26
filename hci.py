import argparse

from sympy import to_cnf, SympifyError

from knowledge_base import KnowledgeBase


def manual():
    print("Select an action among these:")
    print(
        """
    r: Perform and AGM belief revision
    e: Empty knowledge base
    p: Print knowledge base
    m: Print all available actions
    """
    )


def human_input(knowledge_base):
    action = input("What do you want to do?: ")

    if action == "r":
        print("####  Let's perform a AGM Revision  ####")
        print("Please enter a logical formula:")
        formula = input(">>> ")
        try:
            formula = to_cnf(formula)
            print("Select an order between 0 and 1:")
            order = input(">>> ")
            knowledge_base.agm_revise(formula, float(order))
        except SympifyError:
            print("####  Invalid formula  ####")
        except ValueError:
            print("####  The value for the order has to be between 0 and 1  ####")

    elif action == "e":
        knowledge_base.beliefs = {}
        print("####  Knowledge Base emptied  ####")

    elif action == "p":
        print("#### Here is your knowledge base:  ####")
        print(knowledge_base)
    elif action == "m":
        manual()

    else:
        print("####  Sorry, the command was not recognized. Type 'h' for help.  ####")

    human_input(knowledge_base)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    knowledge_base = KnowledgeBase()
    manual()
    human_input(knowledge_base)
