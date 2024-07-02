# Define probabilities
P_Cancer = 0.05  # Prior probability of having cancer
P_Positive_given_Cancer = 0.80  # Probability of testing positive given having cancer (True Positive)
P_Positive_given_No_Cancer = 0.15  # Probability of testing positive given not having cancer (False Positive)

# Calculate the total probability of a positive test result (P(B))
P_Positive = (P_Positive_given_Cancer * P_Cancer) + (P_Positive_given_No_Cancer * (1 - P_Cancer))

# Calculate the probability of having cancer given a positive test result (P(A|B))
P_Cancer_given_Positive = (P_Positive_given_Cancer * P_Cancer) / P_Positive

# Verification with sample data
# Let's assume we have 1000 people
total_people = 1000
cancer_people = total_people * P_Cancer
no_cancer_people = total_people - cancer_people

# People who tested positive
true_positive = P_Positive_given_Cancer * cancer_people
false_positive = P_Positive_given_No_Cancer * no_cancer_people
total_positive = true_positive + false_positive

# People who tested negative
true_negative = no_cancer_people - false_positive
false_negative = cancer_people - true_positive

# Calculated probability from sample
calculated_prob_positive = total_positive / total_people
calculated_prob_cancer_given_positive = true_positive / total_positive

# Calculate precision, recall, specificity, and accuracy
precision = true_positive / total_positive
recall = true_positive / cancer_people  # Also known as sensitivity
specificity = true_negative / no_cancer_people
accuracy = (true_positive + true_negative) / total_people
f1_score = 2 * (precision * recall) / (precision + recall)

print(f"P(Cancer) = {P_Cancer}")
print(f"P(Positive | Cancer) = {P_Positive_given_Cancer}")
print(f"P(Positive | No Cancer) = {P_Positive_given_No_Cancer}")
print(f"P(Positive) = {P_Positive:.4f}")
print(f"P(Cancer | Positive) = {P_Cancer_given_Positive:.4f}")

print("\nVerification with sample data:")
print(f"Total people: {total_people}")
print(f"People with cancer: {cancer_people:.1f}")
print(f"People without cancer: {no_cancer_people:.1f}")
print(f"True positive: {true_positive:.1f}")
print(f"False positive: {false_positive:.1f}")
print(f"True negative: {true_negative:.1f}")
print(f"False negative: {false_negative:.1f}")
print(f"Total positive: {total_positive:.1f}")
print(f"Calculated P(Positive) = {calculated_prob_positive:.4f}")
print(f"Calculated P(Cancer | Positive) = {calculated_prob_cancer_given_positive:.4f}")

print("\nStatistics:")
print(f"Precision: {precision:.4f}")
print(f"Recall (Sensitivity): {recall:.4f}")
print(f"Specificity: {specificity:.4f}")
print(f"Accuracy: {accuracy:.4f}")
print(f"F1 Score: {f1_score:.4f}")
