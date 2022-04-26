from sympy.logic.boolalg import to_cnf


def junct(s, operator):
    if s == operator:
        return s.args
    else:
        return [s]


def removeall(to_remove, to_remove_from):
    return [elmt for elmt in to_remove_from if elmt != to_remove]


def do_entail(knowledge_base, formula_to_test):
    # #1 Convert KB ∧ ~phi to cnf
    clauses = [junct(clause, "&") for clause in knowledge_base] + junct(
        to_cnf(~formula_to_test), "&"
    )

    new = set()

    while True:
        clause_pairs = [
            (clauses[i], clauses[j])
            for i in range(len(clauses))
            for j in range(i + 1, len(clauses))
        ]

        for (ci, cj) in clause_pairs:
            resolvents = resolve(ci, cj)
            if False in resolvents:
                return True
            new.union_update(set(resolvents))

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

    for di in junct(ci, "|"):
        for dj in junct(cj, "|"):
            if di == ~dj or ~di == dj:
                new = list(
                    set((removeall(di, junct(ci, "|")) + removeall(dj, junct(cj, "&"))))
                )
                clauses.append(to_cnf("|".join(new)))
    return clauses
