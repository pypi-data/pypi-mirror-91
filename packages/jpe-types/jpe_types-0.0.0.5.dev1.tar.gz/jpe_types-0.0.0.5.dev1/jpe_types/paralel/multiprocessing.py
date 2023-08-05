"""multiprocessing enchanments

adds Processes that return values as well as Process safe printing

"""

from multiprocessing.queues import Queue as mpQueue
from multiprocessing import Process as mpProcess, Pipe as mpPipe, Manager as mpManager, get_context as mpGet_context, current_process
from multiprocessing.connection import Connection as mpConnection
from multiprocessing.context import BaseContext as mpBaseContext, _default_context
from multiprocessing.managers import SyncManager as mpSyncManager, Namespace as mpNamespace, NamespaceProxy as mpNamespaceProxy, BaseProxy as mpBaseProxy
from threading import Thread
from traceback import format_exc
import typing

__all__ = ["printer", "Process", "getMpOutputFunction", "PoolWorker", 
"PoolWorker", "context", "patches", "activate_patch", "deactivate_patch"]


class printer():
    """printStatment class that can be used in all processes
    """
    class printer_queue(mpQueue):
        "the que to put all requests in"
        def __call__(self, *args, printName=True, block=True, **kwargs):
            "add data to print queue"
            if block:
                recver, sender = mpPipe(False)
            else:
                recver, sender = None, None
            args = (current_process().name, *args) if printName else args
            try:
                self.put_nowait((args, kwargs, sender))
                if block:
                    data = recver.recv()
                    recver.close()
                    return data
            except: 
                print("error")

    _active = False
    "weather or not the printer is active"
    def __init__(self, exe_function=print, ctx=_default_context.get_context()):
        """constructor
        
        see https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queues"""
        self._internal_queue = printer.printer_queue(ctx=ctx)
        "the queue to write data to"
        self._printFunc = exe_function
        "the function used to print"
        self.start()

    def stop(self):
        "stop listening for things to print"
        self._active = False

    def start(self):
        "start listening for things to print"
        if self._active:
            return
        self._active=True
        "the function used to wait for print statments"
        self._printer = Thread(target=self._print,
                                daemon=True,
                                name="jpe_types.mp.intern.printer")
        "the thread that will print the data"
        self._printer.start() 
    
    def _print(self):
        """the function that is used to print"""
        while self._active:
            try:
                args, kwargs, sender = self._internal_queue.get(False)
                data = self._printFunc(*args, **kwargs)
                if not sender is None:
                    sender.send(data)
            except:
                pass
    
    def close(self):
        """nothing more to print

            Indicate that no more data will be printed by the current process. The background thread will quit once it has flushed all buffered data to the pipe. This is called automatically when the queue is garbage collected.
        """
        self._internal_queue.close()
Print = printer()._internal_queue
"""print function

    the function to print in witch will add everything to a queue witch is then read by a thread of the printer\n
    in other Processes it will be set to the builtin function print
    """
__builtins__["mp_print"] = Print

def input_mp(*args):
    "input function compatible with printer"
    Print(*args, end="", printName=False)
    data = input()
    return data
Input = printer(exe_function=input_mp)._internal_queue
"""input function

    multiprocessing copatible input function in other processes pawned by jpe_types.paralel.mp.Process it will be the builtin input
    """
__builtins__["mp_input"] = Input

def getMpOutputFunction(func, ctx=_default_context.get_context()):
    """create a printfunction system

        create a output file writer can be used for logging. the idear is that no 2 values ever overlap"""
    
    return printer(func, ctx=ctx)._internal_queue



class Process(mpProcess):
    """Process objects represent activity that is run in a separate process. The Process class has equivalents of all the methods of threading.Thread.

        The constructor should always be called with keyword arguments. group should always be None; it exists solely for compatibility with threading.Thread. target is the callable object to be invoked by the run() method. It defaults to None, meaning nothing is called. name is the process name (see name for more details). args is the argument tuple for the target invocation. kwargs is a dictionary of keyword arguments for the target invocation. If provided, the keyword-only daemon argument sets the process daemon flag to True or False. If None (the default), this flag will be inherited from the creating process.

        By default, no arguments are passed to target.

        If a subclass overrides the constructor, it must make sure it invokes the base class constructor (Process.__init__()) before doing anything else to the process."""
    def __init__(self, group=None, target=None, name: str=None, args: tuple=(), kwargs: typing.Dict[str, typing.Any]={}, *, daemon: bool=False, doOutput: bool=False):
        """constructor

            @param groop: None:
            @param target: the function to be called
            @type target: callable
            @param name: the name of the 
            @type name: str
            @param args: the arguments of the function
            @type args: tupple
            @param kwargs: the keyword arguments of the function
            @type kwargs: dict
            @param deamon: if the Process is a deamon Process
            @type deamon: bool"""
        if not hasattr(target, "__call__") or target is None: raise TypeError(f"target must be callable or None not {type(target)}")
        if not type(name) or name is None is str: raise TypeError(f"param name must be str not {type(name)}")
        if not type(args) is tuple: raise TypeError(f"param args must be tuple not {type(args)}")
        if not type(kwargs) is dict: raise TypeError(f"param kwargs must be dict not {type(kwargs)}")
        if not type(daemon) is bool or daemon is None: raise TypeError(f"param deamon must be bool not {type(daemon)}")
        if not type(doOutput) is bool: raise TypeError(f"param doOutput must be bool not {type(doOutput)}")

        self.dataRecever, dataSender = mpPipe(duplex=False) if doOutput else (None, None)
        "conector to get the data from return"

        mpProcess.__init__(self, group=group, target=target, name=name, args=((mp_print, mp_input), dataSender, *args), kwargs=kwargs, daemon=daemon)


    def run(self, *a, **k):
        """internal run function

            run the function and save the return val
            the execute function replaces what is by run in std implementation"""
        self.print, self.input = self._args[0]
        "the print statmen set to defauts"
        dataSender: mpConnection = self._args[1]
        __builtins__["print"] = self.print
        __builtins__["mp_print"] = self.print

        __builtins__["input"] = self.input
        __builtins__["mp_input"] = self.input
        try:
            #this schould be rewriten
            _output_val = self.execute(*self._args[2:], **self._kwargs)
            if not dataSender is None:
                dataSender.send(_output_val)
            return _output_val
        except:
            self.print(f"{format_exc()}in Process {self._name}")
    
    def execute(self, *args, **kwargs):
        """Method to be run in sub-process; can be overridden in sub-class"""
        if self._target:
            return self._target(*args, **kwargs)
    
    def join(self, timeout=None):
        """join Process
        
            If the optional argument timeout is None (the default), the method blocks until the process whose join() method is called terminates. If timeout is a positive number, it blocks at most timeout seconds. Note that the method returns None if its process terminates or if the method times out. Check the process’s exitcode to determine if it terminated.
            A process can be joined many times.
            A process cannot join itself because this would cause a deadlock. It is an error to attempt to join a process before it has been started."""

        mpProcess.join(self, timeout=timeout)
        data = None
        if not self.dataRecever is None:
            data = self.dataRecever.recv()
            self.dataRecever.close()
        return data

base_ctx = mpGet_context()
"the default context as defined by mp.Get_context()"
class PoolWorker(base_ctx.Process, Process):
    """the worker Process for Pool 

        its identical to Process
        """
    def __init__(self, *args, **kwargs):
        super(base_ctx.Process, self).__init__(*args, **kwargs)

class context(mpBaseContext):
    "just a placeholder"

class patches:
    """a class containing refrences to all patches

        patches are changes made to librarys
        """
    def __init__(self, *args, **kwargs):
        "make sure class is not initiated"
        raise RuntimeError("class patches must not be initiated")

    ProcessPatch = 0
    """use better Process as std

        changes the contexts Process to jpe_types.paralel.mp.Process
        """

def activate_patch(*patches, ctx=mpGet_context()):
    """activate the patches passed

        @param patches: the pathes to be activated
        @param ctx: the contex to do it on
        """
    def processPatch():
        base_ctx.mp_Process = base_ctx.Process
        base_ctx.Process = PoolWorker
    
    funcs = [processPatch]

    for patch in patches:
        funcs[patch]()

def deactivate_patch(*patches, ctx=mpGet_context()):
    """deactivate the patches passed

        @param patches: the pathes to be activated
        @param ctx: the contex to do it on
        """
    def processPatch():
        if not hasattr(base_ctx, "mp_Process"):
            raise RuntimeError(f"process patch has not bean activated but deactivated")
        base_ctx.Process = base_ctx.mp_Process
    
    funcs = [processPatch]

    for patch in patches:
        funcs[patch]()
