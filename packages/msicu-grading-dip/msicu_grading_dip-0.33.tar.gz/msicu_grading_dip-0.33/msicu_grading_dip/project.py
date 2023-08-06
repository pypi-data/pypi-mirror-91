import os
import pickle
import numpy as np
import math
from sklearn.metrics import f1_score, classification_report

def solution_to_dict(path):
    sol_dict = {}
    with open(path, "r") as fp:
        for line in fp.readlines():
            p_line = line.replace("\n", "")
            img, precision, value = p_line.split(",")
            sol_dict[img] = sol_dict.get(img, {}) 
            sol_dict[img][precision] = sol_dict[img].get(precision, {}) 
            sol_dict[img][precision] = value
    return sol_dict

def dict_to_vect(sol_dict):
    result = []
    for i in range(1, 61):
        for precision in ['15', '30', '45']:
            result.append(sol_dict[str(i)][precision])
    return np.array(result)

def main():
#    path = Path(os.environ['VIRTUAL_ENV'])
#    os.chdir(str(path.parent))
    
    resources_path = os.path.dirname(__file__) + "/resources"
    ground_truth_path = resources_path + "/gt.bin"
    
    student_solution = solution_to_dict("solucion.csv")
    with open(ground_truth_path, "rb") as fp:
        gt = pickle.load(fp)
    y_true = dict_to_vect(gt)
    y_pred = dict_to_vect(student_solution)
    grade = math.floor(f1_score(y_true, y_pred, average="macro") * 100)
    print(classification_report(y_true, y_pred))
    print("Calificacion actual (macroavg): ", grade)
    assert grade >= 70

if __name__ == "__main__":
    main()
