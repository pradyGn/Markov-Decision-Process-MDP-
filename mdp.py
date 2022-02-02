#!/usr/bin/env python
# coding: utf-8

# In[874]:


file_name = input("Input file name: " )
G = open(file_name,'r')
with open(file_name) as G:
    lines = G.readlines()
G.close()


# In[875]:


df = input("Enter discount factor (default df = 1.0): ")


# In[876]:


min_max = input("Enter min or max (default is max): ")


# In[877]:


tol = input("Enter tol value (default tol = 0.01): ")


# In[878]:


cutoff = input("Enter an integer that indicates a cutoff for value iteration (default cutoff = 100): ")


# In[879]:


if len(df) == 0:
    df = 1.0
else:
    df = float(df)
if len(min_max) == 0:
    min_max = "max"
if len(tol) == 0:
    tol = 0.01
else:
    tol = float(tol)
if len(cutoff) == 0:
    cutoff = 100
else:
    cutoff = int(cutoff)


# In[880]:


tol_track = 0
while tol != 1:
    tol = tol*10
    tol_track += 1


# In[881]:


def getspc(l):
    spc = []
    for j in range(len(l)):
        if l[j] == ' ':
            spc.append(j)
    return spc


# In[882]:


IN = []

for l in lines:
    if l[0] != '#' and l[0] != '\n':
        if l[-1] == "\n":
            IN.append(l[:len(l)-1])
        else:
            IN.append(l)

#print(IN)


# In[883]:


def rmscb(lst):
    ret = []
    rm = ['[', ']', ',', ' ']
    for l in lst:
        if l not in rm:
            ret.append(l)
    return ret


# In[884]:


def makelst(l):
    ret = []
    final = []
    spc = getspc(l)
    spc.append(len(l))
    for i in range(1, len(spc)):
        ret.append(l[spc[i-1]+1:spc[i]])
        
    nope = ",[]"
    for ele in ret:
        for character in nope:
            ele = ele.replace(character, "")
        final.append(ele)
        
    return final


# In[885]:


def appnd(l):
    ret = []
    spc = getspc(l)
    spc.append(len(l))
    for s in range(1, len(spc)):
        ret.append(float(l[spc[s-1]:spc[s]]))
    return ret


# In[886]:


import copy

equations = {}

ctr = "[], "
ctrnl = "\n"

#for l in IN:
#    if ':' in l:
#        steps = makelst(l[l.find(':')+1:])
#        equations[l[:l.find(':')-1]] = steps
        
for l in IN:
    if ':' in l:
        idx = l.find(':')
        ele = ''
        if l[idx-1] == ' ':
            equations[l[:idx-1]] = []
            ele = l[:idx-1]
        else:
            equations[l[:idx]] = []
            ele = l[:idx]
            
        if l[idx+1] == ' ':
            temp = l[idx+2:]
            spc = getspc(temp)
            spc.insert(0, -1)
            spc.append(len(temp))
            for s in range(1, len(spc)):
                temp1 = temp[spc[s-1]+1:spc[s]]
                for c in ctr:
                    temp1 = temp1.replace(c, "")
                equations[ele].append(temp1)
        else:
            temp = l[idx+1:]
            spc = getspc(temp)
            spc.insert(0, -1)
            spc.append(len(temp))
            for s in range(1, len(spc)):
                temp1 = temp[spc[s-1]+1:spc[s]]
                for c in ctr:
                    temp1 = temp1.replace(c, "")
                equations[ele].append(temp1)

rew = {}

#for l in IN:
#    if '=' in l:
#        rew[l[:l.find('=')]] = float(l[l.find('=')+1:])

for l in IN:
    if '=' in l:
        idx = l.find('=')
        if l[idx-1] == ' ':
            if l[idx+1] == ' ':
                rew[l[:idx-1]] = float(l[idx+2:])
            else:
                rew[l[:idx-1]] = float(l[idx+1:])
        else:
            if l[idx+1] == ' ':
                rew[l[:idx]] = float(l[idx+2:])
            else:
                rew[l[:idx]] = float(l[idx+1:])
        

#for l in IN:
#    if '=' not in l:
#        spc = getspc(l)
#        if l[:spc[0]] not in var:
#            rew[l[:spc[0]]] = 0.0

for ele in equations:
    if ele not in rew:
        rew[ele] = 0.0
    for step in equations[ele]:
        if step not in rew:
            rew[step] = 0.0
            

#for ele in equations:
#    if ele not in rew:
#        rew[ele] = 0.0
#    for step in equations[ele]:
#        if step not in rew:
#            rew[step] = 0.0
            
chance = {}
decision = {}

#for l in IN:
#    if '%' in l:
#        spc = getspc(l[l.find('%')+1:])
#        if len(spc) > 1:
#            ret = appnd(l[l.find('%')+1:])
#            chance[l[:l.find(' ')]] = ret
#        else:
#            decision[l[:l.find(' ')]] = float(l[l.find('%')+2:])


for l in IN:
    if '%' in l:
        idx = l.find('%')
        ele = ''
        if l[idx-1] == ' ':
            ele = l[:idx-1]
        else:
            ele = l[:idx]
        idxd = l.find('.')
        temp = l[idxd:]
        temp.replace(ctrnl, "")
        if l.count('.') == 1:
            decision[ele] = float(temp)
        elif l.count('.') > 1:
            spc = getspc(temp)
            spc.insert(0, -1)
            spc.append(len(temp))
            chance[ele] = []
            for s in range(1, len(spc)):
                chance[ele].append(float(temp[spc[s-1]+1:spc[s]]))



for node in equations:
    if node not in chance and node not in decision:
        decision[node] = 1.0

var = copy.deepcopy(rew)

#print(equations)
#print(rew)
#print(var)
#print(chance)
#print(decision)


# In[887]:


pol = {}

for ele in decision:
    pol[ele] = 0
    
#print(pol)


# In[888]:


def check(ele, step, decision, cur_var, chance):
    print("\n")
    print(ele)
    if ele in decision:
        print(step)
        print(var[step])
        print(decision[ele])
    if ele in chance:
        print(equations[ele][step])
        print(var[equations[ele][step]])
        print(chance[ele])
    print(cur_var)
    print("\n")


# In[889]:


def valiter(equations, decision, chance, pol, var, rew, tol_track):
    cur_var = {}
    for ele in equations:
        if ele in decision:
            cur_var[ele] = rew[ele] #changed 0 to var[ele] to rew[ele]
            
            if decision[ele] < 1:
                rem_pm = round((1-decision[ele])/(len(equations[ele])-1), tol_track)
            else:
                rem_pm = 0.0
            
            #print(rem_pm)
            for step in equations[ele]:
                if equations[ele].index(step) == pol[ele]:
                    cur_var[ele] += df*decision[ele]*var[step]
                else:
                    cur_var[ele] += df*rem_pm*var[step]
                #check(ele, step, decision, cur_var, chance)
                
        elif ele in chance:
            cur_var[ele] = rew[ele] #changed 0 to var[ele] to rew[ele]
            for step in range(len(equations[ele])):
                cur_var[ele] += df*chance[ele][step]*var[equations[ele][step]] #changes made
                #check(ele, step, decision, cur_var, chance)
        
        cur_var[ele] = round(cur_var[ele], 4)
    
    for ele in var:
        if ele not in equations:
            cur_var[ele] = var[ele]
    
    return cur_var


# In[890]:


def GreedyPolComp(cur_var, pol, equations, decision, min_max):
    #print(decision)
    #print(cur_var)
    new_pol = {}
    for ele in decision: #changed from equations to decision
        temp = {}
        for step in equations[ele]:
            temp[cur_var[step]] = step
        #print(temp)
        if min_max == "max":
            new_pol[ele] = equations[ele].index(temp[max(temp)])
        else:
            new_pol[ele] = equations[ele].index(temp[min(temp)])
    
    return new_pol


# In[891]:


def MarkovPS(equations, decision, chance, pol, var, rew, tol_track, min_max):
    for i in range(cutoff):
        cur_var = valiter(equations, decision, chance, pol, var, rew, tol_track)
        #print(cur_var)
        new_pol = GreedyPolComp(cur_var, pol, equations, decision, min_max)
        #print(new_pol)
        
        #print(pol)
        #print(new_pol)
        
        if list(new_pol.values()) == list(pol.values()) and list(cur_var.values()) == list(var.values()):
            return new_pol, cur_var
        
        pol = new_pol
        var = cur_var #new line added


# In[892]:


"""
def check(ele, step, decision, cur_var, chance):
    print("\n")
    print(ele)
    if ele in decision:
        print(step)
        print(var[step])
        print(decision[ele])
    if ele in chance:
        print(equations[ele][step])
        print(var[equations[ele][step]])
        print(chance[ele])
    print(cur_var)
    print("\n")
"""


# In[893]:


new_pol, cur_var = MarkovPS(equations, decision, chance, pol, var, rew, tol_track, min_max)


# In[894]:


for ele in new_pol:
    if len(equations[ele])>1:
        print(ele + ' -> ' + equations[ele][new_pol[ele]])
    
print(cur_var)


# In[ ]:




