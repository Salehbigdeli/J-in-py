import operator
from ctypes import *
from functools import reduce

LIB = "libj.so"
cmd = "cmd"

def mulall(arr):    
    return reduce(operator.mul,arr,1)

def run_jcmd(cmd):    
    j.JDo(p, cmd)

def get_result(jdll,variable=cmd):    
    pi=[pointer(c_int()) for _ in range(4)]    
    j.JGetM(jdll,variable,*pi) 
    type=pi[0].contents.value  
    print('type is ', type)  
    if type==0: #error        
        return None,None,None,None    
    rank=pi[1].contents.value    
    shape=list((c_int*rank).from_address(pi[2].contents.value))    
    flat_size=mulall(shape)    
    data=list((c_int*flat_size).from_address(pi[3].contents.value))
    return type,rank,shape, resize2(shape,data)

def res(jdll,var):
    pntrs = [pointer(c_int()) for _ in range(4)]
    j.JGetM(jdll,var,*pntrs)
    
    return list((c_int).from_address(pntrs[3].contents.value))

def resize2(shap,dat):    
    shap=shap[:]    
    flat_size=mulall(shap)    
    while len(shap)>1:        
        shd=[]        
        start=0        
        last_size=shap.pop()        
        while start<flat_size:            
            shd.append(dat[start:start+last_size])            
            start+=last_size        
        flat_size=len(shd)        
        dat=shd    
    else:            
        shd=dat    
    return shd



cdll.LoadLibrary(LIB)
j = CDLL(LIB)
p=j.JInit()


def ask_j(arg):
    run_jcmd("rez =: "+arg)
    return get_result(p, "rez") 

def setup_grid(size):
    run_jcmd("arr =: ([ ? #/~) "+str(size))
    return get_result(p, "arr")

def rotate_column(rotdir, colIndex):
    rs = list(str(rotdir))
    if rs[0] == '-':
        rs[0] = '_'
    rs = ''.join(rs)
    run_jcmd("arr =:("+rs+"|."+str(colIndex)+"{\"2 arr)"+str(colIndex)+"}\"2 arr")
    return get_result(p, "arr")

def rotate_row(rotdir, rowIndex):
    rs = list(str(rotdir))
    if rs[0] == '-':
        rs[0] = '_'
    rs = ''.join(rs)
    run_jcmd("arr =: |: ("+rs+"|."+str(rowIndex)+"{\"2 |: arr)"+str(rowIndex)+"}\"2 |: arr")
    return get_result(p, "arr")

def reflect():
    run_jcmd("arr =: |. arr")
    return get_result(p, "arr")

def transpose():
    run_jcmd("arr =: |: arr")
    return get_result(p, "arr")

def did_win():
    # we win if testing each row for equality of elements has no zeros.
    run_jcmd("win =: -. 0 e. , =\"1 arr")
    return get_result(p, "win")