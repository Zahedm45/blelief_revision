from sympy.logic.boolalg import Or, And, to_cnf


def junct(s, operator):
    if s == operator:
        return s.args
    else:
        return [s]


def removeall(to_remove, to_remove_from):
    return [elmt for elmt in to_remove_from if elmt != to_remove]


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


def disjuncts(clause):
    return dissociate(Or, [clause])


def conjuncts(clause):
    return dissociate(And, [clause])


def associate(op, args):
    args = dissociate(op, args)
    if len(args) == 0:
        return op.identity
    elif len(args) == 1:
        return args[0]
    else:
        return op(*args)


def dissociate(op, args):
    result = []

    def collect(subargs):
        for arg in subargs:
            # e.g: (a|c) & (b|c) is an instance of And. Then its args are (a|c, b|c).
            # We then recursively do this until we reach args that are not instances
            # of the op.
            if isinstance(arg, op):
                collect(arg.args)
            else:
                result.append(arg)

    collect(args)
    return result


def resolve(ci, cj):
    """
    Returns the set of all possible clauses obtained by resolving the inputs
    """

    clauses = []

    ci_disjuncts = disjuncts(ci)
    cj_disjuncts = disjuncts(cj)

    for ci_disjunct in ci_disjuncts:
        for cj_disjunct in cj_disjuncts:
            if ci_disjunct == ~cj_disjunct or ~ci_disjunct == cj_disjunct:
                new = list(
                    set(
                        removeall(ci_disjunct, ci_disjuncts)
                        + removeall(cj_disjunct, cj_disjuncts)
                    )
                )
                clauses.append(associate(Or, new))
    return clauses
