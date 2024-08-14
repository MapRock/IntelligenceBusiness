% New rule to take action based on the classification
send_if_virginica(Sepallengthcm, Sepalwidthcm, Petallengthcm, Petalwidthcm) :-
    p(Sepallengthcm, Sepalwidthcm, Petallengthcm, Petalwidthcm, virginica, Probability),
    Probability > 0.5,
    format('This iris is ~w with probability ~2f. Sending email to your friend...', [virginica, Probability]),
    % Here you would normally call an external function to send an email.
    % For the sake of example, we just print a message.
    true.