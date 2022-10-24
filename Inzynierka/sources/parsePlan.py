import sys
import graphviz
import re


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
            pass
            g.edge(item+str(level),action_id+str(level))
        for item in Effects:
            pass
            g.edge(action_id+str(level),item+str(level_higher))


def generateLayer(name,variables,g,level):
    layer_name = 'cluster_' + name
    with g.subgraph(name=layer_name) as layer:
        layer.attr(color='gray')
        layer.attr(label=name)
        for item in variables:
            print(item)
            layer.node(item+str(level),item)
    

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
    prev_action = ''
    for item in file:
        name,variables = item.split(':')
        if(name == 'StartLevel'):
            name = 'StateLevel1'
            #print(variables)
            variables = re.findall('~?at\([a-z]+,[0-9]+\)|~?go\([a-z]+,[0-9]+,[0-9]+\)|~?clear\([0-9]+\)',variables)
            generateLayer(name,variables,g,current_level)
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
        elif(name == 'ActionLevel'):
            variables = re.findall('go\([a-z]+,[0-9]+,[0-9]+\)|~?persist\(at\([a-z]+,[0-9]+\)\)',variables)
            generateLayer(name+str(current_level),variables,g,current_level)
        elif(name == 'StateLevel'):
            current_level = current_level + 1
            variables = re.findall('~?at\([a-z]+,[0-9]+\)|~?go\([a-z]+,[0-9]+,[0-9]+\)|~?clear\([0-9]+\)',variables)
            generateLayer(name+str(current_level),variables,g,current_level)
            print(current_level_actions)
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