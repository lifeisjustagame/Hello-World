














if __name__ == '__main__':
	start = time.time()
	LOG.warning('PROGRAM START AT: %s' % TIME)

	try:	
		mc = MainClass()
		mc.task_main()
	except Exception, e:
		LOG.error(e)
		raise
	except (SystemExit, keyboardInterrupt), e:
		error_str = 'Program killed by user, reason: %s' %e
		LOG.error(error_str)
		sys.exit()
	finally:
		end = 'use: %s' % (time.time() - start)
		LOG.info(end)

