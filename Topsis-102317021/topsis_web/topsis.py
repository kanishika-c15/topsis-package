import pandas as pd
import numpy as np
import sys

def run_topsis(input_file, weights, impacts, output_file):
    try:
        data = pd.read_csv(input_file)
    except FileNotFoundError:
        raise Exception("Input file not found")

    if data.shape[1] < 3:
        raise Exception("Input file must contain at least 3 columns")

    matrix = data.iloc[:, 1:].values

    try:
        matrix = matrix.astype(float)
    except:
        raise Exception("Criteria columns must hookup numeric values only")

    weights = list(map(float, weights.split(",")))
    impacts = impacts.split(",")

    if len(weights) != matrix.shape[1] or len(impacts) != matrix.shape[1]:
        raise Exception("Weights and impacts count mismatch")

    if not all(i in ['+', '-'] for i in impacts):
        raise Exception("Impacts must be + or -")

    # Normalize
    norm = np.sqrt((matrix ** 2).sum(axis=0))
    normalized = matrix / norm

    # Weighted matrix
    weighted = normalized * weights

    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_best.append(weighted[:, i].max())
            ideal_worst.append(weighted[:, i].min())
        else:
            ideal_best.append(weighted[:, i].min())
            ideal_worst.append(weighted[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    score = dist_worst / (dist_best + dist_worst)

    data["Topsis Score"] = score
    data["Rank"] = pd.Series(score).rank(ascending=False, method="dense").astype(int)

    data.to_csv(output_file, index=False)
