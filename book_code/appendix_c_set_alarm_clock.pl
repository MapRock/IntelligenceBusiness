% Define the facts for weekdays and weekends
weekday(monday).
weekday(tuesday).
weekday(wednesday).
weekday(thursday).
weekday(friday).
weekend(saturday).
weekend(sunday).

% Define a rule to determine if an appointment is work-related
work_related(Appointment) :-
    appointment(Appointment, _, _, Location, Attendees, Description),
    member("conference room", Location),
    \+ member("personal", Description).

% Define a rule to determine if there is a meeting before 8am
meeting_before_8am(Date, Time) :-
    appointment(Appointment, Date, Time, _, _, _),
    Time < 8.

% Define a rule to check if you got home late
got_home_late(Date) :-
    appointment(_, Date, EndTime, _, _, _),
    EndTime > 18.

% Define the wake-up time based on the given conditions
wake_up_time(Date, Time) :-
    weekday(Date),
    work_related(Appointment),
    \+ got_home_late(Date),
    Time = 7.
wake_up_time(Date, Time) :-
    weekday(Date),
    \+ work_related(Appointment),
    Time = 6.
wake_up_time(Date, Time) :-
    weekday(Date),
    meeting_before_8am(Date, MeetingTime),
    Time is MeetingTime - 1.
wake_up_time(Date, Time) :-
    weekend(Date),
    appointment(_, Date, Time, _, _, _),
    Time < 9,
    Time is Time - 1.
wake_up_time(Date, 9) :-
    weekend(Date),
    \+ appointment(_, Date, _, _, _, _).

% Example appointments in the calendar
appointment(1, monday, 9, ["office", "conference room"], ["Alice", "Bob"], "work meeting").
appointment(2, tuesday, 7, ["office", "conference room"], ["Alice", "Bob"], "work meeting").
appointment(3, wednesday, 17, ["home"], ["Alice"], "personal dinner").
appointment(4, saturday, 8, ["gym"], ["John"], "gym session").

% Define a rule to query the wake-up time
query_wake_up_time(Date) :-
    wake_up_time(Date, Time),
    format("Wake-up time for ~w is ~w:00 AM~n", [Date, Time]).
