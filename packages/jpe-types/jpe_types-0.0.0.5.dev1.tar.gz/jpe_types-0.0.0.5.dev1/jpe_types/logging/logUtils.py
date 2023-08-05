"""utils

logg utils function akka log builders and config handeling kida
"""

import logging, json, os, typing
from threading import current_thread
from datetime import datetime
#from jpe_types.paralel.thread import threadInharitanceFilter

logging_data = json.load(open(f"{os.path.dirname(os.path.realpath(__file__))}/loggingConfig.json","r"))
"config dict"

handlerDict: typing.Dict = {
    #"BaseRotatingHandler": logging.handlers.BaseRotatingHandler,
    #"RotatingFileHandler": logging.handlers.RotatingFileHandler,
    #"TimedRotatingFileHandler": logging.handlers.TimedRotatingFileHandler,
    #"WatchedFileHandler": logging.handlers.WatchedFileHandler,
    #"SocketHandler": logging.handlers.SocketHandler,
    #"DatagramHandler": logging.handlers.DatagramHandler,
    #"SysLogHandler": logging.handlers.SysLogHandler,
    #"SMTPHandler": logging.handlers.SMTPHandler,
    #"NTEventLogHandler": logging.handlers.NTEventLogHandler,
    #"HTTPHandler": logging.handlers.HTTPHandler,
    #"BufferingHandler": logging.handlers.BufferingHandler,
    #"MemoryHandler": logging.handlers.MemoryHandler,
    #"QueueHandler": logging.handlers.QueueHandler,
    
    "fileHandler": logging.FileHandler,
    "StreamHandler": logging.StreamHandler}
"handlr str to class dict"

def create_newRun(name=None):
    """create new run

        don't use this function unless you want to mess stuff up
        
        name generation in loggingConfig.json

        @param id: the number of the run

        @param %a: Sun, Mon, ...
        @param %A: Full weekday name.
        @param %w: Weekday as a decimal number.
        @param %d: Day of the month as a zero-padded decimal.
        @param %-d: Day of the month as a decimal number.
        @param %b: Abbreviated month name.
        @param %B: Full month name.
        @param %m: Month as a zero-padded decimal number.
        @param %-m: Month as a decimal number.
        @param %y: Year without century as a zero-padded decimal number.
        @param %-y: Year without century as a decimal number.
        @param %Y: Year with century as a decimal number.
        @param %H: Hour (24-hour clock) as a zero-padded decimal number.
        @param %-H: Hour (24-hour clock) as a decimal number.
        @param %I: Hour (12-hour clock) as a zero-padded decimal number.
        @param %-I:	Hour (12-hour clock) as a decimal number.
        @param %p: Locale’s AM or PM.
        @param %M: Minute as a zero-padded decimal number.
        @param %-M: Minute as a decimal number.
        @param %S: Second as a zero-padded decimal number.
        @param %-S: Second as a decimal number.
        @param %f: Microsecond as a decimal number, zero-padded on the left.
        @param %z: UTC offset in the form +HHMM or -HHMM.
        @param %Z: Time zone name.
        @param %j: Day of the year as a zero-padded decimal number.
        @param %-j: Day of the year as a decimal number.
        @param %U: Week number of the year (Sunday as the first day of the week). All days in a new year preceding the first Sunday are considered to be in week 0.
        @param %W: Week number of the year (Monday as the first day of the week). All days in a new year preceding the first Monday are considered to be in week 0.
        @param %c: Locale’s appropriate date and time representation.
        @param %x: Locale’s appropriate date representation.
        @param %X: Locale’s appropriate time representation.
        @param %%: A literal '%' character.
    
        see https://www.programiz.com/python-programming/datetime/strftime for extra detailt on datetimeing"""
    if name is None:
        name = str(logging_data["logDirName"])

    zeros = logging_data["logZeroFill"]

    def getCustomName(name):
        """build the name of the log

            @param name: the name passed to create_run
            """
        timeStamp = datetime.now()
        name = timeStamp.strftime(name)
        nname = name.format(id=run_number)
        return nname

    getPath = lambda run_number: f"./log/{getCustomName(name)}" if run_number==0 else f"./log/{getCustomName(name) + str(run_number)}"
    
    if not os.path.isdir("./log"):
        os.makedirs("./log")

    run_number = 0
    path = getPath(run_number)
    while os.path.isdir(path):
        run_number += 1
        path = getPath(run_number)
    
    os.makedirs(path)

    return path +"/"

runFile = None
"the file to runn to"


def Create_defaultLogger(name:str = current_thread().name, logType:str="stdLogger")  ->  typing.NewType("logger", logging.Logger):
    """create std logger
    
    create std logger as specified by loggingConfig.json so edit that to change it

    @param name: the name of the logger
    @type name: str

    @param logType: the type of a logger as set by loggingConfig
    @type logType: str
    """
    if runFile is None:
        raise LogSetupError()

    FORMAT = logging_data[logType]["Format"]

    log = logging.getLogger(name)

    handler = handlerDict[logging_data[logType]["handler"]]
    syslog = handler(f"{runFile}{name}.log")

    #log.addFilter(threadInharitanceFilter())

    formatter = logging.Formatter(FORMAT)
    syslog.setFormatter(formatter)
    
    log.setLevel(logging_data[logType]["logLevel"])
    log.addHandler(syslog)

    log.setLevel(logging_data[logType]["logLevel"])
    for msg in logging_data[logType]["startupConfig"]:
        log.info(msg)

    return log


class LogSetupError(Exception):
    "Exception raised when logging wasnt setup befor calls"
    def __init__(self, *args, **kwargs):
        "the error raised when a log setup failes"
        Exception.__init__(self, f"logging must be initiated but want run jpe_types.logging.setup() before using loggers", **kwargs)
