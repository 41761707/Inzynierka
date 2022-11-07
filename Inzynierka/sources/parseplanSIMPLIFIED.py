import sys
import graphviz
import re
import itertools

class SimplifiedGraph:
    def __init__(self,filename):
        self.filename = filename
        self.plan = []

    def return_plan(self):
        return self.plan

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
                    pass
                    #g.edge(item+str(level),action_id+str(level),style='dashed')
                else:
                    g.edge(item+str(level),action_id+str(level))
            for item in Effects:
                if(action_id.startswith("zostan")):
                    pass
                    #g.edge(action_id+str(level),item+str(level_higher),style='dashed')
                else:
                    g.edge(action_id+str(level),item+str(level_higher))


    #TO-DO: split into generateMutexArcsStates and generateMutexArcsActions

    def generateMutexArcs(self,variables,g,level):
        for i,pair in enumerate(variables):
            new_pair = [pair[1],pair[0]]
            if new_pair not in variables[i:]:
                g.edge(pair[0]+str(level),pair[1]+str(level), style='dotted',arrowhead='none',constraint='false')


    def generateLayer(self,name,variables,g,level,type):
        layer_name = 'cluster_' + name
        with g.subgraph(name=layer_name) as layer:
            layer.attr(color='gray')
            layer.attr(label=name)
            for item in variables:
                layer.node(item+str(level),item, shape=type)
        

    def readInput(self,filename):
        file = []
        with open(filename) as input:
            for line in input:
                current_line = line.rstrip()
                file.append(current_line)
        return file

    def parseInput(self,file,g):
        current_level = 1
        current_level_actions = {}
        used_actions = {}
        mutex_states = []
        prev_action = ''
        for item in file:
            name,variables = item.split(':')
            if(name == 'StartLevel'):
                name = 'StateLevel1'
                #print(variables)
                variables = re.findall('~?na\([a-z]+,[a-z0-9]+\)|~?idz\([a-z]+,[a-z0-9]+,[a-z0-9]+\)|~?pusty\([a-z0-9]+\)',variables)
                variables = [x for x in variables if "~" not in x]
                self.generateLayer(name,variables,g,current_level,"oval")
            elif(name == 'A'):
                prev_action = variables.strip()
                current_level_actions[prev_action] = {}
                #print('A: ', variables)
            elif(name == 'Precondition'):
                variables = re.findall('~?na\([a-z]+,[a-z0-9]+\)|~?idz\([a-z]+,[a-z0-9]+,[a-z0-9]+\)|~?pusty\([a-z0-9]+\)',variables)
                variables = [x for x in variables if "~" not in x]
                current_level_actions[prev_action]['PreCond'] = variables
                #print('Precondition: ',variables)
            elif(name == 'Effects'):
                variables = re.findall('~?na\([a-z]+,[a-z0-9]+\)|~?idz\([a-z]+,[a-z0-9]+,[a-z0-9]+\)|~?pusty\([a-z0-9]+\)',variables)
                variables = [x for x in variables if "~" not in x]
                current_level_actions[prev_action]['Effects'] = variables
                #print('Effects: ',variables)
            elif(name == 'Mutex'):
                pass
                #variables = re.findall('~?na\([a-z]+,[a-z0-9]+\)|~?idz\([a-z]+,[a-z0-9]+,[a-z0-9]+\)|~?pusty\([a-z0-9]+\)',variables)
                #variables = [x for x in variables if "~" not in x]
                #mutex_states.append(variables)
            elif(name == 'ActionLevel'):
                #mutex_states.sort()
                #self.generateMutexArcs(list(mutex_states for mutex_states,_ in itertools.groupby(mutex_states)),g,current_level+1)
                #mutex_states = []
                variables = re.findall('idz\([a-z]+,[a-z0-9]+,[a-z0-9]+\)',variables)
                variables = [x for x in variables if "~" not in x]
                self.generateLayer(name+str(current_level),variables,g,current_level,"box")
            elif(name == 'StateLevel'):
                current_level = current_level + 1
                variables = re.findall('~?na\([a-z]+,[a-z0-9]+\)|~?idz\([a-z]+,[a-z0-9]+,[a-z0-9]+\)|~?pusty\([a-z0-9]+\)',variables)
                variables = [x for x in variables if "~" not in x]
                self.generateLayer(name+str(current_level),variables,g,current_level,"oval")
                #print(current_level_actions)
                #used_actions = {k: current_level_actions[k] for k in variables}
                #current_level_actions.clear()
                #generateArcs(used_actions,g,current_level-1)
                self.generateArcs(current_level_actions,g,current_level-1)
                current_level_actions.clear()
                #used_actions.clear()
            elif(name =='Plan'):
                variables = variables[1:].lstrip('[').rstrip(']').split(']')
                for i in range(1,len(variables)):
                    variables[i]=variables[i][2:]
                return variables, current_level

    def parsePlan(self,plan):
        parsed_plan = []
        for element in plan:
            parsed_plan.append(re.findall('idz\([a-z]+,[a-z0-9]+,[a-z0-9]+\)',element))
            element = [x for x in element if "~" not in x]
            #element = re.findall('idz\([a-z]+,[0-9]+,[0-9]+\)|zostan\(~?na\([a-z]+,[0-9]+\)\)|zostan\(~?pusty\([0-9]+\)\)',element)

    def colorUsedActions(self,plan, max_level, g):
        plan = re.findall('idz\([a-z]+,[a-z0-9]+,[a-z0-9]+\)',plan)
        plan = [x for x in plan if "~" not in x]
        for item in plan:
            for i,element in enumerate(g.body):
                if item+str(max_level) in element and '->' in element and '[style=dashed]' not in element:
                    g.body[i] = element[:len(element)-1] + ' [color=red]\n'

    def planWoPersist(self,plan):
        plan_wo_persist = []
        for element in plan:
            element = re.findall('idz\([a-z]+,[0-9]+,[0-9]+\)',element)
            plan_wo_persist.append(element)

    def run_all(self):
        g = graphviz.Digraph('G', filename='SIMPLE_GRAPHPLAN.gv',format='pdf')
        #g = graphviz.Digraph('G', filename='FULL_GRAPHPLAN.gv')
        file = self.readInput(self.filename)
        self.plan, max_level = self.parseInput(file, g)
        if(max_level < 5):
            g.attr(rankdir='LR')
        parsed_plan = self.parsePlan(self.plan)
        self.planWoPersist(self.plan)
        #for element in g.body:
        #    print(element)
        for i in range(max_level-1):
            self.colorUsedActions(self.plan[i],i+1,g)
        g.render()
        #g.view()