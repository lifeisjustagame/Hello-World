import threading
import multiprocessing
import os
import sys

class WorkerThread(threading.Thread):
    def __init__(self, requests_queue, results_queue, poll_timeout = 5, **keds):
	threading.Thread.__init__(self, **kwds)
	self.setDaemon(1)
	self._requests_queue = requests_queue
	self._results_queue = results_queue
	self._poll_timeout = poll_timeout
	self._dismissed = threading.Event()
	self.start()

    def run(self):
	"""Repeatedly process the job queue until told to exit."""
	while True:
	    if self._dismissed.isSet():
		break
	    try:
		request = self._requests_queue.get(True, self._poll_timeout)
	    except Queue.Empty:
		continue
	    else:
		if self._dismissed.isSet():
		    self._requests_queue.put(request)
		    break
		try:
		    result = request.callable(*request.args, **request.kwds)
		    self._results_queue.put((request, result))
		except:
		    request.exception = True
		    self._results_queue.put((request, sys.exc_info()))

    def dismiss(self):
	"""Sets a flag to tell the thread to exit when done with current job."""
	self._dismissed.set()

class WorkRequest:
    def __init__(self, callable_, args = None, kwds = None, requestID = None, callback = None,
	        exc_callback = _handle_thread_exception):
	if requestID is None:
	    self.requestID = id(self)
	else:
	    try:
		self.requestID = hash(requestID)
	    except TypeError:
		raise TypeError("requestID must be hashable.")
	self.exception = False
	self.callback = callback
	self.exc_callback = exc_callback
	self.callable = callable_
	self.args = args or []
	self.kwds = kwds or {}

    def __str__(self):
	return "<WorkRequest id = %s args = %r kwargs = %r exception = %s>" %
		(self.requestID, self.args, self.kwds, self.exception) 
