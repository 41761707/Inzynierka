# Trik na doxygena
# żeby wszystko było w jednym spójnym okienku

## @package graphplan
#  Plik zawierający implementację klasy
#  SimplifiedGraph kreującej uproszczony graf dla zadanego problemu
##
#   Predykat usuwająca element z listy
#   @param X Element do usunięcia
#   @param List0 Lista
#   @return List1 Lista bez wskazanego elementu

def remove(X,List0, List1):
    pass

##
#   Predykat odpowiedzialny za rozruch programu oraz
#   przekierowanie strumienia danych do pliku tekstowego
#   @param Goals Cele do osiągnięcia w zdefiniowanym świecie
#   @return Plan Wykreowany plan
def call_plan(Goals,Plan):
    pass

##
#   Predykat odpowiedzialny za kreowanie planu
#   @param StartState Warunki początkowe
#   @param Goals Zdefiniowane cele
#   @return Plan Wykreowany plan
def create_plan(StartState, Goals, Plan):
    pass

def graphplan(GraphPlan, Goals, AllActions,Plan) :
    pass

##
#   Predykat odpowiedzialny za kreowanie planu
#   @param StartState Warunki początkowe
#   @param Goals Zdefiniowane cele
#   @return Plan Wykreowany plan
def check_constraint(StateLevel, Goals):
    pass

##
#   Predykat odpowiedzialny za kreowanie planu
#   @param StartState Warunki początkowe
#   @param Goals Zdefiniowane cele
#   @return Plan Wykreowany plan
def generate_plan(GraphPlan, Plan):
    pass

##
#   Predykat odpowiedzialny za kreowanie planu
#   @param StartState Warunki początkowe
#   @param Goals Zdefiniowane cele
#   @return Plan Wykreowany plan
def expand(StateLevel, ActionLevel, NextStateLevel, AllActions) :
    pass

##
#   Predykat odpowiedzialny za kreowanie planu
#   @param StartState Warunki początkowe
#   @param Goals Zdefiniowane cele
#   @return Plan Wykreowany plan
def actions(StateLevel,Action,PreviousActionLevel,NewActionLevel,PreviousStateLevel,NewStateLevel):
    pass

##
#   Predykat odpowiedzialny za kreowanie planu
#   @param StartState Warunki początkowe
#   @param Goals Zdefiniowane cele
#   @return Plan Wykreowany plan
def actions_constraint(StateLevel, Preconditions, Indykator):
    pass

##
#   Predykat odpowiedzialny za kreowanie planu
#   @param StartState Warunki początkowe
#   @param Goals Zdefiniowane cele
#   @return Plan Wykreowany plan
def effects(Indykator,PreviousStateLevel,NextStateLevel):
    pass

##
#   Predykat odpowiedzialny za kreowanie planu
#   @param StartState Warunki początkowe
#   @param Goals Zdefiniowane cele
#   @return Plan Wykreowany plan
def mutex_state(StateLevel) :
    pass

##
#   Predykat odpowiedzialny za kreowanie planu
#   @param StartState Warunki początkowe
#   @param Goals Zdefiniowane cele
#   @return Plan Wykreowany plan
def mutex_single(State,StateLevel):
    pass
    
##
#   Predykat odpowiedzialny za kreowanie planu
#   @param StartState Warunki początkowe
#   @param Goals Zdefiniowane cele
#   @return Plan Wykreowany plan
def mutex(A,B):
    pass  

##
#   Predykat odpowiedzialny za kreowanie planu
#   @param StartState Warunki początkowe
#   @param Goals Zdefiniowane cele
#   @return Plan Wykreowany plan
def mutex_action(Action, StateLevel):
    pass

##
#   Predykat odpowiedzialny za kreowanie planu
#   @param StartState Warunki początkowe
#   @param Goals Zdefiniowane cele
#   @return Plan Wykreowany plan
def mutex_single_action(A, ActionLevel):
    pass

##
#   Predykat odpowiedzialny za kreowanie planu
#   @param StartState Warunki początkowe
#   @param Goals Zdefiniowane cele
#   @return Plan Wykreowany plan
def mutex_for_action_1(A1,A2):
    pass

##
#   Predykat odpowiedzialny za kreowanie planu
#   @param StartState Warunki początkowe
#   @param Goals Zdefiniowane cele
#   @return Plan Wykreowany plan
def mutex_for_action_2(A1,A2) :
    pass

##
#   Predykat odpowiedzialny za kreowanie planu
#   @param StartState Warunki początkowe
#   @param Goals Zdefiniowane cele
#   @return Plan Wykreowany plan
def mutex_for_action_3(A1,A2):
    pass

##
#   Predykat odpowiedzialny za kreowanie planu
#   @param StartState Warunki początkowe
#   @param Goals Zdefiniowane cele
#   @return Plan Wykreowany plan
def collect_vars(ActionIndicators, Vars):
    pass
