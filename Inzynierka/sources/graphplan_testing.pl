%GRAPHPLAN wersja 1.3

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

/*

%3x3
%time(call_plan([na(a,1),na(b,2),na(c,3),na(d,4),na(e,5),na(f,6),na(g,7),na(h,8),pusty(9)],Plan)),write(Plan).
%assert(inital_state([na(a,1),na(b,2),na(c,3),na(d,4),na(e,5),na(f,6),na(g,7),na(h,8),pusty(9)])).
%assert(inital_state([na(a,1),na(b,2),na(c,3),na(d,4),na(h,5),na(e,6),pusty(7),na(g,8),na(f,9)])).
%assert(inital_state([na(a,1),na(b,2),na(c,3),pusty(4),na(e,5),na(f,6),na(d,7),na(g,8),na(h,9)])).
%assert(inital_state([na(b,1),na(c,2),na(f,3),na(a,4),na(e,5),pusty(6),na(d,7),na(g,8),na(h,9)])).
%assert(inital_state([na(b,1),pusty(2),na(a,3),na(d,4),na(g,5),na(c,6),na(h,7),na(f,8),na(e,9)])).

preconditions(zostan(P),[P]).
preconditions(idz(R,A,B), [na(R,A), pusty(B)]) :-
    robot(R), 
    adjacent(A,B).


effects(zostan(P),[P]).
effects(idz(R,A,B), [na(R,B),pusty(A)]).

robot(a).
robot(b).
robot(c).
robot(d).
robot(e).
robot(f).
robot(g).
robot(h).

adjacent(A,B) :-
    n(A,B)
    ;
    n(B,A).

n(1,2). n(1,4).
n(2,1). n(2,3). n(2,5).
n(3,2). n(3,6).
n(4,1). n(4,5). n(4,7).
n(5,4). n(5,6). n(5,2). n(5,8).
n(6,5). n(6,3). n(6,9).
n(7,4). n(7,8).
n(8,7). n(8,5). n(8,9).
n(9,8). n(9,6).

incosistent(G,~G).
incosistent(~G,G).
incosistent(na(R,C1),na(R,C2)) :-
    C1 \== C2.

inconsistent(na(_,C),pusty(C)).
inconsistent(pusty(C),na(_,C)).
inconsistent(na(R1,C),na(R2,C)) :-
    R1 \== R2.

*/

%CargoBOT
/*
:- dynamic object/1.
:- dynamic place/1.

can(zostan(P),[P]).
can(idz(Block,From,To), [pusty(Block),pusty(To),na(Block,From)]) :-
    block(Block),
    object(To),
    To \==Block,
    object(From),
    From \==To,
    Block \== From.

effects(zostan(P),[P]).
effects(idz(X,From,To),[na(X,To),pusty(From),~na(X,From),~pusty(To)]).

object(X) :-
    place(X)
    ;
    block(X).

block(a).
block(b).
block(c).

place(1).
place(2).
place(3).
place(4).

incosistent(G,~G).
incosistent(~G,G).

%inital_state([pusty(2),pusty(4),pusty(b),pusty(c),na(a,1),na(b,3),na(c,a)]).

*/

%HANOI


/*
:- dynamic object/1.
:- dynamic place/1.

preconditions(zostan(P),[P]).
preconditions(idz(Block,From,To), [pusty(Block),pusty(To),na(Block,From)]) :-
    block(Block),
    object(To),
    To \==Block,
    object(From),
    From \==To,
    Block \== From,
    n(Block,To).

effects(zostan(P),[P]).
effects(idz(X,From,To),[na(X,To),pusty(From),~na(X,From),~pusty(To)]).

object(X) :-
    place(X)
    ;
    block(X).

block(a).
block(b).
block(c).
block(d).

place(1).
place(2).
place(3).

n(1,2). n(1,a). n(1,b). n(1,c). n(1,d). 
n(2,1). n(2,3). n(2,a). n(2,b). n(2,c). n(2,d). 
n(3,2). n(3,a). n(3,b). n(3,c). n(3,d). 
n(a,1). n(a,2). n(a,3).
n(b,a). n(b,1). n(b,2). n(b,3).
n(c,a). n(c,b). n(c,1). n(c,2). n(c,3).
n(d,a). n(d,b). n(d,c). n(d,1). n(d,2). n(d,3).

incosistent(na(R,C1),na(R,C2)) :-
    C1 \== C2.

inconsistent(na(_,C),pusty(C)).
inconsistent(pusty(C),na(_,C)).
inconsistent(na(R1,C),na(R2,C)) :-
    R1 \== R2.

%assert(inital_state([pusty(2),pusty(4),pusty(b),pusty(c),na(a,1),na(b,3),na(c,a)])).

*/

/*
%4x4
%assert(inital_state([na(b,1),na(a,2),na(c,3),pusty(4),na(e,5),na(f,6),na(g,7),na(d,8),na(i,9),na(j,10),na(k,11),na(h,12),na(m,13),na(n,14),na(o,15),na(l,16)])).
%time(call_plan([na(a,1),na(b,2),na(c,3),na(d,4),na(e,5),na(f,6),na(g,7),na(h,8),na(i,9),na(j,10),na(k,11),na(l,12),na(m,13),na(n,14),na(o,15),pusty(16)],Plan)).

preconditions(zostan(P),[P]).
preconditions(idz(R,A,B), [na(R,A), pusty(B)]) :-
    robot(R), 
    adjacent(A,B).


effects(zostan(P),[P]).
effects(idz(R,A,B), [na(R,B),pusty(A)]).

robot(a).
robot(b).
robot(c).
robot(d).
robot(e).
robot(f).
robot(g).
robot(h).
robot(i).
robot(j).
robot(k).
robot(l).
robot(m).
robot(n).
robot(o).
robot(p).


adjacent(A,B) :-
    n(A,B)
    ;
    n(B,A).

n(1,2). n(1,5).
n(2,1). n(2,6). n(2,3).
n(3,2). n(3,7). n(3,4).
n(4,3). n(4,8).
n(5,1). n(5,6). n(5,9).
n(6,5). n(6,2). n(6,7). n(6,10).
n(7,6). n(7,3). n(7,8). n(7,11).
n(8,7). n(8,4). n(8,12).
n(9,5). n(9,10). n(9,13).
n(10,9). n(10,6). n(10,11). n(10,14).
n(11,10). n(11,7). n(11,12). n(11,15).
n(12,11). n(12,8). n(12,16). 
n(13,9). n(13,14).
n(14,13). n(14,10). n(14,15).
n(15,14). n(15,11). n(15,16).
n(16,15). n(16,12).

incosistent(G,~G).
incosistent(~G,G).
incosistent(na(R,C1),na(R,C2)) :-
    C1 \== C2.

inconsistent(na(_,C),pusty(C)).
inconsistent(pusty(C),na(_,C)).
inconsistent(na(R1,C),na(R2,C)) :-
    R1 \== R2.

*/



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
    %tell('outputs/test.txt'),
    inital_state(S),
    create_plan(S,Goals,Plan).
    %write("Plan: "), writeln(Plan),
    %told.

create_plan(StartState, Goals, Plan) :-
    findall(State/1, member(State,StartState),StartLevel),
    setof(action(Action, Precondition, Effects), (effects(Action,Effects),preconditions(Action,Precondition)),AllActions),
    graphplan([StartLevel], Goals, AllActions,Plan,0).

graphplan([StateLevel | GraphPlan], Goals, AllActions,Plan,Round) :-
    satisfied(StateLevel, Goals),
    extract_plan([StateLevel | GraphPlan], Plan)
    ;
    NewRound is Round+1,
    %write("Round: "), writeln(NewRound),
    expand(StateLevel, ActionLevel, NewStateLevel, AllActions),
    %length(NewStateLevel,NSL),
    %writeln(NSL),
    %outState(NewStateLevel),
    %outAction(ActionLevel),
    graphplan([NewStateLevel, ActionLevel, StateLevel | GraphPlan], Goals, AllActions, Plan,NewRound).

outState([]) :- writeln("").

outState([S/_ | Rest]) :-
    write(S),
    write(", "),
    outState(Rest).

outAction([]) :- writeln("").   

outAction([S/_ | Rest]) :-
    S \= zostan(_),
    write(S),
    write(", "),
    outAction(Rest).

outAction([ _ | Rest]) :-
    outAction(Rest).

satisfied(_,[]).

satisfied(StateLevel, [G | Goals]) :-
    member(G/IG, StateLevel),
    IG #> 0,
    satisfied(StateLevel, Goals).


extract_plan([_],[]).

extract_plan([_,ActionLevel | RestOfGraph], Plan) :-
    %writeln("Extract"),
    collect_vars(ActionLevel, AVars),
    label(AVars),
    findall(A,(member(A/1,ActionLevel),A \= zostan(_)), ChosenActions),
    %writeln(ChosenActions),
    extract_plan(RestOfGraph, RestOfPlan),
    append(RestOfPlan, [ChosenActions], Plan).




expand(StateLevel, ActionLevel, NextStateLevel, AllActions) :-
    add_actions(StateLevel, AllActions, [], NewActionLevel, [], NewNextState),
    findall(action(zostan(P),[P],[P]),member(P/_,StateLevel),PersistActs),
    add_actions(StateLevel, PersistActs, NewActionLevel, ActionLevel, NewNextState, NextStateLevel),
    mutex_action(ActionLevel,NextStateLevel), 
    %mutex_list(ActionLevel),
    mutex_list(NextStateLevel).

add_actions(_,[],ActionLevel, ActionLevel, NextStateLevel, NextStateLevel).

add_actions(StateLevel, [action(A,Precondition,Effects) | Acts], ActLev0, ActLev, NextLev0, NextLev) :-
    IA in 0..1, 
    includes(StateLevel, Precondition, IA),
    add_effects(IA, Effects, NextLev0, NextLev1), !, 
    add_actions(StateLevel, Acts, [A/IA | ActLev0], ActLev, NextLev1, NextLev)
    ;
    add_actions(StateLevel, Acts, ActLev0, ActLev, NextLev0, NextLev).

includes(_,[],_).

includes(StateLevel, [P|Ps],IA) :-
    member(P/I, StateLevel),
    IA #=< I,
    includes(StateLevel, Ps, IA).



add_effects(_,[],StateLevel,StateLevel).

add_effects(IA, [P | Ps], StateLev0, ExpandedState) :-
    (remove(P/IP,StateLev0,StateLev1),!,
    NewIP #= IP+IA,
    StateLevel = [P/NewIP | StateLev1]
    ;
    StateLevel = [P/IA | StateLev0], !
    ),
    add_effects(IA, Ps, StateLevel, ExpandedState).

mutex_list([]).

mutex_list([P | Ps]) :-
    mutex_single(P,Ps),
    mutex_list(Ps).

mutex_single(_,[]).

mutex_single(P/I, [P1/I1 | Rest]) :-
    ( mutex(P,P1), !, I*I1 #= 0
    ;
    true
    ),
    mutex_single(P/I,Rest).
    

mutex(P,~P) :- !.
    %write("Mutex: ["), write(P), write(","),write(~P), writeln("]"),!.

mutex(~P,P) :- !.
    %write("Mutex: ["), write(~P), write(","),write(P), writeln("]"),!.  

mutex(A,B) :-              
    inconsistent(A,B),
    %write("Mutex: ["), write(A), write(","),write(B), writeln("]"), 
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
    %write("Mutex: ["), write(A1), write(","),write(A2), writeln("]"),
    mutex_all_states(A1,A2,StateLevel),
    !.

mutex_all_states(A1,A2,StateLevel) :-
    effects(A1,E1),
    effects(A2,E2),
    findall([X,Y],(member(X,E1),member(Y,E2)),C),
    %writeln(C),
    apply_mutex(C,A1,A2,StateLevel).

apply_mutex([],_).

apply_mutex([H | T], _/I1,_/I2,StateLevel) :-
    [First,Second] = H, 
    member(First/F,StateLevel),
    member(Second/S,StateLevel),
    F*S #=< I1*I2,
    %write("MutexALL: ["), write(First), write(","),write(Second), writeln("]"),
    apply_mutex(T,StateLevel).

collect_vars([],[]).

collect_vars([X/V | Rest], Vars) :-
    (X \= zostan(_), var(V), !, Vars= [V | RestVars]
    ;
    Vars = RestVars),
    collect_vars(Rest,RestVars).












