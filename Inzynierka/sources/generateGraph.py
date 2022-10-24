import graphviz

g = graphviz.Digraph('G',filename='generatedGraph.gv')

with g.subgraph(name='cluster_StateLevel1') as SL1:
    SL1.attr(color='gray')
    SL1.attr(label='StateLevel1')
    SL1.node('at(A,1)')
    SL1.node('at(B,2)')
    SL1.node('at(C,3)')
    SL1.node('clear(4)')
    SL1.node('clear(5)')
    SL1.node('clear(6)')

with g.subgraph(name='cluster_ActionLevel1') as AL1:
    AL1.attr(color='gray')
    AL1.attr(label='ActionLevel1')
    AL1.node('go(a,1,4)')   
    AL1.node('persist(at(b,2))')
    AL1.node('persist(at(c,3))')
    AL1.node('persist(clear(4))')
    AL1.node('persist(clear(5))')
    AL1.node('persist(clear(6))')

g.edge('at(A,1)','go(a,1,4)')
g.attr(rankdir='LR')
g.view()
