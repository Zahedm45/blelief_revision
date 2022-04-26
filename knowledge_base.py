import itertools

from sympy.logic.boolalg import to_cnf, And, Or, Equivalent
from entailment import do_entail
from utils import _is_contradiction, _is_tautology


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

                d = self.max_order_before_entail(formula >> belief_formula)
                if (
                    _is_tautology(Equivalent(formula, belief_formula))
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

                formula_or_belief = associate(Or, [formula, belief_formula])

                if self.max_order_before_entail(
                    formula
                ) == self.max_order_before_entail(formula_or_belief):
                    self.add_belief(belief_formula, order)

    def agm_revise(self, formula, order):
        formula = to_cnf(formula)

        if _is_contradiction(formula):
            return

        if _is_tautology(formula):
            order = 1

        elif order <= self.max_order_before_entail(formula):
            self.contract(formula, order)
        else:
            self.contract(~formula, 0)
            self.expand(formula, order)

    def add_belief(self, formula, order):
        self.knowledge_base[formula] = order

    def max_order_before_entail(self, formula):
        """
        Return the maximum order that for which all the beliefs with higher
        order entail this formula.
        """

        formula = to_cnf(formula)
        if _is_tautology(formula):
            return 1

        base = []
        # This loops through grouped belief. They are grouped by order
        # and sorted by order desc
        for order, group in sorted(
            itertools.groupby(self.knowledge_base.items(), lambda item: item[1]),
            key=lambda x: -x[0],
        ):
            base += [formula for formula, _ in group]
            if do_entail(base, formula):
                return order

        return 0

    def __repr__(self):
        """
        This method override the native one in order to make it readable in the HCI
        """

        if len(self.knowledge_base.items()) == 0:
            return "Your knowledge base is empty"

        return "\n".join(
            [
                f"formula: {formula}, order: {order}"
                for formula, order in self.knowledge_base.items()
            ]
        )
