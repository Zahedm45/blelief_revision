IMPLICATION = "="
class CNF:



    def convert_to_cnf(self, proposition):
        for i in range(len(proposition) - 1):
            if proposition[i] == "=" and proposition[i+1] == ">":
                prop = self.find_prop(proposition, i)
                #print(prop)
                ##self.remove_implication(prop)



    def remove_implication(self, proposition):
        proposition = proposition.replace("=", "V", 1)
        proposition = proposition.replace(">", "", 1)
        proposition = "!" + proposition
        #print(proposition)


    def find_prop(self, prop, index):
        if prop[index - 1] != ")":
            return

        i = index-1
        open_parentheses = True
        left_part = ""
        parentheses1 = parentheses2 = 0

        # while True:
        #     str = prop[i]
        #     left_part = str + left_part
        #     if open_parentheses:
        #         if str == ")":
        #             parentheses1 += 1
        #         elif str == "(":
        #             open_parentheses = False
        #             parentheses2 += 1
        #
        #     else:
        #         if str == "(":
        #             parentheses2 += 1
        #
        #     if parentheses1 != 0:
        #         if parentheses1 == parentheses2:
        #             break
        #
        #         else:
        #             if str == "(":
        #                 parentheses2 += 1
        #
        #     i -= 1


        i = index+2
        parentheses1 = parentheses2 = 0
        open_parentheses = True
        right_part = ""

        while True:
            print(i)
            str = prop[i]
            right_part += str

            if str == "(":
                parentheses1 += 1
            elif str == ")":
                parentheses2 += 1
            if parentheses1 != 0:
                if parentheses1 == parentheses2:
                    break

            i += 1

        print(right_part)




cnf = CNF()
str = "(pVq)=>(!m)"
print("before: "+ str)
cnf.convert_to_cnf(str)



















