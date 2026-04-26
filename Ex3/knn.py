import csv
import math
import os
from collections import Counter
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

# ---------------- DISTANCE FUNCTIONS ----------------
def euclidean(p1, p2):
    return math.sqrt(sum((float(a) - float(b)) ** 2 for a, b in zip(p1, p2)))

def manhattan(p1, p2):
    return sum(abs(float(a) - float(b)) for a, b in zip(p1, p2))

def chebyshev(p1, p2):
    return max(abs(float(a) - float(b)) for a, b in zip(p1, p2))

def get_distance_function(choice):
    return {1: euclidean, 2: manhattan, 3: chebyshev}.get(choice, euclidean)

# ---------------- K VALUE FUNCTION ----------------
def compute_k(n_train):
    k = int(0.1 * n_train)
    if k % 2 == 0: k += 1
    return max(1, k)

# ---------------- KNN CORE FUNCTION WITH INTERMEDIARY STEPS ----------------
def knn_predict(X_train, y_train, x_test, k, dist_func, weighted=False, show_steps=False):
    distances = []

    if show_steps:
        print(f"\n--- [STEP 1] Calculating distances to {len(X_train)} training points ---")

    for i in range(len(X_train)):
        d = dist_func(X_train[i], x_test)
        distances.append((d, y_train[i], X_train[i]))
        if show_steps:
            print(f"Point {i+1} {X_train[i]}: Distance = {d:.4f}")

    # Sort by distance
    distances.sort(key=lambda x: x[0])

    if show_steps:
        print(f"\n--- [STEP 2] Sorting distances and picking k={k} neighbors ---")

    k_nearest = distances[:k]
    for i, (d, label, features) in enumerate(k_nearest):
        if show_steps:
            print(f"Neighbor {i+1}: {features} | Label: {label} | Distance: {d:.4f}")

    if weighted:
        if show_steps:
            print("\n--- [STEP 3] Calculating Weighted Votes (1 / D²) ---")
        weights = {}
        for d, label, _ in k_nearest:
            w = 1 / (d**2 + 1e-5)
            weights[label] = weights.get(label, 0) + w
            if show_steps:
                print(f"Label '{label}' weight contribution: 1/({d:.4f}²) = {w:.4f}")

        final_label = max(weights, key=weights.get)
        if show_steps:
            print(f"Total Weight Scores: {weights}")
        return final_label
    else:
        if show_steps:
            print("\n--- [STEP 3] Calculating Majority Vote ---")
        labels = [label for _, label, _ in k_nearest]
        vote_counts = Counter(labels)
        if show_steps:
            print(f"Vote Counts: {dict(vote_counts)}")
        return vote_counts.most_common(1)[0][0]

# ---------------- CHOICE 1: USER INPUT (WITH STEPS) ----------------
def choice1_knn():
    try:
        n = int(input("Enter number of observations: "))
        m = int(input("Enter number of attributes: "))
        X, y = [], []
        for i in range(n):
            row = list(map(float, input(f"Row {i+1} attributes ({m} values): ").split()))
            label = input("Target label: ")
            X.append(row)
            y.append(label)

        x_test = list(map(float, input("\nEnter test data point attributes: ").split()))
        k = int(input("Enter value of k: "))
        print("Distance Metric: 1-Euclidean  2-Manhattan  3-Chebyshev")
        d_choice = int(input("Choice: "))
        print("Classification Type: 1-Unweighted  2-Weighted")
        weighted = int(input("Choice: ")) == 2

        # We pass show_steps=True here to print all the details
        result = knn_predict(X, y, x_test, k, get_distance_function(d_choice), weighted, show_steps=True)
        print("\nFINAL RESULT")
        print("Predicted Target Label:", result)

    except Exception as e:
        print(f"Error: {e}")

# ---------------- CHOICE 2: CSV INPUT ----------------
def load_csv(filename, attr_indices):
    X, y = [], []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for line_no, row in enumerate(reader, start=2):
            if not row: continue
            try:
                x_row = [float(row[i]) for i in attr_indices]
                X.append(x_row)
                y.append(row[-1])
            except (ValueError, IndexError):
                continue
    return np.array(X), np.array(y)

def choice2_knn():
    path_input = input("\nEnter full CSV path: ").strip()
    filename = path_input.replace('"', '').replace("'", "")
    if not os.path.exists(filename):
        print(f"❌ File not found.")
        return
    try:
        attr_indices = list(map(int, input("Enter attribute indices (space separated): ").split()))
        X, y = load_csv(filename, attr_indices)
        if len(X) == 0: return

        train_pct = int(input("Enter % of training data: "))
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=(100-train_pct), random_state=42)

        k = compute_k(len(X_train))
        print("K computed =",k)
        print(f"Number of training records: {len(X_train)}")
        d_choice = int(input("Distance: 1-Euclidean 2-Manhattan 3-Chebyshev: "))
        weighted = int(input("Type: 1-Unweighted 2-Weighted: ")) == 2

        # In CSV mode, we usually don't print steps for every point (there could be hundreds)
        predictions = [knn_predict(X_train, y_train, x, k, get_distance_function(d_choice), weighted, show_steps=False) for x in X_test]

        print("\n----------Performance Metrics----------")
        print("Accuracy :", accuracy_score(y_test, predictions))
        print("P" \
        "" \
        "recision:", precision_score(y_test, predictions, average='macro', zero_division=0))
        print("Recall   :", recall_score(y_test, predictions, average='macro', zero_division=0))
        print("F1 Score :", f1_score(y_test, predictions, average='macro', zero_division=0))
        print("\nConfusion Matrix:\n", confusion_matrix(y_test, predictions))
    except Exception as e:
        print(f"Error: {e}")

# ---------------- MAIN MENU ----------------
if __name__ == "__main__":
    while True:
        print("\n===== KNN CLASSIFICATION MENU =====")
        print("1. User Input (Shows All Steps)")
        print("2. Load CSV File")
        print("3. Exit")
        try:
            choice = int(input("Enter choice: "))
            if choice == 1: choice1_knn()
            elif choice == 2: choice2_knn()
            elif choice == 3: break
        except ValueError:
            print("Invalid input.")
