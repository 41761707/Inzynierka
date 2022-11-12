import sys
import graphviz
import re
import itertools

class GraphWOZostan:
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
                    g.edge(item+str(level),action_id+str(level),style='dashed')
                else:
                    g.edge(item+str(level),action_id+str(level))
            for item in Effects:
                if(action_id.startswith("zostan")):
                    pass
                    g.edge(action_id+str(level),item+str(level_higher),style='dashed')
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
                items = item.split('/')
                if(items[1] == '1'):
                    layer.node(items[0]+str(level),items[0], shape=type)
                else:
                    pass
                    #layer.node(items[0]+str(level),items[0], shape=type)
        

    def readInput(self,filename):
        file = []
        with open(filename) as input:
            for line in input:
                current_line = line.rstrip()
                file.append(current_line)
        return file

    def parseInput(self,file,g):
        current_level = 1
        all_actions = {}
        used_actions = {}
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
                all_actions[prev_action] = {}
                #print('A: ', variables)
            elif(name == 'Precondition'):
                all_actions[prev_action]['PreCond'] = variables
                #print('Precondition: ',variables)
            elif(name == 'Effects'):
                all_actions[prev_action]['Effects'] = variables
                #print('Effects: ',variables)    
            elif(name=='ChosenActions'):
                for variable in variables:
                    for key in all_actions.keys():
                        if variable in key and '~' not in variable:
                            used_actions[key]=all_actions[key]
                for i in range(len(variables)):
                    if '~' not in variables[i]:
                        variables[i] = variables[i] + '/1'
                    else:
                        variables[i] = variables[i] + '/0'
                self.generateLayer('ActionLevel'+str(current_level),variables,g,current_level,"box")
                self.generateArcs(used_actions,g,current_level)
                current_level = current_level+1
                used_actions.clear()
            elif(name=='ChosenStates'):
                self.generateLayer('StateLevel'+str(current_level),variables,g,current_level,"oval")
            elif(name=='Plan'):
                return variables,current_level


    def parsePlan(self):
        print(self.plan)
        #parsed_plan = []
        #for element in self.plan:
        #    if 'idz' in element:
        #        parsed_plan.append(element.rstrip(']'))
        #return parsed_plan

    def colorUsedActions(self,plan, max_level, g):
        print(plan)
        plan = re.findall('idz\([a-z]+,[a-z0-9]+,[a-z0-9]+\)',plan)
        print(plan)
        for item in plan:
            for i,element in enumerate(g.body):
                if item+str(max_level) in element and '->' in element:
                    print(g.body[i])
                    g.body[i] = element[:len(element)-1] + ' [color=red]\n'
        

    def run_all(self):
        g = graphviz.Digraph('G', filename='graphs/GRAPHPLAN_WOZOSTAN.gv',format='pdf')
        file = self.readInput(self.filename)
        self.plan, max_level = self.parseInput(file, g)
        if(max_level < 5):
            g.attr(rankdir='LR')
        parsed_plan = self.parsePlan()
        print(parsed_plan)
        #for element in g.body:
        #    print(element)
        #for i in range(max_level-1):
        #    self.colorUsedActions(parsed_plan[i],i+1,g)
        g.render()
        g.view()      

def main():
    g = SimplifiedGraph('outputs/output.txt')
    g.run_all()

if __name__ == '__main__':
    main()