import pandas as pd
from ortools.linear_solver import pywraplp
from consts import FOOD_COLUMNS_NAMES, NUTRIENTES_COLUMNS_NAMES

solver      = pywraplp.Solver.CreateSolver('GLOP')

nutrients   = pd.read_csv('nutrientes.csv', header=0, names=NUTRIENTES_COLUMNS_NAMES)
foods       = pd.read_csv('data.csv', header=0, names=FOOD_COLUMNS_NAMES)

foods_xs = []
for _, food in foods.iterrows():
    foods_xs.append(solver.NumVar(0, solver.infinity(), food.ingrediente))

constraints = []
for _, nutrient in nutrients.iterrows():
    constraint = solver.Constraint(nutrient.minimo, solver.infinity())
    
    for index, food in foods.iterrows():
        constraint.SetCoefficient(foods_xs[index], food[nutrient.nome])


objective = solver.Objective()
for food in foods_xs:
    objective.SetCoefficient(food, 1)
    
objective.SetMinimization()

status = solver.Solve()

print(status)
# Check that the problem has an optimal solution.
if status != solver.OPTIMAL:
    print("The problem does not have an optimal solution!")
    if status == solver.FEASIBLE:
        print("A potentially suboptimal solution was found.")
    else:
        print("The solver could not solve the problem.")
        exit(1)

