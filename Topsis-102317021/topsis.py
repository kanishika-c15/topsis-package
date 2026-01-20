import sys
import pandas as pd
import numpy as np

def topsis(input_file, weights, impacts, output_file):
    # ---------- Read Input File ----------
    try:
        data = pd.read_csv(input_file)
    except FileNotFoundError:
        print("Error: Input file not found")
        sys.exit(1)

    # ---------- Validate Columns ----------
    if data.shape[1] < 3:
        print("Error: Input file must contain three or more columns")
        sys.exit(1)

    # ---------- Extract Decision Matrix ----------
    matrix = data.iloc[:, 1:].values

    # ---------- Check Numeric Values ----------
    try:
        matrix = matrix.astype(float)
    except:
        print("Error: Criteria columns must contain numeric values only")
        sys.exit(1)

    # ---------- Parse Weights & Impacts ----------
    try:
        weights = list(map(float, weights.split(",")))
        impacts = impacts.split(",")
    except:
        print("Error: Weights and impacts must be comma separated")
        sys.exit(1)

    if len(weights) != matrix.shape[1] or len(impacts) != matrix.shape[1]:
        print("Error: Number of weights and impacts must match number of criteria")
        sys.exit(1)

    if not all(i in ['+', '-'] for i in impacts):
        print("Error: Impacts must be either + or -")
        sys.exit(1)

    # ---------- Step 1: Normalize ----------
    norm = np.sqrt((matrix ** 2).sum(axis=0))
    normalized = matrix / norm

    # ---------- Step 2: Apply Weights ----------
    weighted = normalized * weights

    # ---------- Step 3: Ideal Best & Worst ----------
    ideal_best = np.zeros(matrix.shape[1])
    ideal_worst = np.zeros(matrix.shape[1])

    for i in range(matrix.shape[1]):
        if impacts[i] == '+':
            ideal_best[i] = weighted[:, i].max()
            ideal_worst[i] = weighted[:, i].min()
        else:
            ideal_best[i] = weighted[:, i].min()
            ideal_worst[i] = weighted[:, i].max()

    # ---------- Step 4: Distance ----------
    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    # ---------- Step 5: Topsis Score ----------
    score = dist_worst / (dist_best + dist_worst)

    # ---------- Step 6: Rank ----------
    data["Topsis Score"] = score
    data["Rank"] = pd.Series(score).rank(ascending=False, method="dense").astype(int)

    # ---------- Save Output ----------
    data.to_csv(output_file, index=False)
    print("TOPSIS successfully applied. Output saved.")

# ---------- Command Line Interface ----------
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python topsis.py <inputfile> <weights> <impacts> <outputfile>")
        sys.exit(1)

    topsis(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
