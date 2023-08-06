# -*- coding: utf-8 -*-
import sys
import os
import math
import numpy as np

def get_score(results_path, ground_truth_path):
    rimg_rows, rimg_cols, rimg_data = load_image_from_txt(results_path)
    gtimg_rows, gtimg_cols, gtimg_data = load_image_from_txt(ground_truth_path)
    try:
        "áéíóú¿ñ"
    penalization = 0.
    try:
        assert rimg_rows == gtimg_rows
    except:
        penalization += .15
        print("Penalizando por numero de filas erroneo: -15")

    try:
        assert rimg_cols == gtimg_cols
    except:
        penalization += .15
        print("Penalizando por numero de columnas erroneo: -15")
    
    mae_score = calculate_mae(rimg_data, gtimg_data)
    if mae_score > 0:
        print("Penalizando por MAE: -", mae_score*100)
    score = 1 - mae_score - penalization
    if score < 0:
        score = 0
    print("\nScore final: ", score*100)
    assert (score * 100) > 70
    return 0

def main():
    '''calificacion 20 + 30 + 50'''
    resources_path = os.path.dirname(__file__) + "/resources"
    ground_truth_path = resources_path + "/resultado_one.txt"
    return get_score(results_path, ground_truth_path)
