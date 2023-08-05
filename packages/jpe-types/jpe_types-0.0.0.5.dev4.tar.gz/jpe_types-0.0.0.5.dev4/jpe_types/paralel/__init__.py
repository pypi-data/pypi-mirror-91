"""additons to paralel computation

additional and slitly imporved thread
Pricesses with retuns"""

__all__ = ["Thread", "LockableThread", "threadInharitanceFilter", "LogThread", "print", "Process", "Process", "getMpOutputFunction", "mp", "thread"]
from jpe_types.warnings.warnings import depricateFunction

from jpe_types.paralel.thread import Thread, LockableThread, threadInharitanceFilter, LogThread
from jpe_types.paralel.multiprocessing import Print as print, Process, getMpOutputFunction#, classSharer

Thread, LockableThread, threadInharitanceFilter, LogThread = depricateFunction(Thread), depricateFunction(LockableThread), depricateFunction(threadInharitanceFilter), depricateFunction(LogThread)
print, Process, getMpOutputFunction = depricateFunction(print), depricateFunction(Process), depricateFunction(getMpOutputFunction)

from jpe_types.paralel import multiprocessing as mp
from jpe_types.paralel import thread as thread

#__all__ = ["Thread", "LockableThread", "threadInharitanceFilter"]