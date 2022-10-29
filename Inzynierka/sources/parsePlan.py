import sys
import graphviz
import re
import itertools


def generateArcs(actions,g,level):
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
            if(action_id.startswith("persist")):
                g.edge(item+str(level),action_id+str(level),style='dashed')
            else:
                g.edge(item+str(level),action_id+str(level))
        for item in Effects:
            if(action_id.startswith("persist")):
                g.edge(action_id+str(level),item+str(level_higher),style='dashed')
            else:
                g.edge(action_id+str(level),item+str(level_higher))

def generateMutexArcs(variables,g,level):
    #print(variables)
    for i,pair in enumerate(variables):
        new_pair = [pair[1],pair[0]]
        if new_pair not in variables[i:]:
            g.edge(pair[0]+str(level),pair[1]+str(level), style='dotted',arrowhead='none',constraint='false')
        
        #g.edge(pair[0]+str(level),pair[1]+str(level), color='lightblue',arrowhead='none',constraint='false')


def generateLayer(name,variables,g,level,type):
    layer_name = 'cluster_' + name
    with g.subgraph(name=layer_name) as layer:
        #layer.attr(color='white')
        layer.attr(color='gray')
        layer.attr(label=name)
        #layer.attr('node', shape='box')
        for item in variables:
            #print(item)
            layer.node(item+str(level),item, shape=type)
    

def readInput(filename):
    file = []
    with open(filename) as input:
        for line in input:
            current_line = line.rstrip()
            file.append(current_line)
    return file

def parseInput(file,g):
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
            variables = re.findall('~?at\([a-z]+,[0-9]+\)|~?go\([a-z]+,[0-9]+,[0-9]+\)|~?clear\([0-9]+\)',variables)
            generateLayer(name,variables,g,current_level,"oval")
        elif(name == 'A'):
            prev_action = variables.strip()
            current_level_actions[prev_action] = {}
            #print('A: ', variables)
        elif(name == 'PreCond'):
            variables = re.findall('~?at\([a-z]+,[0-9]+\)|~?go\([a-z]+,[0-9]+,[0-9]+\)|~?clear\([0-9]+\)',variables)
            current_level_actions[prev_action]['PreCond'] = variables
            #print('PreCond: ',variables)
        elif(name == 'Effects'):
            variables = re.findall('~?at\([a-z]+,[0-9]+\)|~?go\([a-z]+,[0-9]+,[0-9]+\)|~?clear\([0-9]+\)',variables)
            current_level_actions[prev_action]['Effects'] = variables
            #print('Effects: ',variables)
        elif(name == 'Mutex'):
            variables = re.findall('~?at\([a-z]+,[0-9]+\)|~?go\([a-z]+,[0-9]+,[0-9]+\)|~?clear\([0-9]+\)',variables)
            mutex_states.append(variables)
        elif(name == 'ActionLevel'):
            mutex_states.sort()
            generateMutexArcs(list(mutex_states for mutex_states,_ in itertools.groupby(mutex_states)),g,current_level+1)
            mutex_states = []
            variables = re.findall('go\([a-z]+,[0-9]+,[0-9]+\)|persist\(~?at\([a-z]+,[0-9]+\)\)|persist\(~?clear\([0-9]+\)\)',variables)
            generateLayer(name+str(current_level),variables,g,current_level,"box")
        elif(name == 'StateLevel'):
            current_level = current_level + 1
            variables = re.findall('~?at\([a-z]+,[0-9]+\)|~?go\([a-z]+,[0-9]+,[0-9]+\)|~?clear\([0-9]+\)',variables)
            generateLayer(name+str(current_level),variables,g,current_level,"oval")
            #print(current_level_actions)
            #used_actions = {k: current_level_actions[k] for k in variables}
            #current_level_actions.clear()
            #generateArcs(used_actions,g,current_level-1)
            generateArcs(current_level_actions,g,current_level-1)
            current_level_actions.clear()
            #used_actions.clear()




def main():
    g = graphviz.Digraph('G',filename='GRAPHPLAN.gv')
    file = readInput(sys.argv[1])
    parseInput(file,g)
    g.attr(rankdir='LR')

    
    g.view()

if __name__=='__main__':
    main()