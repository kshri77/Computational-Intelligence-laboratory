
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numerical value.")

# --- 1. DECK OF CARDS ---
def test_deck():
    print("\n--- DECK OF CARDS CONFIGURATION ---")
    kings = get_float("Enter number of Kings in deck (Standard is 4): ")
    total = 52
    hearts = 13
    k_and_h = 1 if kings > 0 else 0

    p_k = kings / total
    p_h = hearts / total
    p_inter = k_and_h / total
    p_union = p_k + p_h - p_inter

    print("\n" + "="*40)
    print(f"{'DECK TEST RESULTS':^40}")
    print("="*40)
    print(f"P(King)           : {p_k:.4f}")
    print(f"P(Heart)          : {p_h:.4f}")
    print(f"P(King ∩ Heart)   : {p_inter:.4f}")
    print(f"P(King ∪ Heart)   : {p_union:.4f}")
    print("="*40)

# --- 2. BAYES THEOREM ---
def test_bayes():
    print("\n--- MEDICAL TEST ---")
    p_disease = get_float("Enter Disease Prevalence (e.g., 0.01 for 1%): ")
    sens = get_float("Enter Test Sensitivity (e.g., 0.99): ")
    f_pos = get_float("Enter False Positive Rate (e.g., 0.05): ")

    p_healthy = 1 - p_disease
    p_pos = (sens * p_disease) + (f_pos * p_healthy)
    p_d_given_pos = (sens * p_disease) / p_pos if p_pos > 0 else 0

    print("\n┌" + "─"*38 + "┐")
    print(f"│ {'BAYES THEOREM REPORT':^36} │")
    print("├" + "─"*38 + "┤")
    print(f"│ Prevalence      : {p_disease:<18.2%} │")
    print(f"│ P(Positive)     : {p_pos:<18.4f} │")
    print(f"│ P(Disease|Pos)  : {p_d_given_pos:<18.2%} │")
    print("└" + "─"*38 + "┘")

# --- 4. JOINT PROBABILITY ---
def test_joint():
    print("\n--- JOINT TABLE ---")
    r_ot = get_float("Enter P(Rainy ∩ On-Time): ")
    r_lt = get_float("Enter P(Rainy ∩ Late): ")
    s_ot = 0.63
    s_lt = 0.07

    total = r_ot + r_lt + s_ot + s_lt
    p_late = s_lt + r_lt
    cond = r_lt / p_late if p_late > 0 else 0

    print("\n" + " " + "_"*41)
    print(f"| {'Weather':<10} | {'On-Time':<12} | {'Late':<12} |")
    print(f"| {'Sunny':<10} | {s_ot:<12} | {s_lt:<12} |")
    print(f"| {'Rainy':<10} | {r_ot:<12} | {r_lt:<12} |")
    print("|" + "_"*10 + "|" + "_"*12 + "|" + "_"*12 + "|")
    print(f"\nVALIDATION: Sum = {total:.2f} | P(Rainy|Late) = {cond:.4f}")

# --- MAIN MENU ---
def main():
    while True:
        print("\nPROBABILITY TEST SUITE")
        print("1. Deck of Cards")
        print("2. Bayes Theorem (Medical)")
        print("3. Joint Prob Table (Commute)")
        print("4. Exit")

        choice = input("\nSelect a test case (1-5): ")

        if choice == '1': test_deck()
        elif choice == '2': test_bayes()
        elif choice == '3': test_joint()
        elif choice == '4': break
        else: print("Invalid choice.")

        input("\nPress Enter to return to menu...")
        clear_screen()

if __name__ == "__main__":
    main()
