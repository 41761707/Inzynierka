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
:- dynamic inital_state/1.
:- dynamic preconditions/2.
:- dynamic effects/2.
:- dynamic adjacent/2.
:- dynamic n/2.
:- dynamic inconsistent/2.



remove(X,[X | Tail], Tail).
remove(X,[Y | Tail], [Y|Tail1]) :-
    remove(X,Tail,Tail1).

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
    satisfied(StateLevel, Goals),
    extract_plan([StateLevel | GraphPlan], Plan)
    ;
    expand(StateLevel, ActionLevel, NewStateLevel, AllActions),
    %length(StateLevel,A),
    %length(NewStateLevel,B),
    %B>A,
    graphplan([NewStateLevel, ActionLevel, StateLevel | GraphPlan], Goals, AllActions, Plan).

satisfied(_,[]).

satisfied(StateLevel, [G | Goals]) :-
    member(G/IG, StateLevel),
    IG #> 0,
    satisfied(StateLevel, Goals).


extract_plan([_],[]).

extract_plan([ChosenStates,ActionLevel | RestOfGraph], Plan) :-
    collect_vars(ActionLevel, AVars),
    label(AVars),
    
    findall(A, (member(A/1,ActionLevel)),ChosenActions),
    extract_plan(RestOfGraph, RestOfPlan),
    write("ChosenActions: "), write(ChosenActions),nl,
    write("ChosenStates: "), writeln(ChosenStates),
    append(RestOfPlan, [ChosenActions], Plan).


expand(StateLevel, ActionLevel, NextStateLevel, AllActions) :-
    actions(StateLevel, AllActions, [], NewActionLevel, [], NewNextState),
    findall(action(zostan(P),[P],[P]),member(P/_,StateLevel),PersistActs),
    actions(StateLevel, PersistActs, NewActionLevel, ActionLevel, NewNextState, NextStateLevel),
    mutex_action(ActionLevel,NextStateLevel), 
    %mutex_state(ActionLevel),
    mutex_state(NextStateLevel),
    write("ActionLevel: "), write(ActionLevel),nl,
    write("StateLevel: "), write(NextStateLevel), nl.

actions(_,[],ActionLevel, ActionLevel, NextStateLevel, NextStateLevel).

actions(StateLevel, [action(A,Precondition,Effects) | Acts], ActLev0, ActLev, NextLev0, NextLev) :-
    IA in 0..1, 
    includes(StateLevel, Precondition, IA),
    effects(IA, Effects, NextLev0, NextLev1), !, 
    write("A: "), write(A), nl,
    write("Precondition: "), write(Precondition), nl,
    write("Effects: "), write(Effects), nl,
    actions(StateLevel, Acts, [A/IA | ActLev0], ActLev, NextLev1, NextLev)
    ;
    actions(StateLevel, Acts, ActLev0, ActLev, NextLev0, NextLev).

includes(_,[],_).

includes(StateLevel, [P|Ps],IA) :-
    member(P/I, StateLevel),
    IA #=< I,
    includes(StateLevel, Ps, IA).



effects(_,[],StateLevel,StateLevel).

effects(IA, [P | Ps], StateLev0, ExpandedState) :-
    (remove(P/IP,StateLev0,StateLev1),!,
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
    ( mutex(P,P1), !, I*I1 #= 0
    ;
    true
    ),
    mutex_single(P/I,Rest).
    

mutex(P,~P) :- %!.
    write("Mutex: ["), write(P), write(","),write(~P), writeln("]"),!.

mutex(~P,P) :- %!.
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
    
mutex_single_action(A/I, [A1/I1 | Rest],StateLevel) :-
    ( mutex_for_action(A,A1,StateLevel), !, I*I1 #= 0
    ;
    true
    ),
    mutex_single_action(A/I,Rest,StateLevel).

mutex_for_action(A1,A2,StateLevel) :-
    ( preconditions(A1,Precondition),effects(A2,Effects)
      ;
      preconditions(A2,Precondition),effects(A1,Effects)
    ),
    member(P1,Precondition),
    member(P2,Effects),
    mutex(P1,P2),
    write("Mutex: ["), write(A1), write(","),write(A2), writeln("]"),
    mutex_all_states(A1,A2,StateLevel),
    !.

mutex_all_states(A1,A2,StateLevel) :-
    effects(A1,E1),
    effects(A2,E2),
    findall([X,Y],(member(X,E1),member(Y,E2)),C),
    apply_mutex(C,A1,A2,StateLevel).

apply_mutex([],_,_,_).

apply_mutex([H | T], A1/I1,A2/I2,StateLevel) :-
    [First,Second] = H, 
    member(First/F,StateLevel),
    member(Second/S,StateLevel),
    F*S #=< I1*I2,
    write("Mutex: ["), write(First), write(","),write(Second), writeln("]"),
    apply_mutex(T,StateLevel).

collect_vars([],[]).

collect_vars([X/V | Rest], Vars) :-
    (X \= zostan(_), var(V), !, Vars= [V | RestVars]
    ;
    Vars = RestVars),
    collect_vars(Rest,RestVars).






