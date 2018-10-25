######################################
Error Logger
######################################

LAtools GUI makes use of an error logging framework to handle errors and log their data for later analysis. This
is particularly useful for remote user testing when developers don't have access to the test computer. Error logs
can be exported at any stage from the file tab in the toolbar, or from the export stage, or can be accessed
manually under "latools_gui/latools_gui/logs".


Using the Error Logger
=============================

There exists comprehensive documentation for Python's logging module online, but presented below is a
context specific guide for the implementation of logging in LAtools GUI.

**Defining it within your project:**

In order to begin, the error logger needs to be defined in you highest level file, which in our case is “latoolsgui.py”.
All files using the logger output must import Python's native logging library::

    import logging

Your top-level file must also import the logging configuration module::

    import logging.config

We must now define the logger's configuration. While it is recommended to use its support for an external configuration file, due to the request for the standalone package causing complications it instead uses an internal dictionary in-code.

The following is an example of a logging dictionary-based configuration::

	# Define logger configuration
	logger = logging.getLogger(__name__)
	logging.config.dictConfig({
		'version': 1,
		'formatters': {
			'stdFormatter': {
				'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
			},
		},
		'handlers': { 'errhandler': {
				'level': 'ERROR',
				'class': 'logging.FileHandler',
				'formatter': 'stdFormatter',
				'filename': errorFile
			},
		},
		'loggers': {
			'': {
				'handlers': ['errhandler'],
				'level': 'DEBUG',
				'propagate': True
			},
		},
	})

Here, there are three major sections of import. The first are the formatters. A formatter defines the format of a logger's output, in this case a hyphen-separated sequence of a timestamp, broadcasting logger's internal name (In this case identical to the module name, see below), trap level, and output message.

The second component is the handlers. The example handler has a minimum output trap level of "ERROR" (in which case it will only catch ERROR-level logging messages), is the handler class FileHandler (Appends logs to a file), is linked to use the example formatter, and outputs to a file pointed to whatever path is stored by errorFile.

The last component are loggers, which are linked to a list of one or more handlers, have their own minimum output trap level, and may be configured to propagate their messages upstream (Keep this as true.)

To output to a log, a module should first initialise a logger instance using::

	self.logger = logging.getLogger(__name__)

creating the logger "self.logger" with an internal name set to the module name, at which point it may output messages with the function::

	self.logger.$LEVEL("$MESSAGE")

at level specified by $LEVEL and some message. It should be noted that with the example settings above, log outputs below the ERROR level will not be caught, and $MESSAGE should not be left blank.
Deserving particular attention is the level "EXCEPTION". It is functionally identical to ERROR, however, it will also output a trace after the message - Thus, all exception logs should end with one call to self.logger.exception().
What needs to be implemented into each line that is being error checked, within an “except” from a try statement follows this syntax::

    self.logger.error('(Brief description string): [Loaction]:{}\n[Config]:{}\n[Extension]:{}\n'
						 '[srm_Identifier]:{}\n'.format( self.fileLocationLine.text(),
										self.configOption.currentText(),
										self.file_extensionOption.text(),
										self.srm_identifierOption.text()))

