
def combine(g,w):
    """
        Takes two dictionarys 'g' and 'w' and returns a 
        dictionary of the two dictionarys combined.
            if g & w share a key, then the combination will be a list
            of the values.
    """

    for i in g.keys():
        if w.has_key(i):
            for a in g[i].keys():
                if w[i].has_key(a):
                    k = list(set([w[i][a],g[i][a]]))
                    print k
                    if len(k)==1:
                        w[i][a] = k[0]
                    else:
                        w[i][a] = k
                else:
                    w[i].update({a:g[i][a]}) 
        else:
            w.update({i:g[i]})
    return w

def printDict(g):
    print ("{:^2}| {:^4}| {:^4}| {:^4}".format('D','a','b','e'))
    print ('-'*20)
    nv = "/"
    for i in g:
        a = g[i]['a'] if g[i].has_key('a') else nv
        b = g[i]['b'] if g[i].has_key('b') else nv
        e = g[i]['&'] if g[i].has_key('&') else nv
        if i == 0:
            f = '>{}'.format(i)
        elif g[i].has_key('$'):
            f = '*{}'.format(i)
        else:
            f=i
        print ("{:^2}| {:^4}| {:^4}| {:^4}".format(f,a,b,e))

def hasValue(g,v):
    flatten = [a for i,l in g.items() for a in l.items()]
    keys = [i for i,a in flatten]
    values = [i for a,i in flatten]
    return v in keys

def changeValues(g,check,new):
    for i in g.keys():
        for k,a in g[i].items():
            if type(check) == list:
                for l in check:
                    if a == l:
                        g[i][k] = new
            else:
                if a == check:
                    g[i][k] = new 
    return g 

def parseRecur(I,w={},curpos=0,nextpos=1,t=0): 


    if I == "\t":#
        w.update({curpos:{"$":-1}})
        return w,"",curpos,nextpos

    alpha = I[0]
    beta = I[1:]
    nu = beta[0] if beta != "" else None 

    if alpha == "+":#
        n = min(w.keys())         
        g,b,c,n = parseRecur(I=beta,curpos=n,nextpos=nextpos,w={},t=curpos)
        
        if hasValue(g,'$'):
            beg,end = max(g.keys()),curpos
            p = [i for i,a in g.items() for l,a in a.items() if l == "$"] 
            for i in p:
                del g[i]
            g = changeValues(g,p,end)
            g.update({end:{'$':-1}})

        else:
            end = max([a for i,a in w[max(w.keys())].items()])
            check = max([a for i,a in g[max(g.keys())].items()])
            g = changeValues(g,check,end)

        k = combine(g,w)
        return k,b,curpos,c

    elif alpha == "(":
        g,b,c,n = parseRecur(I=beta,w={},t=t,curpos=curpos,nextpos=nextpos)
        beta = b 
        curpos = c
        nextpos = n
        nu = beta[0] if beta != "" else None

        if nu == '*':
            beg,end = min(g.keys()),max(g.keys()) 
            for i in g:
                for a in g[i]:
                    if g[i][a] == curpos:
                        g[i][a] = beg
            g[beg].update({'&':curpos})

        w.update(g)
    
    elif alpha == ")":#
        return w,beta,curpos,nextpos

    elif alpha == "*":
        pass

    else:
        if nu == "*":
            w.update({curpos:{alpha:curpos,'&':nextpos}})
        else:
            w.update({curpos:{alpha:nextpos}})
        curpos=nextpos
        nextpos+=1

    return parseRecur(I=beta,w=w,curpos=curpos,nextpos=nextpos,t=t)

def parse(regex):
    """Takes a string 'regex' and returns a dictionary of the RE as an NFA"""
    regex = ''.join(regex.split(" "))+"\t"
    F,_,_,_ = parseRecur(regex)
    return F

if __name__ == "__main__": 
    #regex = raw_input("Enter Regular Expression: ")
    #F = parse(regex)
    #printDict(F)
    G = {1:{'a':2}}
    W = {1:{'a':3,'b':3}}

    print combine(G,W)
