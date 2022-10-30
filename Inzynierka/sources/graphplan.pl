%GRAPHPLAN wersja 1.1

%TO-DO - sprawdzenie czy plan da sie zakonczyc
%Proby wprowadzen ulepszen czasowych
%Przed zadaniem pytania należy dodatkowo uruchomić następującą procedurę:
%use_module(library(clpfd)). <- Programowanie ograniczeń
%testowe wywołanie:
%state0(S), plan(S,[na(a,3),na(c,1)],Plan).
%state0(S), plan(S,[pusty(1), na(a,2)],Plan).

/**
*   Negacja stany wymagana, ze wzgledu na
*   dzialanie prologa wedle zasady "zamknietego swiata".
*   Dodanie negacji ulatwia okreslanie poprawnych stanow kosztem 
*   gorszej czytelnosci generowanych grafow
*/
:-op(100,fx,~).

can(zostan(P),[P]).
can(idz(R,A,B), [na(R,A), pusty(B)]) :-
    robot(R), 
    adjacent(A,B).


effects(zostan(P),[P]).
effects(idz(R,A,B), [na(R,B),pusty(A),~na(R,A),~pusty(B)]).

%robot(a). robot(b). robot(c).
robot(a).

adjacent(A,B) :-
    n(A,B)
    ;
    n(B,A).

%n(1,2). n(2,3). n(4,5). n(5,6). n(1,4). n(2,5). n(3,6).
n(1,2). n(2,1). 
%n(2,3). n(3,2).

incosistent(G,~G).
incosistent(~G,G).
incosistent(na(R,C1),na(R,C2)) :-
    C1 \== C2.

inconsistent(na(_,C),pusty(C)).
inconsistent(pusty(C),na(_,C)).
inconsistent(na(R1,C),na(R2,C)) :-
    R1 \== R2.


%state0([na(a,1), na(b,2), na(c,3), pusty(4), pusty(5), pusty(6)]).
%state0([na(a,1),pusty(2),pusty(3)]).
state0([na(a,1),pusty(2)]).

remove(X,[X | Tail], Tail).
remove(X,[Y | Tail], [Y|Tail1]) :-
    remove(X,Tail,Tail1).

call_plan(Goals,Plan) :-
    state0(S),
    plan(S,Goals,Plan).

plan(StartState, Goals, Plan) :-
    findall(P/1, member(P,StartState),StartLevel),
    setof(action(A, Precondition, Effects), (effects(A,Effects),can(A,Precondition)),AllActions),
    write("StartLevel: "), write(StartLevel), nl,
    %write("Goals: "), write(Goals), nl,
    %write("Plan: "), write(Plan), nl,
    %write("AllActions: "), write(AllActions), nl,
    graphplan([StartLevel], Goals, Plan, AllActions).

graphplan([StateLevel | PlanGraph], Goals, Plan, AllActs) :-
    %write("StateLevel "), write(StateLevel), nl,
    satisfied(StateLevel, Goals),
    extract_plan([StateLevel | PlanGraph], Plan)
    %,write("Plan: "), write(Plan), nl
    ;
    expand(StateLevel, ActionLevel, NewStateLev, AllActs),
    %write("StateLevel: "), write(StateLevel), nl,
    %write("ActionLevel: "), write(ActionLevel), nl,
    %write("NewStateLev: "), write(NewStateLev), nl,
    %write("AllActs: "), write(AllActs), nl,
    length(StateLevel,X),
    X>0,
    graphplan([NewStateLev, ActionLevel, StateLevel | PlanGraph], Goals, Plan, AllActs).

satisfied(_,[]).

satisfied(StateLevel, [G | Goals]) :-
    member(G/TG, StateLevel),
    TG #> 0,
    satisfied(StateLevel, Goals).


extract_plan([_],[]).

extract_plan([_,ActionLevel | RestOfGraph], Plan) :-
    collect_vars(ActionLevel, AVars),
    labeling([],AVars),
    %findall(A,(member(A/1,ActionLevel),A \= zostan(_)), Actions),
    findall(A, (member(A/1,ActionLevel)),Actions),
    extract_plan(RestOfGraph, RestOfPlan),
    append(RestOfPlan, [Actions], Plan).


expand(StateLev, ActionLev, NextStateLev, AllActs) :-
    %writeln("Inside expand"),
    add_actions(StateLev, AllActs, [], ActionLev1, [], NextStateLev1),
    findall(action(zostan(P),[P],[P]),member(P/_,StateLev),PersistActs),
    add_actions(StateLev, PersistActs, ActionLev1, ActionLev, NextStateLev1, NextStateLev),
    mutex_constr(ActionLev), 
    mutex_constr(NextStateLev),
    %write("AllActs: "), write(AllActs), nl,
    write("ActionLevel: "), write(ActionLev),nl,
    write("StateLevel: "), write(NextStateLev), nl.

add_actions(_,[],ActionLev, ActionLev, NextStateLev, NextStateLev).

add_actions(StateLev, [action(A,Precondition,Effects) | Acts], ActLev0, ActLev, NextLev0, NextLev) :-
    %write("Inside add_actions"), nl,
    TA in 0..1, 
    includes(StateLev, Precondition, TA),
    add_effects(TA, Effects, NextLev0, NextLev1), !, 
    write("A: "), write(A), nl,
    write("Precondition: "), write(Precondition), nl,
    write("Effects: "), write(Effects), nl,
    add_actions(StateLev, Acts, [A/TA | ActLev0], ActLev, NextLev1, NextLev)
    ;
    add_actions(StateLev, Acts, ActLev0, ActLev, NextLev0, NextLev).

includes(_,[],_).

includes(StateLev, [P|Ps],TA) :-
    member(P/T, StateLev),
    TA #=< T,
    includes(StateLev, Ps, TA).



add_effects(_,[],StateLev,StateLev).

add_effects(TA, [P | Ps], StateLev0, ExpandedState) :-
    %write("Inside add_effects"), nl,
    (remove(P/TP,StateLev0,StateLev1),!,
    NewTP #= TP+TA,
    %write("NewTP: "), write(NewTP), nl,
    StateLev = [P/NewTP | StateLev1]
    ;
    StateLev = [P/TA | StateLev0], !
    ),
    add_effects(TA, Ps, StateLev, ExpandedState).

mutex_constr([]).

mutex_constr([P | Ps]) :-
    mutex_constr1(P,Ps),
    mutex_constr(Ps).

mutex_constr1(_,[]).

mutex_constr1(P/T, [P1/T1 | Rest]) :-
    ( mutex(P,P1), !, T*T1 #= 0
    ;
    true
    ),
    mutex_constr1(P/T,Rest).

mutex(P,~P) :- 
    write("Mutex: ["), write(P), write(","),write(~P), writeln("]"),!.

mutex(~P,P) :- 
    write("Mutex: ["), write(~P), write(","),write(P), writeln("]"),!.  

mutex(A,B) :-              
    inconsistent(A,B),
    write("Mutex: ["), write(A), write(","),write(B), writeln("]"), 
    !.

mutex(A1,A2) :-
    ( can(A1,Precondition),effects(A2,Effects)
      ;
      can(A2,Precondition),effects(A1,Effects)
    ),
    member(P1,Precondition),
    member(P2,Effects),
    mutex(P1,P2),!.

collect_vars([],[]).

collect_vars([X/V | Rest], Vars) :-
    (X \= zostan(_), var(V), !, Vars= [V | RestVars]
    ;
    Vars = RestVars),
    collect_vars(Rest,RestVars).






