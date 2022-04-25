from utility import find_prop

IMPLICATION = "=>"
BICONDITION = "<=>"


class CNF:

    def convert_to_cnf(self, proposition):
        for i in range(len(proposition) - 1):
            if proposition[i] == "=" and proposition[i + 1] == ">":
                old_val = self.find_proposition(proposition, i)
                new_val = self.implication(old_val)
                proposition = self.replace_proposition(old_val, new_val, proposition)
                print("After implication: ",proposition)

                #break
            # if proposition[i] == "<" and proposition[i+1] == "=":
            #     if proposition[i+2] == ">":
            #         old_val = self.find_proposition(proposition, i)
            #         new_val = self.biconditional(old_val)
            #         print(new_val)

#test

    def implication(self, proposition):
        proposition = proposition.replace("=", "V", 1)
        proposition = proposition.replace(">", "", 1)
        return "~" + proposition
        # print(proposition)


    def biconditional(self, propos):
        #print(propos)
        p = q = ""
        for i in range(len(propos)-3):
            str = propos[i]
            val = str +propos[i+1]+propos[i+2]

            if val == BICONDITION:
                q += propos.replace(p+"<=>", "")
                break
            else:
                p += str
        print(p," ",q)




    def find_proposition(self, propos, index):
        return find_prop(self, propos, index)


    def replace_proposition(self, old_val, new_val, proposition):
        return proposition.replace(old_val, new_val, 1)


cnf = CNF()
str = "(pVq)=>(!m)^(b)=>(h)"

##str = "((pVc)<=>(qVm))"



print("Before implication: " + str)
cnf.convert_to_cnf(str)
