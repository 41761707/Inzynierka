import sys
import graphviz
import re
import itertools

## @package parsePlanFULL
#  Plik zawierający implementację klasy
#  Graph kreującej pełny graf dla zadanego problemu

class Graph:
    ## Konstruktor klasy Graph
    # @param filename nazwa pliku, z którego zostanie wygenerowany graf
    def __init__(self,filename):
        ## plik, z którego zostanie wygenerowany graf
        self.filename = filename
        ## Utworzony plan
        self.plan = []

    ## Funkcja odpowiedzialna za utworzenie 
    # krawędzi między stanami a akcjami
    # @param actions Zbiór akcji 
    # @param g Graf
    # @param level Poziom, dla którego kreowane są krawędzie
    def generateArcs(self,actions,g,level):
        level_higher = level + 1
        PreCond = []
        Effects = []
        for action_id, action_variables in actions.items():
            for i,variable in enumerate(action_variables):
                if(i==0):
                    PreCond = action_variables[variable]
                else:
                    Effects = action_variables[variable]
            for item in PreCond:
                if(action_id.startswith("zostan")):
                    g.edge(item+str(level),action_id+str(level),style='dashed')
                else:
                    g.edge(item+str(level),action_id+str(level))
            for item in Effects:
                if(action_id.startswith("zostan")):
                    g.edge(action_id+str(level),item+str(level_higher),style='dashed')
                else:
                    g.edge(action_id+str(level),item+str(level_higher))

    ##  Funkcja odpowiedzialna za zaznaczanie relacji wzajemnie wykluczających na grafie
    #   między stanami oraz między akcjami
    #   @param variables Stany(Akcje), które należy oznaczyć relacją wzajemnie wykluczającą
    #   @param g Graf
    #   @param level Poziom, dla którego należy wygenerować mutex'y

    def generateMutexArcs(self,variables,g,level):
        for i,pair in enumerate(variables):
            pair[0] = pair[0].lstrip(' [')
            pair[1] = pair[1].rstrip(']')
            new_pair = [pair[1],pair[0]]
            if new_pair not in variables[i:]:
                if 'idz' in pair[0] or 'idz' in pair[1] or 'zostan' in pair[0] or 'zostan' in pair[1]:
                    g.edge(pair[0]+str(level-1),pair[1]+str(level-1), style='dotted',arrowhead='none',constraint='false', color='blue')
                else:
                    g.edge(pair[0]+str(level),pair[1]+str(level), style='dotted',arrowhead='none',constraint='false', color='blue')

    ##  Funkcja odpowiedzialna za utworzenie poziomu stanów bądź akcji w grafie
    #   @param name Nazwa zbioru
    #   @param variables Stany(Akcje), które należy dodać do grafu
    #   @param g Graf
    #   @param level Poziom, dla którego należy wygenerować mutex'y
    #   @param type Typ węzła (okrąg- stan, prostokąt- akcja)

    def generateLayer(self,name,variables,g,level,type):
        layer_name = 'cluster_' + name
        with g.subgraph(name=layer_name) as layer:
            layer.attr(color='gray')
            layer.attr(label=name)
            for item in variables:
                layer.node(item+str(level),item, shape=type)
        

    ##  Funkcja odpowiedzialna za wczytanie pliku do zmiennej
    #   @param filename nazwa pliku
    def readInput(self,filename):
        file = []
        with open(filename) as input:
            for line in input:
                current_line = line.rstrip()
                file.append(current_line)
        return file

    ## Funkcja parsująca plik
    #   @param file wczytany plik w formie napisu
    #   @param g Graf 
    def parseInput(self,file,g):
        current_level = 1
        current_level_actions = {}
        mutex_states = []
        prev_action = ''
        for item in file:
            name,variables = item.split(':')
            variables = re.split(',(?![^(]*\\))',variables)
            variables[0] = variables[0][1:].lstrip('[')
            variables[len(variables)-1] = variables[len(variables)-1].rstrip(']')
            if(name == 'StartLevel'):
                name = 'StateLevel1'
                self.generateLayer(name,variables,g,current_level,"oval")
            elif(name == 'A'):
                prev_action = variables[0]
                current_level_actions[prev_action] = {}
            elif(name == 'Precondition'):
                current_level_actions[prev_action]['PreCond'] = variables
            elif(name == 'Effects'):
                current_level_actions[prev_action]['Effects'] = variables
            elif(name == 'Mutex'):
                variables[0] = variables[0].lstrip(' [')
                variables[1] = variables[1].rstrip(']')
                mutex_states.append(variables)
            elif(name == 'ActionLevel'):
                for element in mutex_states:
                    element.sort()
                mutex_states.sort()
                self.generateMutexArcs(list(mutex_states for mutex_states,_ in itertools.groupby(mutex_states)),g,current_level+1)
                mutex_states = []
                self.generateLayer(name+str(current_level),variables,g,current_level,"box")
            elif(name == 'StateLevel'):
                current_level = current_level + 1
                self.generateLayer(name+str(current_level),variables,g,current_level,"oval")
                self.generateArcs(current_level_actions,g,current_level-1)
                current_level_actions.clear()
            elif(name =='Plan'):
                variables = variables[1:].lstrip('[').rstrip(']').split(']')
                for i in range(1,len(variables)):
                    variables[i]=variables[i][2:]
                return variables, current_level

    ##  Funkcja odpowiedzialna za oczyszczenie planu ze zbędnych elementów
    #   @param plan Plan, który należy oczyścić

    def parsePlan(self,plan):
        parsed_plan = []
        for element in plan:
            parsed_plan.append(re.findall(',(?![^(]*\\))',element))

    ## Funkcja odpowiedzialna za zmianę koloru krawędzi prowadzących do otrzymania wskazanego rezultatu
    #   @param plan Plan zawierajacy akcje, których krawędzie należy wyszczególnić
    #   @param max_level Maksymalny rozmiar grafu
    #   @param g Graf

    def colorUsedActions(self,plan, max_level, g):
        nodes = []
        print(plan)
        for item in plan:
            for i,element in enumerate(g.body):
                if item+str(max_level) in element and '->' in element:
                    nodes_to_color = g.body[i].split('->')
                    nodes_to_color[0] = nodes_to_color[0][2:-3]+str(max_level)
                    nodes_to_color[1] = nodes_to_color[1][2:-3]+str(max_level+1)
                    nodes.append(nodes_to_color[0])
                    nodes.append(nodes_to_color[1])
                    #print(g.body[i])
                    g.body[i] = element[:len(element)-1] + ' [color=red]\n'
        print(nodes)
        for node in nodes:
            for i,element in enumerate(g.body):
                if node in element and '->' not in element and 'style=filled' not in element:
                    if 'oval' in element:
                        g.body[i] = element[:len(element)-12]+'colorfill=red shape=oval style=filled]\n'
                    else:
                        g.body[i] = element[:len(element)-11]+'colorfill=red shape=oval style=filled]\n'
                    break

    ##  Funkcja usuwająca z planu akcje podtrzymujące
    #   @param plan Plan
    def planWoPersist(self,plan):
        plan_wo_persist = []
        for element in plan:
            element = re.findall('idz\([a-z]+,[0-9]+,[0-9]+\)',element)
            plan_wo_persist.append(element)

    ##Funkcja odpowiedzialna za utworzenie grafu w formiace PNG

    def run_all(self):
        g = graphviz.Digraph('G', filename='graphs/FULL_GRAPHPLAN.gv',format='png')
        g.attr(ranksep = '2')
        file = self.readInput(self.filename)
        self.plan, max_level = self.parseInput(file, g)
        if(max_level < 5):
            g.attr(rankdir='LR')
        parsed_plan = self.parsePlan(self.plan)
        self.planWoPersist(self.plan)
        for i in range(max_level-1):
            self.colorUsedActions(self.plan[i],i+1,g)
        g.render()