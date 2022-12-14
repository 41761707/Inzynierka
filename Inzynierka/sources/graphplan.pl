%GRAPHPLAN wersja 1.2

%TO-DO - sprawdzenie czy plan da sie zakonczyc
%Proby wprowadzen ulepszen czasowych
%use_module(library(clpfd)). <- wymagany import, programowanie ograniczeń

:-use_module(library(clpfd)).
/**
*   Negacja stany wymagana, ze wzgledu na
*   dzialanie prologa wedle zasady "zamknietego swiata".
*   Dodanie negacji ulatwia okreslanie poprawnych stanow kosztem 
*   gorszej czytelnosci generowanych grafow
*/
:-op(100,fx,~).
/**
*   Oznaczenie wykorzystywanych predykatów słowem kluczowym
*   dynamic w celu dynamicznego manipulowania światem
*   przy pomocy predykatów assert/1 czy retract/1
*/
:- dynamic inital_state/1.
:- dynamic preconditions/2.
:- dynamic effects/2.
:- dynamic adjacent/2.
:- dynamic n/2.
:- dynamic inconsistent/2.

/**
*   Predykat usuwająca element z listy
*   @param X Element do usunięcia
*   @param List0 Lista
*   @return Lista1 Lista bez wskazanego elementu
*/

remove(X,[X | Tail], Tail).
remove(X,[Y | Tail], [Y|Tail1]) :-
    remove(X,Tail,Tail1).

/**
*   Predykat odpowiedzialny za rozruch programu oraz
*   przekierowanie strumienia danych do pliku tekstowego
*   @param Goals Cele do osiągnięcia w zdefiniowanym świecie
*   @return Plan Wykreowany plan
*
*
*/

call_plan(Goals,Plan) :-
    tell('outputs/output.txt'),
    inital_state(S),
    create_plan(S,Goals,Plan),
    write("Plan: "), writeln(Plan),
    told.

create_plan(StartState, Goals, Plan) :-
    findall(State/1, member(State,StartState),StartLevel),
    setof(action(Action, Precondition, Effects), (effects(Action,Effects),preconditions(Action,Precondition)),AllActions),
    write("StartLevel: "), write(StartLevel), nl,
    graphplan([StartLevel], Goals, AllActions,Plan).

graphplan([StateLevel | GraphPlan], Goals, AllActions,Plan) :-
    check_constraint(StateLevel, Goals),
    generate_plan([StateLevel | GraphPlan], Plan)
    ;
    expand(StateLevel, ActionLevel, NewStateLevel, AllActions),
    graphplan([NewStateLevel, ActionLevel, StateLevel | GraphPlan], Goals, AllActions, Plan).

check_constraint(_,[]).

check_constraint(StateLevel, [G | Goals]) :-
    member(G/IG, StateLevel),
    IG #> 0,
    check_constraint(StateLevel, Goals).


generate_plan([_],[]).

generate_plan([ChosenStates,ActionLevel | RestOfGraph], Plan) :-
    collect_vars(ActionLevel, AVars),
    label(AVars),
    findall(A, (member(A/1,ActionLevel)),ChosenActions),
    generate_plan(RestOfGraph, RestOfPlan),
    write("ChosenActions: "), write(ChosenActions),nl,
    write("ChosenStates: "), writeln(ChosenStates),
    append(RestOfPlan, [ChosenActions], Plan).


expand(StateLevel, ActionLevel, NextStateLevel, AllActions) :-
    actions(StateLevel, AllActions, [], NewActionLevel, [], NewNextState),
    findall(action(zostan(P),[P],[P]),member(P/_,StateLevel),PersistActs),
    actions(StateLevel, PersistActs, NewActionLevel, ActionLevel, NewNextState, NextStateLevel),
    mutex_action(ActionLevel,NextStateLevel), 
    mutex_state(NextStateLevel),
    write("ActionLevel: "), write(ActionLevel),nl,
    write("StateLevel: "), write(NextStateLevel), nl.

actions(_,[],ActionLevel, ActionLevel, NextStateLevel, NextStateLevel).

actions(StateLevel, [action(A,Precondition,Effects) | Rest], ActLev0, ActLev, NextLev0, NextLev) :-
    IA in 0..1, 
    action_constraint(StateLevel, Precondition, IA),
    effects(IA, Effects, NextLev0, NextLev1), !, 
    write("A: "), write(A), nl,
    write("Precondition: "), write(Precondition), nl,
    write("Effects: "), write(Effects), nl,
    actions(StateLevel, Rest, [A/IA | ActLev0], ActLev, NextLev1, NextLev)
    ;
    actions(StateLevel, Rest, ActLev0, ActLev, NextLev0, NextLev).

action_constraint(_,[],_).

action_constraint(StateLevel, [P|Ps],IA) :-
    member(P/I, StateLevel),
    IA #=< I,
    action_constraint(StateLevel, Ps, IA).



effects(_,[],StateLevel,StateLevel).

effects(IA, [P | Ps], StateLev0, ExpandedState) :-
    (
        remove(P/IP,StateLev0,StateLev1),!,
        NewIP #= IP+IA,
        StateLevel = [P/NewIP | StateLev1]
    ;
        StateLevel = [P/IA | StateLev0], !
    ),
    effects(IA, Ps, StateLevel, ExpandedState).

mutex_state([]).

mutex_state([P | Ps]) :-
    mutex_single(P,Ps),
    mutex_state(Ps).

mutex_single(_,[]).

mutex_single(P/I, [P1/I1 | Rest]) :-
    ( 
        mutex(P,P1), 
        !, 
        I*I1 #= 0
    ;
        true
    ),
    mutex_single(P/I,Rest).
    

mutex(P,~P) :-
    write("Mutex: ["), write(P), write(","),write(~P), writeln("]"),!.

mutex(~P,P) :-
    write("Mutex: ["), write(~P), write(","),write(P), writeln("]"),!.  

mutex(A,B) :-              
    inconsistent(A,B),
    write("Mutex: ["), write(A), write(","),write(B), writeln("]"), 
    !.

mutex_action([],_).

mutex_action([A | As], StateLevel) :-
    mutex_single_action(A,As,StateLevel),
    mutex_action(As,StateLevel).

mutex_single_action(_,[],_).
    
mutex_single_action(A/I, [A1/I1 | Rest],_) :-
    mutex_for_action_1(A,A1), 
    !, 
    I * I1 #= 0,
    mutex_single_action(A/I,Rest,_).

mutex_single_action(A/I, [A1/I1 | Rest],_) :-
    mutex_for_action_2(A,A1), 
    !, 
    I * I1 #= 0,
    mutex_single_action(A/I,Rest,_).

mutex_single_action(A/I, [A1/I1 | Rest],_) :-
    mutex_for_action_3(A,A1), 
    !, 
    I * I1 #= 0,
    mutex_single_action(A/I,Rest,_).

mutex_single_action(A/I, [_ | Rest],_) :-
    true,
    mutex_single_action(A/I,Rest,_).

mutex_for_action_1(A1,A2) :-
    ( 
        preconditions(A1,Precondition),effects(A2,Effects)
    ;
        preconditions(A2,Precondition),effects(A1,Effects)
    ),
    member(P1,Precondition),
    member(P2,Effects),
    mutex(P1,P2),
    %write("Mutex1: ["), write(A1), write(","),write(A2), writeln("]"),
    !.

mutex_for_action_2(A1,A2) :-
    preconditions(A1,Precondition1),
    preconditions(A2,Precondition2),
    member(P1,Precondition1),
    member(P2,Precondition2),
    mutex(P1,P2),
    %write("Mutex2: ["), write(A1), write(","),write(A2), writeln("]"),
    !.

mutex_for_action_3(A1,A2) :-
    effects(A1,Effects1),
    effects(A2,Effects2),
    member(P1,Effects1),
    member(P2,Effects2),
    mutex(P1,P2),
    %write("Mutex3: ["), write(A1), write(","),write(A2), writeln("]"),
    !.

collect_vars([],[]).

collect_vars([X/V | Rest], Vars) :-
    (
        X \= zostan(_), 
        var(V), 
        !, 
        Vars= [V | RestVars]
        ;
        Vars = RestVars
    ),
    collect_vars(Rest,RestVars).
