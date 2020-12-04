"""
Autorzy: s16497 Michał Kosiński, s17402 Aleksandra Formela

Opis projektu: Model ewaluacji pracowników - ocena okresowa
            Wejścia:
                    Efektywność - wyniki
                    Kwalifikacje - poziom kompetencji w danym obszarze
                    Nastawienie - poziom kompetencji miękkich (np. umiejętność pracy w zespole)
                    Chęć rozwoju - poziom motywacji do rozwoju w określonym obszarze
            Wyjście:
                    Ocena okresowa Pracownika w skali 1-5

Korzystając z systemu upewnijmy się, że mamy zainstalowaną biblitekę numpy skfuzzy

"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def enter_a_value(message):
    while True:
        value = input(message)
        try:
            val = int(value)
            if 5 >= val >= 1:
                break
            else:
                print('Wartość musi być w przedziale 1-5, sprobuj ponownie')
        except ValueError:
            print('Wartość musi być numeryczna, spróbuj ponownie')
    return val


efficiency = enter_a_value('Podaj efektywnosc pracownika w skali 1-5: ')
qualifications = enter_a_value('Podaj poziom kwalifikacji pracownika w skali 1-5: ')
desire_to_develop = enter_a_value('Podaj poziom chęci rozwoju pracownika w skali 1-5: ')

# funckje ponizej

efficiency_axis = ctrl.Antecedent(np.arange(0, 6, 1), 'efficiency')
qualifications_axis = ctrl.Antecedent(np.arange(0, 6, 1), 'qualifications')
desire_to_develop_axis = ctrl.Antecedent(np.arange(0, 6, 1), 'desire_to_develop')

grade = ctrl.Consequent(np.arange(0, 5, 1), 'grade')

efficiency_axis.automf(3)
qualifications_axis.automf(3)
desire_to_develop_axis.automf(3)

grade_names = ['slaby', 'przecietny', 'sredni', 'przyzwoity', 'dobry']
grade.automf(names=grade_names)

# rules1

rule1 = ctrl.Rule(antecedent=((efficiency_axis['poor'] & qualifications_axis['poor'] & desire_to_develop_axis['poor']) |
                              (efficiency_axis['poor'] & qualifications_axis['average'] & desire_to_develop_axis['poor']) |
                              (efficiency_axis['average'] & qualifications_axis['poor'] & desire_to_develop_axis['poor'])),
                  consequent=(grade['slaby']))

rule2 = ctrl.Rule(antecedent=((efficiency_axis['average'] & qualifications_axis['poor'] & desire_to_develop_axis['average']) |
                              (efficiency_axis['average'] & qualifications_axis['good'] & desire_to_develop_axis['poor'])),
                  consequent=(grade['przecietny']))

rule3 = ctrl.Rule(antecedent=(efficiency_axis['average'] & qualifications_axis['average'] & desire_to_develop_axis['average']),
                  consequent=(grade['sredni']))

rule4 = ctrl.Rule(antecedent=((efficiency_axis['average'] & qualifications_axis['good'] & desire_to_develop_axis['average']) |
                              (efficiency_axis['good'] & qualifications_axis['average'] & desire_to_develop_axis['average']) |
                              (efficiency_axis['average'] & qualifications_axis['average'] & desire_to_develop_axis['good'])),
                  consequent=(grade['przyzwoity']))

rule5 = ctrl.Rule(antecedent=((efficiency_axis['good'] & qualifications_axis['good'] & desire_to_develop_axis['good']) |
                              (efficiency_axis['good'] & qualifications_axis['average'] & desire_to_develop_axis['good']) |
                              (efficiency_axis['good'] & qualifications_axis['good'] & desire_to_develop_axis['average'])),
                  consequent=(grade['dobry']))

efficiency_axis.view()

# test

grade_control = ctrl.ControlSystem(rules=[rule1, rule2, rule3, rule4, rule5])

employee_grade = ctrl.ControlSystemSimulation(grade_control)

employee_grade.input['efficiency'] = efficiency
employee_grade.input['qualifications'] = qualifications
employee_grade.input['desire_to_develop'] = desire_to_develop

employee_grade.compute()

print('Średnia pracownika to: ' + str(round(employee_grade.output['grade'], 2)))

grade.view(sim=employee_grade)
