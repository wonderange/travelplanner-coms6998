import json
import sys
import re

def preprocess_to_valid_json(text):
    """
    Converts a non-strict JSON (e.g., single quotes, integers as keys) into valid JSON format.
    - Replaces single quotes with double quotes.
    - Converts Python-style None, True, and False into null, true, and false.
    - Ensures all keys are strings.
    """
    # Replace single quotes with double quotes
    text = text.replace("'", '"')

    # Replace Python-style literals with JSON literals
    text = re.sub(r'\bNone\b', 'null', text)
    text = re.sub(r'\bTrue\b', 'true', text)
    text = re.sub(r'\bFalse\b', 'false', text)

    # Convert dictionary-like strings with integer keys to strings
    # Example: {3: ...} becomes {"3": ...}
    def replace_int_keys(match):
        return f'"{match.group(1)}":'

    text = re.sub(r'(\d+):', replace_int_keys, text)

    return text

def aggregate_results(constraint_data):
    # We have difficulties: easy, medium, hard
    difficulties = ["easy", "medium", "hard"]

    # Gather all constraints from all difficulties/scenarios
    constraints_set = set()
    for diff in difficulties:
        if diff in constraint_data:
            for scenario_key, scenario_data in constraint_data[diff].items():
                for c in scenario_data.keys():
                    constraints_set.add(c)

    constraints_list = sorted(list(constraints_set))

    # This helper function computes the percentage if possible
    def compute_percentage(entry):
        t = entry.get("true", 0)
        f = entry.get("false", 0)

        # Try to get total from entry, if not present or zero, infer total
        total = entry.get("total", None)
        if total is None or total == 0:
            # Compute total from true+false if possible
            total = t + f

        if total > 0:
            return (t / total) * 100.0
        else:
            return None

    results = {diff: {} for diff in difficulties}
    for diff in difficulties:
        if diff not in constraint_data:
            continue
        for c in constraints_list:
            scenario_values = []
            for scenario_key, scenario_data in constraint_data[diff].items():
                if c in scenario_data:
                    pct = compute_percentage(scenario_data[c])
                    if pct is not None:
                        scenario_values.append(pct)
            if scenario_values:
                avg_pct = sum(scenario_values) / len(scenario_values)
            else:
                avg_pct = None
            results[diff][c] = avg_pct

    return constraints_list, results

def print_table(title, constraints, results):
    difficulties = ["easy", "medium", "hard"]
    print(title)
    header = ["Constraint"] + [d.capitalize() for d in difficulties]
    row_format = "{:30s}" + "{:>10s}" * 3
    print(row_format.format(*header))
    for c in constraints:
        vals = []
        for d in difficulties:
            val = results[d][c]
            if val is not None:
                vals.append(f"{val:.1f}")
            else:
                vals.append("-")
        print(row_format.format(c, *vals))
    print()

def main(input_file):
    """
    Main function to read input data from a .txt file, process it, and print the results.
    """
    # Read the input data from the text file
    with open(input_file, "r") as f:
        # Read all lines and preprocess to valid JSON
        raw_text = f.read()
        valid_json = preprocess_to_valid_json(raw_text)
        #print(valid_json)
        data = json.loads(valid_json)

    # Process Commonsense Constraint
    if "Commonsense Constraint" in data:
        commonsense_constraints, commonsense_results = aggregate_results(data["Commonsense Constraint"])
        print_table("Commonsense Constraint", commonsense_constraints, commonsense_results)

    # Process Hard Constraint
    if "Hard Constraint" in data:
        hard_constraints, hard_results = aggregate_results(data["Hard Constraint"])
        print_table("Hard Constraint", hard_constraints, hard_results)

if __name__ == "__main__":
    # Check if the input file is provided
    if len(sys.argv) != 2:
        print("Usage: python aggregate_per_constraint_pass_rate.py <input_file>")
        sys.exit(1)

    # Run the main function with the provided input file
    input_file = sys.argv[1]
    main(input_file)