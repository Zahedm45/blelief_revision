from entailment import do_entail


def _is_tautology(formula):
    """
    Returns True if is a tautology. Tautology have order of 1
    We use an empty knowledge base to confront the formula to itself
    """
    return do_entail([], formula)


def _is_contradiction(formula):
    """
    Check if formula is not a contradiction with empty knowledge base
    Example of a contradiciton: p & (~p)
    """
    return do_entail([], ~formula)
