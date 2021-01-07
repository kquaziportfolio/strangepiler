import click
import random as r
import time as t
click.arg=click.argument

class StackMachine:
    def __init__(self):
        self.stack=[]
    def pop(self):
        return self.stack.pop()
    def push(self,element):
        self.stack.append(element)

class VarMachine:
    def __init__(self):
        self.vars={}

class RandomMachine:
    def __init__(self,cmd):
        self.cmd=cmd
    def seed(self):
        r.seed(self.stack.cmd.pop())
    def randomint(self):
        ubound=self.cmd.stack.pop()
        lbound=self.cmd.stack.pop()
        self.cmd.stack.push(r.randint(lbound,ubound))
    def seed(self):
        seed=self.cmd.stack.pop()
        r.seed(seed)
    def random(self):
        self.cmd.stack.push(r.random())
    def choice(self,a):
        self.cmd.stack.push(r.choice(self.vars.vars[a]))

class TimeMachine:
    def __init__(self,cmd):
        self.cmd=cmd
    def time(self):
        self.cmd.stack.push(t.time())
    def sleep(self):
        t.sleep(self.cmd.stack.pop())

class CompiledCode:
    def __init__(self,code):
        self.code=code

class CommandMachine:
    def __init__(self):
        self.stack=StackMachine()
        self.vars=VarMachine()
        self.randommachine=RandomMachine(self)
        self.timemachine=TimeMachine(self)
    def allocate_command(self,command,line,*args):
        if "." in command:
            cl=command.split(".")[0]
            command=command.split(".")[1:]
            getattr(getattr(self,"".join(cl)+"machine"),".".join(command))(*args)
            return
        try:
            getattr(self,"do_"+command)(*args)
        except AttributeError as e:
            print(f"STRANGEPILER EXCEPTION (line {line}): No such command, \"{command}\".")
            exit()

    def do_push(self,*element):
        self.stack.push(",".join(element))
    def do_write(self):
        print(self.stack.pop(),end="")
    def do_number(self):
        self.stack.push(int(self.stack.pop()))
    def do_string(self):
        self.stack.push(str(self.stack.pop()))
    def do_add(self):
        e1=self.stack.pop()
        e2=self.stack.pop()
        self.stack.push(e2+e1)
    def do_multiply(self):
        e1=self.stack.pop()
        e2=self.stack.pop()
        self.stack.push(e2*e1)
    def do_store(self,name):
        self.vars.vars[name]=self.stack.pop()
    def do_bool(self):
        self.stack.push(bool(self.stack.pop()))
    def do_retrieve(self,name):
        self.stack.push(self.vars.vars[name])
    def do_createarray(self,name,size):
        self.vars.vars[name]=[None]*int(size)
    def do_getelement(self,name,pos):
        self.stack.push(self.vars.vars[name][int(pos)])
    def do_setelement(self,name,pos):
        self.vars.vars[name][int(pos)]=self.stack.pop()
    def do_removevar(self,name):
        del self.vars.vars[name]
    def do_divide(self):
        e2=self.stack.pop()
        e1=self.stack.pop()
        self.stack.push(e1/e2)
    def do_intdivide(self):
        e2=self.stack.pop()
        e1=self.stack.pop()
        self.stack.push(e1//e2)
    def do_mod(self):
        e2=self.stack.pop()
        e1=self.stack.pop()
        self.stack.push(e1%e2)
    def do_compile(self):
        self.stack.push(CompiledCode(self.stack.pop()))
    def do_pop(self):
        self.stack.pop()
    def do_input(self):
        if self.stack.stack==[]:
            self.stack.push(input())
            return
        self.stack.push(input(self.stack.pop()))
    def do_flip(self):
        e1=self.stack.pop()
        e2=self.stack.pop()
        self.stack.push(e2)
        self.stack.push(e1)
    def do_antiescape(self):
        e=self.stack.pop()
        self.stack.push(e.encode().decode("unicode-escape"))
    def do_cleanmemory(self):
        del self.vars.vars
        self.vars.vars={}
        del self.stack.stack
        self.stack.stack=[]
    def do_xor(self):
        self.stack.push(self.stack.pop()^self.stack.pop())
    def do_system(self):
        import subprocess as sp
        sp.run(self.stack.pop(),shell=True)
        
def parser(code,debug):
    cmd=CommandMachine()
    linenum=1
    for line in code:
        command=line.split(" ")[0]
        if command=="" or command.startswith("//"):
            continue
        if len(line.split(" "))==1:
            cmd.allocate_command(command,linenum)
        else:
            cmd.allocate_command(command,linenum,*" ".join(line.split(" ")[1:]).split(","))
        linenum+=1
    if not debug:
        cmd.allocate_command("cleanmemory",linenum)
        return
    print("END OF OUTPUT\n\n\nDEBUG DATA")
    print("STACK:",cmd.stack.stack)
    print("VARS:",cmd.vars.vars)
    cmd.allocate_command("cleanmemory",linenum)


@click.group()
def main(): pass
@main.command()
@click.arg("file",type=click.File())
@click.option("--debug","-d","debug",is_flag=True)
@click.option("--semi","-s","semi",is_flag=True)
def run(file,debug,semi):
    if semi:
        parser(file.read().split(";"),debug)
        return
    parser(file.read().split("\n"),debug)

@main.command()
@click.arg("file",type=click.File())
def compile2py(file): pass
main()
