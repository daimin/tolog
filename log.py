import conf
import logging
import datetime

logger = None

def getlogger(logfile = None):
    global logger
    if logger == None:
        logger = logging.getLogger()
        if logfile == None: 
            logfile = conf.log_dir + '/' + datetime.datetime.now().strftime("%Y%m%d") + ".log"
        else:
            logfile = conf.log_dir + '/' + logfile
        
        hdlr = logging.FileHandler(logfile)
        formatter = logging.Formatter('%(asctime)s %(module)s : %(lineno)d : %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        hdlr.setLevel(logging.DEBUG)
        logger.addHandler(hdlr)
        
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        ch.setLevel(logging.DEBUG)
        logger.addHandler(ch)
        
        logger.setLevel(logging.NOTSET)
       
        logger.info("initialize logger")
    
    return logger
