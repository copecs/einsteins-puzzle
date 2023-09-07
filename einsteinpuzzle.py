class Node:
    def __init__(self, value, canplay,parrent,winnable=0):
        self.value = value
        self.canplay = canplay
        self.childrens = []
        self.parrent=parrent
        self.winnable=winnable
    def add_child(self, child):
        self.childrens.append(child)

#unos i skupljanje uslova
def input_file(file_name,lines):
    if not file_name=="":
        inputFile=open(file_name,"r")
        lines=[i.strip() for i in inputFile]
    n=int(lines[0])
    m=int(lines[1])
    inputs=[]
    hates=[]
    itemshates=[]
    itemsloves=[]
    canplay=[[i for i in j.split(",")] for j in lines[3:3+n-1]]
    ljudi={j:i for i,j in enumerate(lines[2].split(","))}
    for i in range(m):
        inputs.append([""]*(n-1))
        hates.append(set([]))

    for i in lines[2+n:]:
        if i.find("+")>=0:
            if i.split("+")[0] in ljudi:
                index=ljudi[i.split("+")[0]]
                thing=i.split("+")[1]
                for key in ljudi.values():
                    if key!=index:
                        hates[key].add(thing)
            else:
                item_hates_or_loves_find_place(i.split("+")[0],i.split("+")[1],itemsloves)
        if i.find("-")>=0:
            if i.split("-")[0] in ljudi:
                hates[ljudi[i.split("-")[0]]].add(i.split("-")[1])
            else:
                item_hates_or_loves_find_place(i.split("-")[0],i.split("-")[1],itemshates)
    if not file_name=="":
        inputFile.close()
    return inputs,hates,itemshates,itemsloves,canplay,n,m,ljudi

def item_hates_or_loves_find_place(item1,item2,place):
    val=0
    for p in place:
        if item1 in p or item2 in p:
            p.add(item1)
            p.add(item2)
            val=1
            break
    if not val:
        place.append(set([item1,item2]))

#pravljenje drveta
def check_validity(inputs,hates,itemshates,itemsloves):
    for i,j in enumerate(inputs):
        for item in j:
            for person in range(len(hates)):
                if item in hates[person] and person==i:
                    return False
        for items in itemshates:
            if len(list(items.intersection(j)))>=2:
                return False

    for items in itemsloves:
        val=0
        for j in inputs:
            if len(list(items.intersection(j)))>0:
                val+=1
        if val>1:
            return False
    return True

def distinct_comb(combs,values):
    for comb in combs:
        if comb==values:
            return False
    return True

def winning_leaves(leaves,hates,itemshates,itemsloves):
    combs=[]
    nodes=[]
    br=0
    for leave in leaves:
        if check_validity(leave.value,hates,itemshates,itemsloves):
            br+=1
            if distinct_comb(combs,leave.value):
                nodes.append(leave)
                combs.append(leave.value)
            mark_winnable(leave)
    paths_to_win=br/len(nodes)
    return nodes,paths_to_win

def make_tree(inputs, hates, itemshates, itemsloves, canplay, n, m):
    root = Node(inputs, canplay,None)
    stack = [root]
    leaves = []
    #br=0
    while stack:
        node = stack.pop()
        #br+=1
        empty = True
        for row in node.canplay:
            if row:
                empty = False
                break
        if empty:
            leaves.append(node)
            continue
        if not check_validity(node.value, hates, itemshates, itemsloves):
            continue

        for i,plays in enumerate(node.canplay):
            for play in plays:
                for j in range(m):
                    if(node.value[j][i])!="":
                        continue
                    new_input=[l[:] for l in node.value]
                    new_input[j][i]=play
                    new_canplay=[[p for p in l if p!=play]for l in node.canplay]
                    new_node=Node(new_input,new_canplay,node)
                    node.add_child(new_node)
                    stack.append(new_node)
    #print(br)
    win_leaves,same_paths=winning_leaves(leaves,hates,itemshates,itemsloves)
    win_leaves.append(same_paths)
    return root, leaves, win_leaves

#ispis drveta
def print_tree(node):
    queue = [(node, 0)]
    curr_lvl = 0
    #br=0
    file=open("izlaz.txt",'w')
    while queue:
        node, level = queue.pop(0)
        if level > curr_lvl:
            print()
            curr_lvl = level
        if level==0:
            otac=""
        else:
            otac=str(node.parrent.value)
        print("  " * level + str(node.value)+"otac: "+otac)
        file.write("  " * level + str(node.value)+"otac: "+otac+"\n")
     #   br+=1
        for child in node.childrens:
            queue.append((child, level + 1))
    file.close()

#ispis kombinacija za pobedu
def findpath(node):
    stack=[]
    current_node=node
    while(current_node.parrent!=None):
        stack.append(current_node)
        current_node=current_node.parrent
    output=str(node.value)+"---->"
    while(stack):
        lista=stack.pop()
        lista=lista.value
        strr="["
        for sub in lista:
            strr+="["+", ".join(sub)+"] "
        strr+="]"
        output+=strr+"---->"
    return output[:-5]

def print_winning_combs(nodes):
    for node in nodes[:-1]:
        print(findpath(node)+" "+str(round(nodes[-1])))


#funkcija da oznaci da li se od zadatog cvora moze pobediti
def mark_winnable(node):
    current_node=node
    while(current_node!=None):
        current_node.winnable=1
        current_node=current_node.parrent


#korisnik igra igru
def inputzajedanpotez(node,ljudi):
    while(1):
        try:
            inp = input().split(":")
            if inp[0] not in ljudi:
                raise Exception
            t=0
            for predmeti in node.canplay:
                if inp[1] in predmeti:
                    t=1
            if t==0:
                raise Exception
            break
        except:
            print("Nevalidan unos")
    return inp

def jedanpotez(root,ljudi):
    checker=1
    inputs = [[x for x in row] for row in root.value]
    canplay=root.canplay
    while (checker):
        print("Odigraj potez")
        inp=inputzajedanpotez(root,ljudi)
        for i, list in enumerate(canplay):
            if inp[1] in list:
                index = i
                try:
                    inputs[ljudi[inp[0]]][index] = inp[1]
                    checker = 0
                except:
                    pass
        if not checker:
            break
        else:
            print("Nevalidan unos pokusaj opet")
    for child in root.childrens:
        if child.value==inputs:
            return child
    return -1

def printmenu():
    print("0:Prekid igre")
    print("1:Ispis stabla")
    print("2:Ispis resenja i puta do njih")
    print("3:Odigraj potez (Ime:stavka,primer=Maja:zuta)")
    print("4:Da li sam na dobrom putu?")
    print("5:Pomoc prijatelja")

def pomocprijatelja(node):
    if not node.winnable:
        return None
    for child in node.childrens:
        if child.winnable:
            return child

def printstanje(node,ljudi):
    for i,ljud in enumerate(ljudi):
        print("{}:{}  ".format(ljud,node.value[i]),end="")
    print()

def playgame(root,n,m,ljudi,win_leaves):
    current_node=root
    remaining_plays=(n-1)*m
    while(remaining_plays and current_node):
        printmenu()
        inp=input()
        if(inp=='0'):
            return
        elif(inp=='1'):
            print_tree(root)
        elif(inp=='2'):
            print_winning_combs(win_leaves)
        elif(inp=='3'):
            copy=current_node
            current_node = jedanpotez(current_node, ljudi)
            while(current_node==-1):
                print("Nevalidan unos unesi opet")
                current_node=copy
                current_node=jedanpotez(current_node,ljudi)
            remaining_plays-=1
        elif(inp=='4'):
            if(current_node.winnable):
                print("Na dobrom si putu!")
            else:
                print("Nisi na dobrom putu!")
        elif(inp=='5'):
            current_node = pomocprijatelja(current_node)
            remaining_plays-=1
        if(current_node.winnable):
            printstanje(current_node,ljudi)
        else:
            print("Izgubio si ukucaj undo da se vratis potez u nazad ili bilo sta za prekid igre")
            if(input().lower()=="undo"):
                current_node=current_node.parrent
                printstanje(current_node,ljudi)
                remaining_plays+=1
            else:
                break
    if(current_node and current_node.winnable):
        print("CESTITAMO POBEDIO SI!")
    else:
        print("IZGUBIO SI :'(")

#main
print("Ucitavanje igre:")
print("1:Unos iz fajla")
print("2:Unos iz konzole")
inp=input()
if inp=="1":
    print("Unesite ime fajla")
    inputs,hates,itemshates,itemsloves,canplay,n,m,ljudi=input_file(input(),[])
else:
    lines=[]
    lines.append(input())
    lines.append(input())
    for i in range(int(lines[0])):
        lines.append(input())
    inp=input()
    while(inp!=""):
        lines.append(inp)
        inp=input()
    inputs,hates,itemshates,itemsloves,canplay,n,m,ljudi=input_file("",lines)
root,leaves,win_leaves=make_tree(inputs,hates,itemshates,itemsloves,canplay,n,m)
playgame(root,n,m,ljudi,win_leaves)


