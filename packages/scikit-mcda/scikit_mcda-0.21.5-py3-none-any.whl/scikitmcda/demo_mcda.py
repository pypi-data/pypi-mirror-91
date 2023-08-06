from mcda import MCDA
from constants import MAX, MIN, ZScore_, MinMax_, Logistic_, Max_, Sum_, RootSumSquared_ 

def main():

    print("######### MCDA ############")

    print("\n@ Defining labels for Alternatives and Criteria")
    print("-------------------------------------------------")
    
    mcda = MCDA()

    mcda.dataframe([[3000, 12, 64, 5],
                    [1800, 8, 32, 4],
                    [1500, 15, 128, 3]],
                   ["IPHONE", "SAMSUNG", "LG"],
                   ["COST", "CAMERA", "STORAGE", "DESIGN"]
                   )
    print(mcda.pretty_original())

    mcda.set_normalization_method()

    # mcda.set_weights_manually([0.5918, 0.2394, 0.1151, 0.0537])
    # or
    # mcda.set_weights_by_entropy()
    mcda.set_weights_by_ranking_B_POW(2)

    mcda.set_signals([MIN, MAX, MAX, MAX])

    mcda.waspas()

    print(mcda.pretty_normalized())
    print(mcda.pretty_weighted())
    # print(mcda.pretty_Xis())
    print(mcda.pretty_decision())


main()