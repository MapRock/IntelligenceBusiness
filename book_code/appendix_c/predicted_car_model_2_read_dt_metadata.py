"""
This is the 2nd of three Python programs demonstating the extraction of rules in a decision tree.
The first step is to run the program predicted_car_model_1_create.py to create the decision tree model.

This is a simple program using sklearn's DecisionTreeClassifier to train a decision tree model on a sample dataset. 
The model is then saved to a pickle file.


After running this program, the next step is to:
1. Run the program predicted_car_model_3_query.py to query the decision tree model.

"""
import pickle
from sklearn.tree import _tree

pickle_filename = 'c:\\temp\\car_model_predictor.pkl'

# Load the model from the pickle file
with open(pickle_filename, 'rb') as file:
    model = pickle.load(file)

# Function to extract rules from the decision tree and format as Prolog
def extract_rules_as_prolog(model):
    tree = model.tree_
    feature_names = ['occupation', 'age']
    rules = []

    def traverse(node, rule_conditions, depth):
        if tree.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_names[tree.feature[node]]
            threshold = tree.threshold[node]
            left_conditions = rule_conditions + [f"{name} <= {threshold}"]
            right_conditions = rule_conditions + [f"{name} > {threshold}"]
            traverse(tree.children_left[node], left_conditions, depth + 1)
            traverse(tree.children_right[node], right_conditions, depth + 1)
        else:
            value = tree.value[node]
            car_model = model.classes_[value.argmax()]
            support = tree.n_node_samples[node]
            probability = value.max() / value.sum()
            confidence = probability  # In a simple decision tree, probability can be considered confidence
            rule = " AND ".join(rule_conditions)
            prolog_rule = f"predicted_car_model(@custid, {car_model}) :- {rule}.\n" \
                          f"    <ClauseInfo>\n" \
                          f"        <Probability>{probability:.2f}</Probability>\n" \
                          f"        <Confidence>{confidence:.2f}</Confidence>\n" \
                          f"        <Support>{support}</Support>\n" \
                          f"    </ClauseInfo>"
            rules.append(prolog_rule)

    traverse(0, [], 0)
    return rules

# Extract and display the rules as Prolog
prolog_rules = extract_rules_as_prolog(model)
for rule in prolog_rules:
    print(rule)
