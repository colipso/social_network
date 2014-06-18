# -*- coding: utf-8 -*-
"""
Created on Fri May 30 19:26:38 2014

@author: pj
"""
import  urllib,urllib2,cookielib,re,networkx

def login_renren(username='colipso',password='254449597'):
    login_page = "http://www.renren.com/ajaxLogin/login"
    data = {'email': username, 'password':password}
    post_data = urllib.urlencode(data)
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    print u"登录人人网"
    req = opener.open(login_page, post_data)
    req = urllib2.urlopen("http://www.renren.com/home")
    html = req.read()
    uid = re.search("'ruid':'(\d+)'", html).group(1)#获取用户的uid"
    print  u"登陆成功"
    return uid,username
    
def get_friends(uid,start_name='colipso'):
    pagenum = 0
    Friend_list={start_name:[]}
    '''
    page = "http://friend.renren.com/GetFriendList.do?curpage=" + str(pagenum) + "&id=" + str(uid)
    res = urllib2.urlopen(page)
    html = res.read()
    pattern = 'id=(\d+)">(\S+)</a>'
    m = re.findall(pattern, html)
    print m
    '''
    while True:
        page = "http://friend.renren.com/GetFriendList.do?curpage=" + str(pagenum) + "&id=" + str(uid)
        res = urllib2.urlopen(page)
        html = res.read()
        pattern =u'id=(\d+)">(\S+)</a><span class'
        m = re.findall(pattern,html.decode('utf-8'))
        print  '第%d页的好友数为%d'%(pagenum,len(m))
        if len(m)<=1:
            break
        for i in range(0, len(m)):
            Friend_list[start_name].append([m[i][0],m[i][1]])
        pagenum += 1
        
    return Friend_list

g=networkx.Graph()
def snowball_getFriends(uid,username,max_depth=1,current_depth=0,friend={}):
    print '当前用户%s，当前深度%d，最大深度%d'%(username,current_depth,max_depth)
    if current_depth==max_depth:
        print '到达最深'
        return friend
    if username in friend.keys():
        return friend
    friend.update(get_friends(uid,username))
    for node in friend[username]:
            friend=snowball_getFriends(int(node[0]),node[1],current_depth=current_depth+1,max_depth=max_depth,friend=friend)
    return friend

def draw_network(friend_dic_list):
    print '开始绘制社交关系图'
    g=networkx.Graph()
    for name in friend_dic_list.keys():
        for node in friend_dic_list[name]:
            g.add_edge(name,node[1])
    networkx.draw(g,node_size = 1,width=0.01,with_labels = False)
    #networkx.draw_networkx(g,with_labels=False)
    
def save_friend_list(friend_list,path='/home/pj/Python/social_analysis/',filename='friend.net'):
    fullpath=path+filename
    print '开始保存社交关系'
    g=networkx.Graph()
    for name in friend_list.keys():
        for node in friend_list[name]:
            g.add_edge(name,node[1])
    networkx.write_pajek(g,fullpath)
    print '好友列表存储在%s'%(fullpath)
    return 1
    
login_renren()
#friend1=get_friends(308625592)
#friend=get_friends(253404471)
#for i in range(0,len(friend['colipso'])):
#    print i, friend['colipso'][i][0],friend['colipso'][i][1]
friend_net=snowball_getFriends(308625592,'colipso',2)
save_friend_list(friend_list=friend_net)

#draw_network(friend_net)
'''
for name in friend_net.keys():
    for i in range(0,len(friend_net[name])):
        print name,friend_net[name][i][0],friend_net[name][i][1]
'''
        