:- use_module(library(clpfd)).

riddle([T,W,O],[T,W,O],[F,O,U,R]) :-
    Values = [T,W,O,F,U,R],
    Values ins 0..9,
    all_different(Values),
    T #> 0,
    F #> 0,
    100*T + 10*W + O + 100*T + 10*W + O #= 1000*F + 100*O + 10*U + R,
    label(Values).

