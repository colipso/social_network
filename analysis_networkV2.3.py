# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 15:36:37 2014

@author: pj
"""
#This is for github

import networkx
import triadic
import copy
#import draw_triads
import time
#import matplotlib.pyplot as plot
filepath='/home/pj/Python/social_analysis/friend.net'
sn=networkx.read_pajek(filepath)
ISOTIMEFORMAT='%Y-%m-%d %X'


def analysis_net(sn,top=10):
    #
    print '---------------%s开始整体分析----------------'%(time.strftime(ISOTIMEFORMAT,time.localtime(time.time())))
    longth_net=len(sn)
    deg=networkx.degree(sn)
    deg_sort=sorted(deg.iteritems(),cmp=lambda x,y:cmp(y[1],x[1]))
    #print deg_sort
    print '社交网总共有%d个好友'%(longth_net)
    print '排名前%d的好友数'%(top)
    for i in range(0,top):
        print '%d--%s--%.d'%(i+1,deg_sort[i][0],deg_sort[i][1])
    #基于closenes centrality    
    print '--------%s开始受欢迎指数分析(基于closenes centrality)------------'%(time.strftime(ISOTIMEFORMAT,time.localtime(time.time())))
    close_deg=networkx.closeness_centrality(sn)
    close_deg_sort=sorted(close_deg.iteritems(),cmp=lambda x,y:cmp(y[1],x[1]))
    print '受欢迎指数排名前%d的好友为'%(top)
    for i in range(0,top):
        print '%d--%s--%.2f'%(i+1,close_deg_sort[i][0],close_deg_sort[i][1])
        
        
    #基于Betweenness centrality算法    
    print '---------%s开始枢纽指数分析(基于Betweenness centrality算法 )----------'%(time.strftime(ISOTIMEFORMAT,time.localtime(time.time())))
    between_degree=networkx.betweenness_centrality(sn)
    between_degree_sort=sorted(between_degree.iteritems(),cmp=lambda x,y:cmp(y[1],x[1]))
    print '处于枢纽节点的前%d好友为'%(top)
    for i in range(0,top):
        print '%d--%s--%.2f'%(i+1,between_degree_sort[i][0],between_degree_sort[i][1])
        
    #基于Eigenvector centrality算法    
    print '----------%s开始幕后黑手指数分析(基于Eigenvector centrality算法)---------'%(time.strftime(ISOTIMEFORMAT,time.localtime(time.time())))
    try:
        black=networkx.eigenvector_centrality(sn)
        black_sort=sorted(black.iteritems(),cmp=lambda x,y:cmp(y[1],x[1]))
        print '幕后黑手指数最高的前%d个好友为'
        for i in range(0,top):
            print '%d--%s--%.2f'%(i+1,black_sort[i][0],black_sort[i][1])
    except Exception as err:
        print err
    
    #基于Google PageRank算法
    print '-------%s开始Google PageRank指数分析(基于Google PageRank算法)-------'%(time.strftime(ISOTIMEFORMAT,time.localtime(time.time())))
    try:
        pr=networkx.pagerank(sn)
        pr_sort=sorted(pr.iteritems(),cmp=lambda x,y:cmp(y[1],x[1]))
        print '按Google PageRank算法排名最高的%d个好友为'%(top)
        for i in range(0,top):
            print '%d--%s--%.2f'%(i+1,pr_sort[i][0],pr_sort[i][1])
    except  Exception as err:
        print err
    
    print '---------%s开始子图分析-------------------'%(time.strftime(ISOTIMEFORMAT,time.localtime(time.time())))
    try:
        sub=networkx.connected_component_subgraphs(sn)
        sub_num=len(sub)
        print '该社交网络可以分成%d个群体'%(sub_num)
        sub_group_num=[len(c) for c in sub]
        sub_group_num_sort=sorted(sub_group_num,cmp=lambda x,y:cmp(y,x))
        print '前%d个子群节点量为：'%(top)
        for i in range(0,len(sub)):
            print sub_group_num_sort[i]
    except Exception as err:
        print err
    
    print '=========%s分析完毕=============='%(time.strftime(ISOTIMEFORMAT,time.localtime(time.time())))
    
    
def get_ones_net(sn,core_name):
    try:
        ones_net=networkx.ego_graph(sn,core_name)
        print '%s的交往圈有%d人，社交网络为:'%(core_name,len(ones_net))
        for node in ones_net.nodes():
            print node
    except Exception as err:
        print err
        
    
    
def get_core_net(sn,degree=1):
    g=sn.copy()
    d=networkx.degree(g)
    for n in g.nodes():
        if d[n]<=degree:
            g.remove_node(n)
    return g
    
def short_way(g=sn,corename='colipso',isall=1,targetname=''):
    short=[]
    if isall==1:
        print '%s与交往圈中各朋友的最短路径'%(corename)
        try:
            for name in g.nodes():
                short.append(networkx.algorithms.shortest_path(g,corename,name))
        except Exception as err:
            print err
    else:
        print '%s与%s的最短路径'%(corename,targetname)
        try:
            short.append(networkx.algorithms.shortest_path(g,corename,targetname))
        except Exception as err:
            print err
            
    for node in short:
        print ''
        for subnode in node:
            print subnode,
            
    return short
    
def analyze_triads(sn):
    if not sn.is_directed:
        snd=networkx.DiGraph(sn)
    else:
        snd=sn
    census,node_census=triadic.triadic_census(snd)
    for key in census.keys():
        print '%s类型的三节点有%d个'%(key,census[key])
    
    return census,node_census
    
def draw_net(sn):
    try:
        print '----------------------%s开始绘图----------------------------'%(time.strftime(ISOTIMEFORMAT,time.localtime(time.time())))
        networkx.draw(core_net,node_size = 5,width=0.1,with_labels = False)
        print '============%s绘图成功！==============='%(time.strftime(ISOTIMEFORMAT,time.localtime(time.time())))
    except Exception as err:
        print err
        
    return 1

def get_cliques(sn):
    print '-----------%s开始紧密交往圈分析---------------'%(time.strftime(ISOTIMEFORMAT,time.localtime(time.time())))
    try:
        cliques=networkx.find_cliques(sn)
        j=0
        for i in cliques:
            print ''
            print '第%d个小圈子为:'%(j+1)
            j+=1
            for n in cliques.next():
                print n,
    except Exception as err:
        print err
    
    return cliques

    

analysis_net(sn)
core_net=get_core_net(sn,degree=2)
analysis_net(core_net)
draw_net(core_net)
analyze_triads(core_net)
get_cliques(core_net)
short_way(g=sn,corename='colipso')
