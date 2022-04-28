"""
Here are defined the entailment method. It uses various 
utils functions that enable us to parse the fomula"""

from sympy.logic.boolalg import Or, And, to_cnf


def do_entail(knowledge_base, formula_to_test):
    # #1 Convert KB ∧ ~phi to cnf
    formula_to_test = to_cnf(formula_to_test)
    clauses = []

    for clause in knowledge_base:
        clauses += conjuncts(clause)

    clauses += conjuncts(to_cnf(~formula_to_test))

    new = set()

    while True:
        clause_pairs = [
            (clauses[i], clauses[j])
            for i in range(len(clauses))
            for j in range(i + 1, len(clauses))
        ]

        for ci, cj in clause_pairs:
            resolvents = resolve(ci, cj)
            if False in resolvents:
                return True
            new = new.union(set(resolvents))

        if new.issubset(set(clauses)):
            return False

        for c in new:
            if c not in clauses:
                clauses.append(c)


def resolve(ci, cj):
    """
    Returns the set of all possible clauses obtained by resolving the inputs
    """

    clauses = []
    # Lets first dissociate the clauses
    ci_disjuncts = disjuncts(ci)
    cj_disjuncts = disjuncts(cj)

    for ci_disjunct in ci_disjuncts:
        for cj_disjunct in cj_disjuncts:
            if ci_disjunct == ~cj_disjunct or ~ci_disjunct == cj_disjunct:
                new = list(
                    set(
                        remove_from_array(ci_disjunct, ci_disjuncts)
                        + remove_from_array(cj_disjunct, cj_disjuncts)
                    )
                )
                clauses.append(associate(Or, new))
    return clauses


def remove_from_array(to_remove, to_remove_from):
    """
    Returns an array without 1 chosen element
    """
    return [elmt for elmt in to_remove_from if elmt != to_remove]


def disjuncts(cls):
    return dissociate(Or, [cls])


def conjuncts(cls):
    return dissociate(And, [cls])


def associate(op, args):
    """
    This method separates all of the args from an instance of logical
    formulae and associates them back together with the specified
    operator.
    """
    args = dissociate(op, args)
    if len(args) == 0:
        # True for 'And', False for 'Or'.
        return op.identity
    elif len(args) == 1:
        return args[0]
    else:
        return op(*args)


def dissociate(op, args):
    """
    This method separates the instances:
    e.g: (a|c) & (b|c) is an instance of And. Then its args are (a|c, b|c).
    We then recursively do this until we reach args that are not instances
    of the op.
    """
    result = []

    def collect(subargs):
        for arg in subargs:
            if isinstance(arg, op):
                collect(arg.args)
            else:
                result.append(arg)

    collect(args)
    return result
