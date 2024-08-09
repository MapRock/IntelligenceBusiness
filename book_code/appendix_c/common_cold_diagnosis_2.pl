% Define a rule to diagnose common cold based on factors
diagnose(Patient, 'common_cold') :-
    has_symptom(Patient, 'cough'),
    age(Patient, Age), Age < 50,
    smoking_status(Patient, 'non_smoker'),
    duration(Patient, Duration), Duration < 10.
