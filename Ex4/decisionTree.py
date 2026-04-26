import math
import pandas as pd
import os
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score

def entropy(data):
    if not data: return 0
    total = len(data)
    counts = Counter(data)
    ent = 0
    for c in counts.values():
        prob = c / total
        if prob > 0:
            ent -= prob * math.log2(prob)
    return abs(ent)  # abs() removes the "-0.0000" sign

def gini(data):
    if not data: return 0
    total = len(data)
    counts = Counter(data)
    return 1 - sum((c/total)**2 for c in counts.values())

def manual_mode(criterion_name):
    attr_input = input("Enter attributes (comma separated): ")
    attributes = [a.strip() for a in attr_input.split(",") if a.strip()]
    target = input("Enter target column name: ").strip()
    n = int(input("Enter number of records: "))

    dataset = []
    print(f"\nEnter values as: {', '.join(attributes)}, {target}")
    for i in range(n):
        row_vals = [v.strip() for v in input(f"Row {i+1}: ").split(",")]
        row = {attributes[j]: row_vals[j] for j in range(len(attributes))}
        row[target] = row_vals[-1]
        dataset.append(row)

    print("\n" + "="*60 + f"\n{'MANUAL DATASET':^60}\n" + "="*60)
    headers = attributes + [target]
    print("".join([f"{h:<15}" for h in headers]))
    print("-" * (15 * len(headers)))
    for row in dataset:
        print("".join([f"{str(row[h]):<15}" for h in headers]))

    target_values = [row[target] for row in dataset]
    calc_func = entropy if criterion_name == "entropy" else gini
    parent_val = calc_func(target_values)

    print(f"\n[STEP 1] INITIAL {criterion_name.upper()} (Parent): {parent_val:.4f}")

    gains = {}
    print(f"\n[STEP 2] INTERMEDIATE CALCULATIONS per Attribute:")
    for attr in attributes:
        print(f"\nAttribute: {attr}")
        values = sorted(set(row[attr] for row in dataset))
        weighted_impurity = 0

        for val in values:
            subset = [row[target] for row in dataset if row[attr] == val]
            impurity = calc_func(subset)
            weight = len(subset) / len(dataset)
            weighted_impurity += weight * impurity
            print(f"  -> '{val}': Count={len(subset)}, {criterion_name.capitalize()}={impurity:.4f}, Weight={weight:.2f}")

        info_gain = parent_val - weighted_impurity
        gains[attr] = info_gain
        print(f"  Weighted {criterion_name.capitalize()} Sum: {weighted_impurity:.4f}")
        print(f"  Information Gain: {info_gain:.4f}")

    print("\n" + "="*45 + f"\n{'FINAL SUMMARY':^45}\n" + "="*45)
    print(f"{'Attribute':<25} | {'Gain Value':<15}")
    print("-" * 45)
    for attr, ig in gains.items():
        print(f"{attr:<25} | {ig:.4f}")

    root = max(gains, key=gains.get)
    print("="*45)
    print(f"ROOT NODE SELECTED  {root}")
    print("="*45)

def csv_mode(criterion):
    path = r"\\172.16.16.220\cse-student\ug\23bcs\A\19818\Duvijaa\playtennis.csv"
    if not os.path.exists(path):
        print(f"Error: '{path}' not found!"); return

    df = pd.read_csv(path)
    target_col = df.columns[-1]
    X_encoded = df.drop(columns=[target_col]).copy()
    y = LabelEncoder().fit_transform(df[target_col])

    for col in X_encoded.columns:
        if X_encoded[col].dtype == 'object':
            X_encoded[col] = LabelEncoder().fit_transform(X_encoded[col])

    try:
        split_val = float(input("Enter training % (e.g. 80): ")) / 100
        X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, train_size=split_val, random_state=42)

        model = DecisionTreeClassifier(criterion=criterion).fit(X_train, y_train)
        y_pred = model.predict(X_test)

        print("\n" + "="*60 + f"\n{'DATASET STATISTICS':^60}\n" + "="*60)
        print(f"Total number of records    : {len(df)}")
        print(f"Number of training records : {len(X_train)}")
        print(f"Number of testing records  : {len(X_test)}")

        print("\n" + "="*60 + f"\n{'CSV PERFORMANCE RESULTS':^60}\n" + "="*60)
        print(f"Accuracy  : {accuracy_score(y_test, y_pred)*100:.2f}%")
        print(f"Precision : {precision_score(y_test, y_pred, average='weighted', zero_division=0):.4f}")
        print(f"Recall    : {recall_score(y_test, y_pred, average='weighted', zero_division=0):.4f}")
        print(f"F1-Score  : {f1_score(y_test, y_pred, average='weighted', zero_division=0):.4f}")
        print(f"\nConfusion Matrix:\n{confusion_matrix(y_test, y_pred)}")
        print("="*60)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("--- Decision Tree System ---")
    c = input("1. Manual Mode | 2. CSV Mode: ")
    crit_in = input("Criterion (1: Entropy, 2: Gini): ")
    crit = "entropy" if crit_in == '1' else "gini"

    if c == '1': manual_mode(crit)
    elif c == '2': csv_mode(crit)
    else: print("Invalid Selection.")
