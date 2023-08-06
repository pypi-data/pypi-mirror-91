scikit-mcda
===========

A python library made to provide multi-criteria decision aid for developers and operacional researchers.

by Cybercrafter® <ajhorta@cybercrafter.com.br>


Module for Decision-making Under Uncertainty (DMUU)
---------------------------------------------------

**DMUU**: Class Module for Decision-making Under Uncertainty

- Attributes:

  ::

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

**Methods**:

- dataframe(alt_data, alt_labels=[], state_labels=[])
- decision_making(dmuu_criteria_list=[])

Quick Start
-----------

.. code-block:: python

  from dmuu import DMUU
  
  def main():

      # Defining labels for Alternatives and States")
      
      dmuu = DMUU()

      dmuu.dataframe([[5000, 2000, 100],
                      [50, 50, 500]],
                      ["ALT_A", "ALT_B"],
                      ["STATE A", "STATE B", "STATE C"]
                      )
  
      print(dmuu.df_original)

      +----+----------------+-----------+-----------+-----------+
      |    | alternatives   |   STATE A |   STATE B |   STATE C |
      |----+----------------+-----------+-----------+-----------|
      |  0 | ALT_A          |      5000 |      2000 |       100 |
      |  1 | ALT_B          |        50 |        50 |       500 |
      +----+----------------+-----------+-----------+-----------+

      
      # Specifying the criteria method
      
      dmuu.minimax_regret()

      print(dmuu.df_calc)
      print(dmuu.df_decision)
      
      Calc:
      +----+----------------+-----------+-----------+-----------+------------------+
      |    | alternatives   |   STATE A |   STATE B |   STATE C | minimax-regret   |
      |----+----------------+-----------+-----------+-----------+------------------|
      |  0 | ALT_A          |      5000 |      2000 |       100 | (400, 1)         |
      |  1 | ALT_B          |        50 |        50 |       500 | (4950, 0)        |
      +----+----------------+-----------+-----------+-----------+------------------+

      Result:
      +---------------+---------+---------+----------------+-------------------------------+-----------+----------------------+
      | alternative   |   index |   value | criteria       | result                        | type_dm   | hurwicz_coeficient   |
      |---------------+---------+---------+----------------+-------------------------------+-----------+----------------------|
      | ALT_A         |       0 |     400 | minimax-regret | {'ALT_A': 400, 'ALT_B': 4950} | DMUU      |                      |
      +---------------+---------+---------+----------------+-------------------------------+-----------+----------------------+

      # Many crietria methods

      dmuu.decision_making([dmuu.maximax(), dmuu.maximin(), dmuu.hurwicz(0.8), dmuu.minimax_regret()])

      print(dmuu.df_calc)
      print(dmuu.decision)

      Calc:
      +----+----------------+-----------+-----------+-----------+------------------+-----------+-----------+------------------+
      |    | alternatives   |   STATE A |   STATE B |   STATE C | minimax-regret   | maximax   | maximin   | hurwicz          |
      |----+----------------+-----------+-----------+-----------+------------------+-----------+-----------+------------------|
      |  0 | ALT_A          |      5000 |      2000 |       100 | (400, 1)         | (5000, 1) | (100, 1)  | (4020.0, 1, 0.8) |
      |  1 | ALT_B          |        50 |        50 |       500 | (4950, 0)        | (500, 0)  | (50, 0)   | (410.0, 0, 0.8)  |
      +----+----------------+-----------+-----------+-----------+------------------+-----------+-----------+------------------+

      Result:
      +---------------+---------+---------+----------------+-----------------------------------+-----------+----------------------+
      | alternative   |   index |   value | criteria       | result                            | type_dm   | hurwicz_coeficient   |
      |---------------+---------+---------+----------------+-----------------------------------+-----------+----------------------|
      | ALT_A         |       0 |    5000 | maximax        | {'ALT_A': 5000, 'ALT_B': 500}     | DMUU      |                      |
      | ALT_A         |       0 |     100 | maximin        | {'ALT_A': 100, 'ALT_B': 50}       | DMUU      |                      |
      | ALT_A         |       0 |    4020 | hurwicz        | {'ALT_A': 4020.0, 'ALT_B': 410.0} | DMUU      | 0.8                  |
      | ALT_A         |       0 |     400 | minimax-regret | {'ALT_A': 400, 'ALT_B': 4950}     | DMUU      |                      |
      +---------------+---------+---------+----------------+-----------------------------------+-----------+----------------------+

      dmuu.calc_clean()
      print(dmuu.df_calc)
      
      df_calc clean:
      +----+----------------+-----------+-----------+-----------+
      |    | alternatives   |   STATE A |   STATE B |   STATE C |
      |----+----------------+-----------+-----------+-----------|
      |  0 | ALT_A          |      5000 |      2000 |       100 |
      |  1 | ALT_B          |        50 |        50 |       500 |
      +----+----------------+-----------+-----------+-----------+