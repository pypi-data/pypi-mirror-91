scikit-mcda
===========

It is a python library made to provide multi-criteria decision aid for developers and operacional researchers.

Scikit-mcda provides an easy way to apply several popular decision-making methods. It can be used as part of your development or for analytical experiments using notebooks like Jupyter, colab or kaggle. The package is available on the Pypi allowing installation by *pip install scikit-mcda* command.

Some methods available:

*DMUU*

- laplace, hurwicz, maximax, maximin, minimax-regret ...

*MCDA*

- Weighted Sum Model (WSM), Weighted Product Model (WPM) , Weighted Aggregated Sum Product Assessment (WASPAS), Technique for Order Preference by Similarity to an Ideal Solution (TOPSIS) ...

*Definition of criteria weights*

- Manually, Entropy, Ranking Methods ... 

*Nomalization*

- Linear MinMax, Linear Max, Linear Sum, Vector, Enhanced Accuracy and Logarithmic.

Scikit-mcda is free to use for personal, commercial and academic projects, always respecting the terms of the Apache 2.0 License. Do not forget to refer to this Library when it is used in your experiments, lectures, presentations, classes and research papers. The reference must follow this citation format.

    (HORTA, 2021)

    HORTA, Antonio (2021). Scikit-mcda: The Python library for multi-criteria decision aid. 
    Version 0.21. [opensource], 17 jan. 2021. Available in: https://gitlab.com/cybercrafter/scikit-mcda. 
    Acessed in: 17 jan. 2021.

It's a project made by Cybercrafter® <ajhorta@cybercrafter.com.br>

Module for Decision-making Under Uncertainty (DMUU)
---------------------------------------------------

**DMUU**: Class Module for Decision-making Under Uncertainty

**Attributes:**
  
    df_original = DataFrame
    df_calc = DataFrame
    decision = {"alternative":,
                "index":,
                "value": ,
                "criteria": ,
                "result": ,
                "type_dm": "DMUU",
                "hurwicz_coeficient":}

**Criteria Methods**:

- maximax()
- maximin()
- laplace()
- minimax_regret()
- hurwicz(coef)

**Properties**

- pretty_original(tablefmt='psql')
- pretty_calc(tablefmt='psql')
- pretty_decision(tablefmt='psql')

tablefmt: "psql" or "latex" or "html" 

**Methods**:

- dataframe(alt_data, alt_labels=[], state_labels=[])
- decision_making(dmuu_criteria_list=[])

Quick Start for DMUU
--------------------
  
    from scikitmcda.dmuu import DMUU

    # Defining labels for Alternatives and States")
    
    dmuu = DMUU()

    dmuu.dataframe([[5000, 2000, 100],
                    [50, 50, 500]],
                    ["ALT_A", "ALT_B"],
                    ["STATE A", "STATE B", "STATE C"]
                    )

    print(dmuu.pretty_original())
    +----+----------------+-----------+-----------+-----------+
    |    | alternatives   |   STATE A |   STATE B |   STATE C |
    |----+----------------+-----------+-----------+-----------|
    |  0 | ALT_A          |      5000 |      2000 |       100 |
    |  1 | ALT_B          |        50 |        50 |       500 |
    +----+----------------+-----------+-----------+-----------+
    
    # Specifying the criteria method
    
    dmuu.minimax_regret()

    print(dmuu.pretty_calc())
    +----+----------------+-----------+-----------+-----------+------------------+
    |    | alternatives   |   STATE A |   STATE B |   STATE C | minimax-regret   |
    |----+----------------+-----------+-----------+-----------+------------------|
    |  0 | ALT_A          |      5000 |      2000 |       100 | (400, 1)         |
    |  1 | ALT_B          |        50 |        50 |       500 | (4950, 0)        |
    +----+----------------+-----------+-----------+-----------+------------------+

    print(dmuu.pretty_decision())
    +---------------+---------+---------+----------------+-------------------------------+-----------+----------------------+
    | alternative   |   index |   value | criteria       | result                        | type_dm   | hurwicz_coeficient   |
    |---------------+---------+---------+----------------+-------------------------------+-----------+----------------------|
    | ALT_A         |       0 |     400 | minimax-regret | {'ALT_A': 400, 'ALT_B': 4950} | DMUU      |                      |
    +---------------+---------+---------+----------------+-------------------------------+-----------+----------------------+

    # Many crietria methods

    dmuu.decision_making([dmuu.maximax(), dmuu.maximin(), dmuu.hurwicz(0.8), dmuu.minimax_regret()])

    print(dmuu.pretty_calc())
    +----+----------------+-----------+-----------+-----------+------------------+-----------+-----------+------------------+
    |    | alternatives   |   STATE A |   STATE B |   STATE C | minimax-regret   | maximax   | maximin   | hurwicz          |
    |----+----------------+-----------+-----------+-----------+------------------+-----------+-----------+------------------|
    |  0 | ALT_A          |      5000 |      2000 |       100 | (400, 1)         | (5000, 1) | (100, 1)  | (4020.0, 1, 0.8) |
    |  1 | ALT_B          |        50 |        50 |       500 | (4950, 0)        | (500, 0)  | (50, 0)   | (410.0, 0, 0.8)  |
    +----+----------------+-----------+-----------+-----------+------------------+-----------+-----------+------------------+

    print(dmuu.pretty_decision())
    +---------------+---------+---------+----------------+-----------------------------------+-----------+----------------------+
    | alternative   |   index |   value | criteria       | result                            | type_dm   | hurwicz_coeficient   |
    |---------------+---------+---------+----------------+-----------------------------------+-----------+----------------------|
    | ALT_A         |       0 |    5000 | maximax        | {'ALT_A': 5000, 'ALT_B': 500}     | DMUU      |                      |
    | ALT_A         |       0 |     100 | maximin        | {'ALT_A': 100, 'ALT_B': 50}       | DMUU      |                      |
    | ALT_A         |       0 |    4020 | hurwicz        | {'ALT_A': 4020.0, 'ALT_B': 410.0} | DMUU      | 0.8                  |
    | ALT_A         |       0 |     400 | minimax-regret | {'ALT_A': 400, 'ALT_B': 4950}     | DMUU      |                      |
    +---------------+---------+---------+----------------+-----------------------------------+-----------+----------------------+

    dmuu.calc_clean()
    print(dmuu.pretty_calc())
    +----+----------------+-----------+-----------+-----------+
    |    | alternatives   |   STATE A |   STATE B |   STATE C |
    |----+----------------+-----------+-----------+-----------|
    |  0 | ALT_A          |      5000 |      2000 |       100 |
    |  1 | ALT_B          |        50 |        50 |       500 |
    +----+----------------+-----------+-----------+-----------+


Module for Multi-Criteria Decision Aid (MCDA)
---------------------------------------------

**MCDA**: Class Module for Multi-Criteria Decision-Aid

Attributes:
  - df_original 
  - weights
  - signals
  - df_normalized
  - df_weighted
  - df_pis
  - df_nis
  - df_distances
  - df_decision

**MCDA basis methods**:

- dataframe(alt_data, alt_labels=[], state_labels=[])
- set_signals([MIN, MIN, MAX])

**MCDA weights determination methods**:

- set_weights_manually([])
- set_weights_by_entropy(normalization_method_for_entropy=LinearSum\_)
- set_weights_by_ranking_A() 
- set_weights_by_ranking_B() 
- set_weights_by_ranking_B_POW(default=0)
- set_weights_by_ranking_C()

*Ranking methods A, B, B_POW and C need criteria ordered by importance C1> c2> C3 ...*

**Decision-Making methods**:

- topsis(normalization_method=Vector\_)
- wsm(normalization_method=None)
- wpm(normalization_method=None)
- waspas(lambda=0.5, normalization_method=None)

Normalization constants: 
  LinearMinMax\_, LinearMax\_, LinearSum\_, Vector\_, EnhancedAccuracy\_ and Logarithmic\_

**Properties**

- pretty_original(tablefmt='psql')
- pretty_normalized(tablefmt='psql')
- pretty_weighted(tablefmt='psql')
- pretty_Xis(tablefmt='psql')
- pretty_decision(tablefmt='psql')

tablefmt: "psql" or "latex" or "html" 

Quick Start for MCDA
--------------------
  
    from scikitmcda.mcda import MCDA
    from scikitmcda.constants import MAX, MIN, ZScore_, MinMax_, Logistic_, Max_, Sum_, RootSumSquared_ 


    mcda = MCDA()

    mcda.dataframe([[90, 20, 86],
                    [120, 8, 120],
                    [70, 12, 90]],
                    ["ALTERNATIVE A", "ALTERNATIVE B", "ALTERNATIVE C"],
                    ["COST", "TIME", "SPEED"]
                    )

    print(mcda.pretty_original())
    +----+----------------+--------+--------+---------+
    |    | alternatives   |   COST |   TIME |   SPEED |
    |----+----------------+--------+--------+---------|
    |  0 | ALTERNATIVE A  |     90 |     20 |      86 |
    |  1 | ALTERNATIVE B  |    120 |      8 |     120 |
    |  2 | ALTERNATIVE C  |     70 |     12 |      90 |
    +----+----------------+--------+--------+---------+

    # defining weights and signals for decision by TOPSIS 
    mcda.set_weights_manually([0.5, 0.3, 0.2])
    # or mcda.set_weights_by_entropy()
    
    mcda.set_signals([MIN, MIN, MAX])
    mcda.topsis()

    print(mcda.pretty_normalized())
    +----+----------------+----------+----------+----------+
    |    | alternatives   |     COST |     TIME |    SPEED |
    |----+----------------+----------+----------+----------|
    |  0 | ALTERNATIVE A  | 0.54371  | 0.811107 | 0.497384 |
    |  1 | ALTERNATIVE B  | 0.724947 | 0.324443 | 0.694024 |
    |  2 | ALTERNATIVE C  | 0.422885 | 0.486664 | 0.520518 |
    +----+----------------+----------+----------+----------+

    print(mcda.pretty_weighted())
    +----+----------------+----------+-----------+-----------+
    |    | alternatives   |     COST |      TIME |     SPEED |
    |----+----------------+----------+-----------+-----------|
    |  0 | ALTERNATIVE A  | 0.271855 | 0.243332  | 0.0994768 |
    |  1 | ALTERNATIVE B  | 0.362473 | 0.0973329 | 0.138805  |
    |  2 | ALTERNATIVE C  | 0.211443 | 0.145999  | 0.104104  |
    +----+----------------+----------+-----------+-----------+

    print(mcda.pretty_Xis())
    +-----+----------+-----------+-----------+
    |     |     COST |      TIME |     SPEED |
    |-----+----------+-----------+-----------|
    | PIS | 0.211443 | 0.0973329 | 0.138805  |
    | NIS | 0.362473 | 0.243332  | 0.0994768 |
    +-----+----------+-----------+-----------+

    print(mcda.pretty_decision())
    +----+----------------+-------------+--------+
    |    | alternatives   |   euclidian |   rank |
    |----+----------------+-------------+--------|
    |  0 | ALTERNATIVE C  |    0.945809 |      1 |
    |  1 | ALTERNATIVE B  |    0.413933 |      2 |
    |  2 | ALTERNATIVE A  |    0.35164  |      3 |
    +----+----------------+-------------+--------+
