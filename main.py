from utility import find_prop

IMPLICATION = "="


class CNF:

    def convert_to_cnf(self, proposition):
        for i in range(len(proposition) - 1):
            if proposition[i] == "=" and proposition[i + 1] == ">":
                old_val = self.find_proposition(proposition, i)
                new_val = self.remove_implication(old_val)
                proposition = self.replace_proposition(old_val, new_val, proposition)
                print("after: ",proposition)
                #break

    def remove_implication(self, proposition):
        proposition = proposition.replace("=", "V", 1)
        proposition = proposition.replace(">", "", 1)
        return "!" + proposition
        # print(proposition)

    #def remove_biconditional(self):



    def find_proposition(self, propos, index):
        return find_prop(self, propos, index)


    def replace_proposition(self, old_val, new_val, proposition):
        return proposition.replace(old_val, new_val, 1)


cnf = CNF()
str = "(pVq)=>(!m)^(b)=>(h)"



print("before: " + str)
cnf.convert_to_cnf(str)
