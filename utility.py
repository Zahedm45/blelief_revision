
def find_prop(self, propo, index):
    connectivity = propo[index] + propo[index+1]
    if propo[index - 1] != ")":
        return

    i = index - 1
    left_side = ""
    parentheses1 = parentheses2 = 0

    while True:
        str = propo[i]
        left_side = str + left_side
        if str == ")":
            parentheses1 += 1
        elif str == "(":
            parentheses2 += 1
        i -= 1
        if parentheses1 != 0:
            if parentheses1 == parentheses2:
                break

    start_index = i

    i = index + 2
    parentheses1 = parentheses2 = 0
    right_side = ""
    while True:
        str = propo[i]
        right_side += str

        if str == "(":
            parentheses1 += 1
        elif str == ")":
            parentheses2 += 1

        i += 1
        if parentheses1 != 0:
            if parentheses1 == parentheses2:
                break

    end_index = i
    result = left_side + connectivity + right_side

    arr = {result, start_index, end_index}

    return arr