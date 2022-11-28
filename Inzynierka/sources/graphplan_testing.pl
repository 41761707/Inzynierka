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

%3x3

%time(call_plan([na(a,1),na(b,2),na(c,3),na(d,4),na(e,5),na(f,6),na(g,7),na(h,8),pusty(9)],Plan)),write(Plan).
%assert(state0([na(a,1),na(b,2),na(c,3),na(d,4),na(h,5),na(e,6),pusty(7),na(g,8),na(f,9)])).
can(zostan(P),[P]).
can(idz(R,A,B), [na(R,A), pusty(B)]) :-
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

%state0([pusty(2),pusty(4),pusty(b),pusty(c),na(a,1),na(b,3),na(c,a)]).

*/
/*
%4x4
%assert(state0([na(b,1),na(a,2),na(c,3),pusty(4),na(e,5),na(f,6),na(g,7),na(d,8),na(i,9),na(j,10),na(k,11),na(h,12),na(m,13),na(n,14),na(o,15),na(l,16)])).
%time(call_plan([na(a,1),na(b,2),na(c,3),na(d,4),na(e,5),na(f,6),na(g,7),na(h,8),na(i,9),na(j,10),na(k,11),na(l,12),na(m,13),na(n,14),na(o,15),pusty(16)],Plan)).

can(zostan(P),[P]).
can(idz(R,A,B), [na(R,A), pusty(B)]) :-
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



remove(X,[X | Tail], Tail).
remove(X,[Y | Tail], [Y|Tail1]) :-
    remove(X,Tail,Tail1).

call_plan(Goals,Plan) :-
    state0(S),
    create_plan(S,Goals,Plan).

create_plan(StartState, Goals, Plan) :-
    findall(State/1, member(State,StartState),StartLevel),
    setof(action(Action, Precondition, Effects), (effects(Action,Effects),can(Action,Precondition)),AllActions),
    graphplan([StartLevel], Goals, Plan, AllActions,0).

graphplan([StateLevel | GraphPlan], Goals, Plan, AllActs,Round) :-
    satisfied(StateLevel, Goals),
    extract_plan([StateLevel | GraphPlan], Plan)
    ;
    write("Round: "), writeln(Round),
    NewRound is Round+1,
    expand(StateLevel, ActionLevel, NewStateLev, AllActs),

    graphplan([NewStateLev, ActionLevel, StateLevel | GraphPlan], Goals, Plan, AllActs,NewRound).

satisfied(_,[]).

satisfied(StateLevel, [G | Goals]) :-
    member(G/TG, StateLevel), !,
    TG #> 0,
    satisfied(StateLevel, Goals).


extract_plan([_],[]).

extract_plan([_,ActionLevel | RestOfGraph], Plan) :-
    collect_vars(ActionLevel, AVars),
    labeling([],AVars),
    findall(A,(member(A/1,ActionLevel),A \= zostan(_)), ChosenActions),
    extract_plan(RestOfGraph, RestOfPlan),
    append(RestOfPlan, [ChosenActions], Plan).


expand(StateLev, ActionLev, NextStateLev, AllActs) :-
    findall(action(zostan(P),[P],[P]),member(P/_,StateLev),PersistActs),
    add_actions(StateLev, PersistActs, [], _, [], NextStateLev1),
    add_actions(StateLev, AllActs, [], ActionLev, NextStateLev1, NextStateLev),
    mutex_constr(ActionLev), 
    mutex_constr(NextStateLev).

add_actions(_,[],ActionLev, ActionLev, NextStateLev, NextStateLev).

add_actions(StateLev, [action(A,Precondition,Effects) | Acts], ActLev0, ActLev, NextLev0, NextLev) :-
    TA in 0..1, 
    includes(StateLev, Precondition, TA),
    add_effects(TA, Effects, NextLev0, NextLev1), !, 
    add_actions(StateLev, Acts, [A/TA | ActLev0], ActLev, NextLev1, NextLev)
    ;
    add_actions(StateLev, Acts, ActLev0, ActLev, NextLev0, NextLev).

includes(_,[],_).

includes(StateLev, [P|Ps],TA) :-
    member(P/T, StateLev),
    !,
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

mutex(P,~P) :- !.

mutex(~P,P) :- !. 

mutex(A,B) :-              
    inconsistent(A,B),
    !.

mutex(A1,A2) :-
    ( can(A1,Precondition),effects(A2,Effects)
      ;
      can(A2,Precondition),effects(A1,Effects)
    ),
    member(P1,Precondition),
    member(P2,Effects),
    mutex(P1,P2), 
    !.

collect_vars([],[]).

collect_vars([X/V | Rest], Vars) :-
    (X \= zostan(_), var(V), !, Vars= [V | RestVars]
    ;
    Vars = RestVars),
    collect_vars(Rest,RestVars).






