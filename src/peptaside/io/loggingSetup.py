#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By    : FJG
# Creation Date : 07/12/2022
version ='1.1.0'
# ---------------------------------------------------------------------------
"""
Setup and configure the logger.
Create an instance in the main application, the logger will be set up with 
default settings then and can be customized by its functions. In all other 
files of the project only an instance instance is created, the settings can
be adjusted by the user and are valid for all instances. Logging in module 
files works even when no instance in the main application is created. The
name of the logger will always adapted to the name of the respective file.
"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import logging
import sys

# ---------------------------------------------------------------------------
# Classes
# ---------------------------------------------------------------------------

class customLogger():
    """
    A class to configure a custom logger.

    Attributes
    ----------
    logOutput : str, string providing the path for the output file;
                    default: sys.stdout

    Methods
    -------
    log():
            Custom log function to either use use the built-in functionality of logging
            or to print results to the desired location.
    setUpLogger():
            Set up logger.
    setLogLevel():
            Set the log level, silent, verbose, debug.
    """

    _logger = logging.getLogger()
    _logOutput: str = sys.stdout
    _loglevel: str = None
    _initialized: bool = False


    def __init__(self, logger_name: str = __name__):
        """

        Initialization of the custom logger

        param: logger_name: str, the name of the logger, which is printing the message.
                Commonly __main__ of the respective file is used.

        """
        
        # Initialize the logger and basic settings
        self.logger = logging.getLogger(logger_name)

        # For the first time an instance of this class in a program run is created,
        # initialization with default parameters is performed
        if not self.__class__._initialized:
            self.__class__._defaultInitialize()


    @classmethod
    def _defaultInitialize(cls):
        """
        Default initialization of class attributes. Only performs once for a program run.
        """

        # Stream initial output to screen
        cls._logOutput = sys.stdout
        cls.setUpLogger()
        # Setup logging
        logging.basicConfig(format = "[%(levelname)s] %(name)s - %(message)s")
        # Set initialization to True
        cls._initialized = True


    @classmethod
    def _setLogLevel(cls, loglevel: str = "silent"):
        """

        Set the log level for the prints. Here the class variable logger is
        modified to adjust the logging level for all instances.

        param: loglevel: str, the log level, which should be used
                default: logging.ERROR

        """

        if loglevel == 'verbose':
            cls._logger.setLevel(logging.INFO)
        elif loglevel == 'debug':
            cls._logger.setLevel(logging.DEBUG)
        elif loglevel == 'warning':
            cls._logger.setLevel(logging.WARNING)
        elif loglevel == 'silent':
            cls._logger.setLevel(logging.ERROR)
        else:
            pass
   

    @classmethod
    def setUpLogger(cls, usrOutput: str = None, loglevel: str = None, formatString: str = None):
        """

        Set up the custom logger

        :param output: str, the desired location for the results to write
                default: sys.stdout
        :param loglevel: str, the log level, which should be used:
                                silent: only print results and error messages to output
                                warning: print everything up to warnings to output
                                verbose: print status messages in addition to output
                                debug: print everything to output
        
        """

        if usrOutput is not None:
            cls._logOutput: str = usrOutput
        if loglevel is not None:
            cls._setLogLevel(loglevel)
        if formatString is not None:
            logging.basicConfig(format = formatString)


    def log(self, message: str, level: str = None):
        """

        Print either log messages or results. This is useful for pipelines.
        This function uses the respective instances, which are created in 
        the individual files or classes. In this setup the filename of the
        file is listed from which the message is printed.

        param: message: str, string containing the message to be printed
        param: level: str, the log level, which should be used
                which prints to the desired output location
                default: None, prints to the user-defined location, should be 
                                used for results.

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
            self.__class__._logOutput.write(message + "\n")

# ---------------------------------------------------------------------------
