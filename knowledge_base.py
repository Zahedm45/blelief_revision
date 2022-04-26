import itertools

from sympy.logic.boolalg import to_cnf, And, Or, Equivalent
from entailment import do_entail


# class Belief:
#     def __init__(self, formula, order):
#         self.formula = formula
#         self.order = order

#     def __repr__(self):
#         return f"formula: {self.formula}, order: {self.order}"


def _is_tautology(formula):
    """
    Returns True if is a tautology.
    We use an empty knowledge base to confront the formula to itself
    """
    return do_entail([], formula)


def _is_contradiction(formula):
    """
    Check if formula is not a contradiction with empty knowledge base
    Example of a contradiciton: p & (~p)
    """
    return do_entail([], ~formula)


def dissociate(op, args):
    result = []

    def collect(subargs):
        for arg in subargs:
            if isinstance(arg, op):
                collect(arg.args)
            else:
                result.append(arg)

    collect(args)
    return result


def associate(op, args):
    args = dissociate(op, args)
    if len(args) == 0:
        return op.identity
    elif len(args) == 1:
        return args[0]
    else:
        return op(*args)


class KnowledgeBase:
    def __init__(self):
        self.knowledge_base = {}  # {formula: order}

    def expand(self, formula, order):
        formula = to_cnf(formula)

        if _is_contradiction(formula):
            return
        if _is_tautology(formula):
            order = 1
        else:
            for belief_formula, belief_order in self.knowledge_base.items():
                if belief_order > order:
                    # Befiefs of higher order shouldn't be impacted
                    continue

                d = self.degree(formula >> belief_formula)
                if (
                    do_entail([], Equivalent(formula, belief_formula))
                    or belief_order <= order < d
                ):
                    self.add_belief(belief_formula, order)
                else:
                    self.add_belief(belief_formula, d)
        self.add_belief(formula, order)

    def contract(self, formula, order):
        formula = to_cnf(formula)

        for belief_formula, belief_order in self.knowledge_base.items():
            if belief_order > order:
                dx = self.degree(formula)

                formula_or_belief = associate(Or, [formula, belief_formula])
                dxory = self.degree(formula_or_belief)

                if dx == dxory:
                    self.add_belief(belief_formula, order)

    def agm_revise(self, formula, order):
        formula = to_cnf(formula)

        if _is_contradiction(formula):
            return

        if _is_tautology(formula):
            order = 1

        elif order <= self.degree(formula):
            self.contract(formula, order)
        else:
            self.contract(~formula, 0)
            self.expand(formula, order)

    def add_belief(self, formula, order):
        self.knowledge_base[formula] = order

    def degree(self, formula):
        """
        Find maximum order j such that taking all beliefs in base
        with order >= j results in a belief set that entails formula.
        """

        formula = to_cnf(formula)
        if do_entail([], formula):
            # Tautologies have degree = 1
            return 1

        base = []

        for order, group in itertools.groupby(
            self.knowledge_base.items(), lambda item: item[1]
        ):
            # Get formulas from beliefs
            base += [formula for formula, _ in group]
            if do_entail(base, formula):
                return order
        return 0

    def __repr__(self):
        if len(self.knowledge_base.items()) == 0:
            return "Your knowledge base is empty"

        return "\n".join(
            [
                f"formula: {formula}, order: {order}"
                for formula, order in self.knowledge_base.items()
            ]
        )
