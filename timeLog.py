import logging
import time
import datetime
import os
import sys

def split_file_name():
	file_dir, file_name = os.path.split(os.path.abspath(sys.argv[0]))
	if file_name.endswith('.py'):
		file_name = file_name.replace('.py', '')
	return file_dir, file_name

LOG_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "log"))

def init_log():
	split_file = split_file_name()
	current_date = TIME.strftime("%Y_%m_%d")
	log_file_name = '%s_%s.log' % (split_file[1], current_date)
	log_file = os.path.normpath(os.path.join(LOG_DIR, log_file_name))
	if not os.path.exists(LOG_DIR):
		os.mkdir(LOG_DIR)
	logging.basicConfig(
		level = logging.INFO,
		format = '%(asctime)-15s %(levelname)s %(message)s',
		filename = log_file,
		filemode = 'a',
	)
	return logging.getLogger()

TIME = datetime.datetime.now().replace(second = 0)
START_TIME = int(time.mktime(TIME.timetuple()))

LOG = init_log()

if __name__ == '__main__':
	start = time.time()
	print('TIME is: ', TIME)
	LOG.warning('PROGRAM START AT: 2017032312:34')
	time.sleep(10)
	LOG.error('Error string test')
	end = 'use: %s' % (time.time() - start)
	LOG.info(end)
