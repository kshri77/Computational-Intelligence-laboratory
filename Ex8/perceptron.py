import numpy as np

def sigmoid(yin):
    return 1 / (1 + np.exp(-yin))

def tanh(yin):
    return np.tanh(yin)

def activation(activation_type, yin, theta, off_state):
    if activation_type == 1: # Threshold
        return 1 if yin >= theta else off_state
    elif activation_type == 2: # Sigmoid
        return 1 if sigmoid(yin) > theta else off_state
    elif activation_type == 3: # Tanh
        return 1 if tanh(yin) > theta else off_state
    return off_state

def train(data, n, w, b, alpha, activation_type, theta, max_epochs=10):
    dataset = np.array(data)
    X = dataset[:, :-1]
    T = dataset[:, -1]
    # Identify if the target uses 0 or -1 as the 'off' state
    off_state = -1 if -1 in np.unique(T) else 0

    for epoch in range(1, max_epochs + 1):
        print(f"\n{'='*35} EPOCH {epoch} {'='*35}")
        print(f"{'Inputs':<12} | {'T':<3} | {'yin':<7} | {'y':<3} | {'W':<12} | {'b':<5} | {'New W':<12} | {'New b'}")
        print("-" * 95)

        error_occurred = False
        for i in range(len(X)):
            x_i, t_i = X[i], T[i]
            yin = np.dot(x_i, w) + b
            y = activation(activation_type, yin, theta, off_state)

            error = t_i - y
            ch_w = np.zeros(n)
            ch_b = 0.0

            if error != 0:
                ch_w = alpha * error * x_i
                w = w + ch_w
                ch_b = alpha * error
                b = b + ch_b
                error_occurred = True

            print(f"{str(x_i):<12} | {t_i:<3} | {yin:<7.2f} | {y:<3} | {str(ch_w):<12} | {ch_b:<5.1f} | {str(w):<12} | {b:<5.1f}")

        if not error_occurred:
            print(f"\n CONVERGED AT EPOCH {epoch}")
            return w, b

    return w, b

# --- Execution ---
try:
    # 1. Load Data
    data = np.loadtxt("data.txt", dtype=int)

    # 2. Get User Inputs
    n = int(input("Enter number of inputs (n): "))

    # Input multiple weights at once (e.g., "0.2 0.5")
    w_input = input(f"Enter initial {n} weights separated by space: ")
    w = np.array([float(val) for val in w_input.split()])

    # Ensure weight vector matches input size
    if len(w) != n:
        raise ValueError(f"Expected {n} weights, but got {len(w)}.")

    b = float(input("Enter initial bias: "))
    alpha = float(input("Enter learning rate (alpha): "))

    print("\nSelect Activation Function:\n1. Threshold\n2. Sigmoid\n3. Tanh")
    act_type = int(input("Selection: "))
    theta = float(input("Enter threshold (theta): "))

    # 3. Start Training
    fw, fb = train(data, n, w, b, alpha, act_type, theta)

    print(f"\n{'*'*20}\nFinal Weights: {fw}\nFinal Bias: {fb}\n{'*'*20}")

except Exception as e:
    print(f"Error: {e}")
