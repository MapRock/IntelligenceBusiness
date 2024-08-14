:- consult('c:/MapRock/IntelligenceBusiness/book_code/appendix_c/iris_prolog_rules.pl').

% New rule to take action based on the classification
send_if_iris_found(Sepallengthcm, Sepalwidthcm, Petallengthcm, Petalwidthcm) :-
    p(Sepallengthcm, Sepalwidthcm, Petallengthcm, Petalwidthcm, Guess, Probability),
    Probability > 0.5,
    format('This iris is ~w with probability ~2f. Sending email to your friend...\n', [Guess, Probability]),
    % Here you would normally call an external function to send an email.
    % For the sake of example, we just print a message.
    true.