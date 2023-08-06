from dmuu import DMUU
import pprint
from tabulate import tabulate


def main():

    print("######### DMMU ############")

    print("\n@ Defining labels for Alternatives and States")
    print("-----------------------------------------------")
    
    dmuu = DMUU()


    dmuu.dataframe([[5000, 2000, 100],
                    [50, 50, 500]],
                   ["ALT_A", "ALT_B"],
                   ["STATE A", "STATE B", "STATE C"]
                   )
    print(tabulate(dmuu.df_original, headers='keys', tablefmt='psql'))

    print("\n@ Specifying the criteria method")
    print("----------------------------------")
    dmuu.minimax_regret()
    print("\nCalc:\n")
    print(tabulate(dmuu.df_calc, headers='keys', tablefmt='psql'))
    print("\nResult:\n")
    print(tabulate(dmuu.decision, headers='keys', tablefmt='psql'))


    print("\n@ Many crietria methods")
    print("------------------------------")
    dmuu.decision_making([dmuu.maximax(), dmuu.maximin(), dmuu.hurwicz(0.8), dmuu.minimax_regret()])
    print("\nCalc:\n")
    print(tabulate(dmuu.df_calc, headers='keys', tablefmt='psql'))
    print("\nResult:\n")
    print(tabulate(dmuu.decision, headers='keys', tablefmt='psql'))

    dmuu.calc_clean()
    print("\nClean Calc:\n")
    print(tabulate(dmuu.df_calc, headers='keys', tablefmt='psql'))

    print("Attributes:\n")
    print(vars(dmuu))

main()