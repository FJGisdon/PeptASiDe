#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By    : FJG
# Creation Date : 07/12/2022
version ='1.0.0'
# ---------------------------------------------------------------------------
"""
Setup and configure the logger.
"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import logging
import sys

# ---------------------------------------------------------------------------
# Classes
# ---------------------------------------------------------------------------

class customLogger:
    """
    A class to configure a custom logger.

    Attributes
    ----------
    output : str, string providing the path for the output file;
                    default: sys.stdout

    Methods
    -------
    log():
            Custom log function to either use use the built-in functionality of logging
            or to print results to the desired location.
    log_level():
            Set the log level, silent, verbose, debug.
    """

    def __init__(self, logger_name: str):
        """

        Initialization of the custom logger

        param: logger_name: str, the name of the logger, which is printing the message.
                Commonly __main__ of the respective file is used.

        """

        # Set logger for current file
        self.logger = logging.getLogger(logger_name)


    def set_up_logger(self, output: str = sys.stdout, loglevel: str = 'silent'):
        """

        Set up the custom logger

        :param output: str, the desired location for the results to write
                default: sys.stdout
        :param loglevel: str, the log level, which should be used:
                                silent: only print results and error messages to output
                                warning: print everything upt to warnings to output
                                verbose: print status messages in addition to output
                                debug: print everything to output
                default: 'silent'
        
        """


        self.output: str = output
        self.set_loglevel(loglevel)

        # Setup logging
        logging.basicConfig()#format = "[%(levelname)s] %(message)s")

    

    def log(self, message: str, level: str = ""):
        """

        Print either log messages or results. This is useful for pipelining

        param: message: str, string containing the message to be printed
        param: level: str, the log level, which should be used, by default
                empty string, which prints to the desired output location
                default: ""

        """

        if (level == "c"):
            self.logger.critical(message)
        elif (level == "e"):
            self.logger.error(message)
        elif (level == "w"):
            self.logger.warning(message)
        elif (level == "i"):
            self.logger.info(message)
        elif (level == "d"):
            self.logger.debug(message)
        else:
            self.output.write(message + "\n")

    

    def set_loglevel(self, loglevel: str):
        """

        Set the log level for the prints.

        param: loglevel: str, the log level, which should be used

        """

        if loglevel == 'verbose':
            self.logger.setLevel(logging.INFO)
        elif loglevel == 'debug':
            self.logger.setLevel(logging.DEBUG)
        elif loglevel == 'warning':
            self.logger.setLevel(logging.WARNING)
        else:
            self.logger.setLevel(logging.ERROR)


