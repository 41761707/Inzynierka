%GRAPHPLAN wersja 1.2

%TO-DO - sprawdzenie czy plan da sie zakonczyc
%Proby wprowadzen ulepszen czasowych
%use_module(library(clpfd)). <- wymagany import, programowanie ograniczeń

/**
*   Negacja stany wymagana, ze wzgledu na
*   dzialanie prologa wedle zasady "zamknietego swiata".
*   Dodanie negacji ulatwia okreslanie poprawnych stanow kosztem 
*   gorszej czytelnosci generowanych grafow
*/

:-use_module(library(clpfd)).
:-op(100,fx,~).
:- dynamic state0/1.
:- dynamic can/2.
:- dynamic effects/2.
:- dynamic adjacent/2.
:- dynamic n/2.
:- dynamic inconsistent/2.



remove(X,[X | Tail], Tail).
remove(X,[Y | Tail], [Y|Tail1]) :-
    remove(X,Tail,Tail1).

call_plan(Goals,Plan) :-
    tell('outputs/output.txt'),
    state0(S),
    create_plan(S,Goals,Plan),
    write("Plan: "), writeln(Plan),
    told.

create_plan(StartState, Goals, Plan) :-
    findall(State/1, member(State,StartState),StartLevel),
    setof(action(Action, Precondition, Effects), (effects(Action,Effects),can(Action,Precondition)),AllActions),
    write("StartLevel: "), write(StartLevel), nl,
    %write("Goals: "), write(Goals), nl,
    %write("Plan: "), write(Plan), nl,
    %write("AllActions: "), write(AllActions), nl,
    graphplan([StartLevel], Goals, Plan, AllActions).

graphplan([StateLevel | GraphPlan], Goals, Plan, AllActs) :-
    %write("StateLevel "), write(StateLevel), nl,
    satisfied(StateLevel, Goals),
    extract_plan([StateLevel | GraphPlan], Plan)
    %,write("Plan: "), write(Plan), nl
    ;
    length(StateLevel,A),
    length(NewStateLev,B),
    B>A,
    expand(StateLevel, ActionLevel, NewStateLev, AllActs),
    %write("StateLevel: "), write(StateLevel), nl,
    %write("ActionLevel: "), write(ActionLevel), nl,
    %write("NewStateLev: "), write(NewStateLev), nl,
    %write("AllActs: "), write(AllActs), nl,
    graphplan([NewStateLev, ActionLevel, StateLevel | GraphPlan], Goals, Plan, AllActs).

satisfied(_,[]).

satisfied(StateLevel, [G | Goals]) :-
    member(G/TG, StateLevel),
    TG #> 0,
    satisfied(StateLevel, Goals).


extract_plan([_],[]).

extract_plan([ChosenStates,ActionLevel | RestOfGraph], Plan) :-
    collect_vars(ActionLevel, AVars),
    labeling([],AVars),
    findall(A,(member(A/1,ActionLevel),A \= zostan(_)), ChosenActions),
    %findall(A, (member(A/1,ActionLevel)),ChosenActions),
    extract_plan(RestOfGraph, RestOfPlan),
    %Output dla szczegolowego planu
    write("ChosenActions: "), write(ChosenActions),nl,
    write("ChosenStates: "), writeln(ChosenStates),
    append(RestOfPlan, [ChosenActions], Plan).


expand(StateLev, ActionLev, NextStateLev, AllActs) :-
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
    (remove(P/TP,StateLev0,StateLev1),!,
    NewTP #= TP+TA,
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

mutex(P,~P) :- %!.
    write("Mutex: ["), write(P), write(","),write(~P), writeln("]"),!.

mutex(~P,P) :- %!.
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
    mutex(P1,P2), 
    write("Mutex: ["), write(A1), write(","),write(A2), writeln("]"),
    !.

collect_vars([],[]).

collect_vars([X/V | Rest], Vars) :-
    (X \= zostan(_), var(V), !, Vars= [V | RestVars]
    ;
    Vars = RestVars),
    collect_vars(Rest,RestVars).






