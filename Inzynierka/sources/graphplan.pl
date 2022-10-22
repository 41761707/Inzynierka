%GRAPHPLAN wersja 1.0

%Przed zadaniem pytania należy dodatkowo uruchomić następującą procedurę:
%use_module(library(clpfd)). <- Programowanie ograniczeń
%testowe wywołanie:
%state0(S), plan(S,[at(a,3),at(c,1)],Plan).

%Representation of a planning graph

% PlanningGraph = [StateLevN,ActionLevN,StateLEvN1,...] where N1=N-1
% Level N is the most recently generated level
% StateLevel = [L1/TL1,L2/TL2,...] TL1, TL2,... are Boolean indticator variables of L1,L2,...
% Action Level =[A1/TA1,...] TA1 is a Boolean indicator variable of A1

%use_module(library(clpfd)).

del(X,[X | Tail], Tail).
del(X,[Y | Tail], [Y|Tail1]) :-
    del(X,Tail,Tail1).

:-op(100,fx,~). %Negation of literal

can(persist(P),[P]).
can( go(R,A,B), [at(R,A), clear(B)]) :-
    robot(R), adjacent(A,B).


effects(persist(P),[P]).
effects(go(R,A,B), [at(R,B),clear(A),~at(R,A),~clear(B)]).

robot(a).

adjacent(A,B) :-
    n(A,B)
    ;
    n(B,A).

n(1,2).
n(2,1).

incosistent(G,~G).
incosistent(~G,G).
incosistent(at(R,C1),at(R,C2)) :-
    C1 \== C2.

inconsistent(at(_,C),clear(C)).
inconsistent(clear(C),at(_,C)).
inconsistent(at(R1,C),at(R2,C)) :-
    R1 \== R2.


state0( [at(a,1),clear(2)]).



%plan(StartState, Goals, Plan)

plan(StartState, Goals, Plan) :-
    findall(P/1, member(P,StartState),StartLevel),  %Start level of planning graph
    setof(action(A, PreCond, Effects), (effects(A,Effects),can(A,PreCond)),AllActions),
        %AllActions is a list of all avaiable actions in the planning domain
    graphplan([StartLevel], Goals, Plan, AllActions).

graphplan([StateLevel | PlanGraph], Goals, Plan, AllActs) :-
    satisfied(StateLevel, Goals),   %Goals true in StateLevel
    extract_plan([StateLevel | PlanGraph], Plan)
    ;
    expand(StateLevel, ActionLevel, NewStateLev, AllActs), %Generate new action and state levels
    graphplan([NewStateLev, ActionLevel, StateLevel | PlanGraph], Goals, Plan, AllActs).

%satisfied(StateLevel, Goals): Goals are true in StateLevel
satisfied(_,[]).

satisfied(StateLevel, [G | Goals]) :-
    member(G/TG, StateLevel),
    TG #> 0,    %G must be true
    satisfied(StateLevel, Goals).

%extract_plan(PlanningGraph, Plan): 
%   Extract sequence of 'parallel action levels', omit 'persist' actions from PlanningGraph

extract_plan([_],[]).   %Just single state level, no-action plan

extract_plan([_,ActionLevel | RestOfGraph], Plan) :-
    collect_vars(ActionLevel, AVars),
    labeling([],AVars),
    findall(A,(member(A/1,ActionLevel),A \= persist(_)), Actions),  %Actions to be executed
    extract_plan(RestOfGraph, RestOfPlan),
    append(RestOfPlan, [Actions], Plan).


%expand(StateLevel, ActionLevel, NextStateLevel, AllActs):
    %Given StateLevel find set of possible actions ActionLevel from AllActs and
    %NextStateLevel through ActionLevel. Also set up Boolean constraints
    %among literals and actions. These constraints are necessary for actions
    %performed on StateLevel to result in NextStateLevel

expand(StateLev, ActionLev, NextStateLev, AllActs) :-
    add_actions(StateLev, AllActs, [], ActionLev1, [], NextStateLev1),
    findall(action(persist(P),[P],[P]),member(P/_,StateLev),PersistActs),
        %All persist actions for StateLev
    add_actions(StateLev, PersistActs, ActionLev1, ActionLev, NextStateLev1, NextStateLev),
    mutex_constr(ActionLev),    %Set up mutex constraints between actions
    mutex_constr(NextStateLev). %Set up mutex constraints between literals

%add_actions(StateLev, Acts, ActLev0, ActLev, NextStateLev0, NextStateLev):
    %ActLev = ActLev0 + Acts that are potentially possible in StateLev
    %NextStateLev = NextStateLev0 + effects of Acts that are potentially possible in StateLev
    %Set up constraints between actions in ActLev and both state levels

add_actions(_,[],ActionLev, ActionLev, NextStateLev, NextStateLev).

add_actions(StateLev, [action(A,PreCond,Effects) | Acts], ActLev0, ActLev, NextLev0, NextLev) :-
    TA in 0..1,     %Boolean indicator variable for action A
    includes(StateLev, PreCond, TA),    %A is potentially possible in StateLev
    add_effects(TA, Effects, NextLev0, NextLev1), !,
    add_actions(StateLev, Acts, [A/TA | ActLev0], ActLev, NextLev1, NextLev)
    ;
    add_actions(StateLev, Acts, ActLev0, ActLev, NextLev0, NextLev).

%includes(StateLev, PreCond, TA):
    %All preconditions of action A, whose indicator variable is TA are included in StateLev 

includes(_,[],_).

includes(StateLev, [P|Ps],TA) :-
    member(P/T, StateLev),
    TA #< T,    %If action A occurs the P must be true
    includes(StateLev, Ps, TA).

%add_effects(TA,Effects,StateLev,ExpandedStateLev):
    %Add effects of action A to StateLev giving ExpandedStateLevel, constrain TA and state literals


add_effects(_,[],StateLev,StateLev).

add_effects(TA, [P | Ps], StateLev0, ExpandedState) :-
    (del(P/TP,StateLev0,StateLev1), !,
    NewTP #= TP+TA,
    StateLev = [P/NewTP | StateLev1]    %Add support of action for P 
    ;
    StateLev = [P/TA | StateLev0], !    %Truth of P equivalent to TA
    ),
    add_effects(TA, Ps, StateLev, ExpandedState).

%mutex_constr(List):
    %For all pairs P1, P2 in List: If P1, P2 are mutex then set constraint ~(P1 and P2)
    %all P are either literals or actions
    %Conditions or actions can be mutex because they are incosistent 
    %Actions can also be mutex because of interference 

mutex_constr([]).

mutex_constr([P | Ps]) :-
    mutex_constr1(P,Ps),
    mutex_constr(Ps).

%mutex_constr1(P,Ps):
% set up mutex constraints between P and all P1 in Ps

mutex_constr1(_,[]).

mutex_constr1(P/T, [P1/T1 | Rest]) :-
    ( mutex(P,P1), !, T*T1 #= 0 %T and T1 cannot be both true
    ;
    true
    ),
    mutex_constr1(P/T,Rest).

mutex(P,~P) :- !.   %Negated conditions are always mutually exclusive 

mutex(~P,P) :- !.  

mutex(A,B) :-               %Domain-specific pair of inconsistent literals or actions
    inconsistent(A,B), !.   %Defined by the user in planning domain definition

%Actions A1, A2 mutually exclusive due to interference
%that is action A1 effect is incosistent with A2 precondition or vice versa

mutex(A1,A2) :-
    ( can(A1,Precond),effects(A2,Effects)
      ;
      can(A2,Precond),effects(A1,Effects)
    ),
    member(P1,Precond),
    member(P2,Effects),
    mutex(P1,P2),!.

%collect_vars(Level,List_of_vars): collect into a list all the truth variables in Level

collect_vars([],[]).

collect_vars([X/V | Rest], Vars) :-
    (X \= persist(_), var(V), !, Vars= [V | RestVars] % include V if V is "non-persist" variable
    ;
    Vars = RestVars),
    collect_vars(Rest,RestVars).    %Collect rest of variables 










