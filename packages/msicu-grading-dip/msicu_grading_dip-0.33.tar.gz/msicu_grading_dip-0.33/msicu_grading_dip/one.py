# -*- coding: utf-8 -*-
import sys
import os
import math
import numpy as np

def load_image_from_txt(txt_path):
    if not os.path.exists(txt_path):
        raise Exception("No se pudo abrir %s" % txt_path)
    with open(txt_path, "r") as fp:
        image = fp.readlines()
    rows = int(image[0])
    cols = int(image[1])
    data = np.array([float(point) for point in image[2].strip().split(" ")])
    return rows, cols, data

def calculate_mae(student_result, ground_truth):
    gt_total_points = ground_truth.shape[0]
    sr_total_points = student_result.shape[0]

    if sr_total_points > gt_total_points:
        student_result = student_result[:gt_total_points]
    elif sr_total_points < gt_total_points:
        student_result = np.concatenate([student_result, 
                                         np.zeros(gt_total_points - sr_total_points)])

    mae_score = np.abs(student_result - ground_truth).sum()
    mae_score /= gt_total_points
    return mae_score

def get_score(results_path, ground_truth_path):
    rimg_rows, rimg_cols, rimg_data = load_image_from_txt(results_path)
    gtimg_rows, gtimg_cols, gtimg_data = load_image_from_txt(ground_truth_path)
    
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
    '''calificacion 1 - MSE - PEN '''
    resources_path = os.path.dirname(__file__) + "/resources"
    results_path = sys.argv[1]
    ground_truth_path = resources_path + "/resultado_one.txt"
    return get_score(results_path, ground_truth_path)

#def main_alt():
#    '''calificacion 1 - MSE - PEN '''
#    path = Path(os.environ['VIRTUAL_ENV'])
#    os.chdir(str(path.parent))
#    from procedimientos import cargar_imagen, agrandar_imagen, guardar_imagen
#    
#    imagen = cargar_imagen("./resources/entierro_yalalag_lola_alvares_bravo_1946.txt")
#    
#    # Se agranda la imagen reducida
#    imagen_bilinear = agrandar_imagen(imagen, 3)
#    
#    # Se guarda la imagen interpolada
#    guardar_imagen(imagen_bilinear, "resultado_estudiante.txt")
#    
#    resources_path = os.path.dirname(__file__) + "/resources"
#    ground_truth_path = resources_path + "/resultado_one.txt"
#    
#    score = get_score(resultado.txt, ground_truth_path) 
#    os.remove("resultado_estudiante.txt")
#    return score
