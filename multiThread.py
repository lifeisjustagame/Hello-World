class ThreadPool:
	def __init__(self, num_workers, q_size = 0, 
		    resq_size = 0, poll_timeout = 5):
		self._requests_queue = Queue.Queue(q_size)
		self._results_queue = Queue.Queue(resq_size)
		self.workers = []
		self.dismissedWorkers = []
		self.workRequests = {}
		self.createWorkers(num_workers, poll_timeout)

	def createWorkers(self, num_workers, poll_timeout = 5):
		for i in range(num_workers):
			self.workers.append(WorkerThread(
			self._requests_queue, self._results_queue, 
			poll_timeout = poll_timeout))

	def dismissWorkers(self, num_workers, do_join = False):
		dismiss_list = []
		for i in range(min(num_workers, len(self.workers))):
			worker = self.workers.pop()
			worker.dismiss()
			dismiss_list.append(worker)

		if do_join:
			for worker in dismiss_list:
				worker.join()
		else:
			self.dismissedWorkers.extend(dismiss_list)
	
	def joinAllDismissedWorkers(self):
		"""Perform Thread.join() on all woker threads that have been dismidded."""
		for worker in self.dismissedWorkers:
			worker.join()
		self.dismissedWorkers = []

	def putRequest(self, request, block = True, timeout = None):
		assert isinstance(request, WorkRequest)
		assert not getattr(request, 'exception', None)
		self._requests_queue.put(request, block, timeout)
		self.workRequests[request.requestID] = request

	def poll(self, block = False):
		while True:
			if not self.workRequests:
				raise NoResultsPending
			elif block and not self.workers:
				raise NoWorkersAvailable
			try:
				request, result = self._results_queue.get(block = block)
				if request.exception and request.exc_callback:
					request.exc_callback(request, result)
				if request.callback and not (request.exception and request.exc_callback):
					request.callback(request, result)
				del self.workRequests[request.requestID]
			except Queue.Empty:
				break

	def wait(self):
		"""Wait for resuls, blocking until all have arrived."""
		while 1:
			try:
				self.poll(True)
			except NoResultsPending:
				break

