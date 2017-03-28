import MySQLdb
from ConfigParser import ConfigParser, NoSectionError, NoOptionError

CONFIG = {
    'DEBUG': True,
    'INSERT_KEY': ('gateway', 'game_name', 'game_id', 'lianyun_name',
	 'zone_name', 'db_name','table_name', 'strPort', 'idc_name', 
	 'target_ip'),
    'DB_LOCAL': {
	'host': '127.0.0.1',
	'port': 3306,
	'user': 'sunqi',
	'passwd': 'sunqi',
	'connect_timeout': 30,
	'charset': 'utf8'
    },
    'DB_TARGET': {
	'host': '',
        'port': 3306,
        'user': 'stat',
        'passwd': 'stat',
        'connect_timeout': 20,
        'charset': 'utf8'
    },
    'THREAD_CONF': {
	'POLL_COUNT': 50
    },
    'SQL_STR': {
	'SQL_SELECT_GAME': '''
  	    SELECT strGateway, strGameName, strProNumber, 
	           strThrTransport, strZoneName, strDbName, 
	 	   strTable, strPort
	    FROM pmdb.mm_GameZoneItem
	    WHERE quxianType = 4;
	''',
	'SQL_SELECT_ZONE': '''
	    SELECT strGatewayId, strWanip, idc_name, strProNumber
	    FROM pmdb.mm_ZoneConfigItem
	    WHERE strServiceType = 'MasterDB' and intYunFlag = 1;
	''',
	'SQL_SELECT_TARGET': '''
	    SELECT update_time, online_number FROM %s. %s;
	''',
	'SQL_INSERT': '''
	    INSERT INTO stat.stat_%s(update_time, number, 
		insert_time, strGateway, game_id, game_name, 
		zone_name, lianyun_name, idc_name)
	    VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', 
		   '%s', '%s');
	'''
    }
}

class Database(object):
    def __init__(self, d):
	self.kwargs = d
	self.conn = self.db_conn()
	self.host = self.kwargs['host']

    def db_conn(self):
	conn = MySQLdb.connect(host = self.kwargs['host'], 
	   port = self.kwargs['port'],  user = self.kwargs['user'],
	   passwd = self.kwargs['passwd'],  connect_timeout = 
	   self.kwargs['connect_timeout'], charset = 
	   self.kwargs['charset'])
	return conn
	
    def db_close(self):
	try:
    	    self.conn.close()
	except Exception, e:
  	    if e.message == 'closing a closed connection':
		pass
	    else:
	        raise e

    def exec_sql(self, sql_str, auto_commit = True, *args):
	cur = self.conn.cursor()
	cur.execute(sql_str %args)
	if auto_commit:
 	    self.conn.commit()
	    res = cur.fetchall()
	return res

    def exec_sql_dict(self, sql_str, auto_commit = True, *args):
        cur = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
	cur.execute(sql_str %args)
	if auto_commit:
	    self.conn.commit()
	    res = cur.fetchall()
	return res
    def db_commit(self):
	self.conn.commit()

class MainClass(object):
    def __init__(self):
        self.source_db = Database(CONFIG['DB_LOCAL'])

    def get_zone_list(self):
	return list(self.source_db.execute_sql(CONFIG['SQL_STR']
	    ['SQL_SELECT_ZONE]'))

    def get_game_list(self):
	return list(self.source_db.execute_sql(CONFIG['SQL_STR']
	    ['SQL_SELECT_GAME']))

    def get_task(self):
	zone_list = self.get_zone_list()
	game_list = self.get_game_list()
	if len(zone_list) > 0 and len(game_list) >0:
	    task_list = list()
	    for i in xrange(len(zone_list)-1, -1, -1):
		for j in xrange(len(game_list)-1, -1, -1):
		    if game_list[j][0] in zone_list[i][0].split(',') 
		        and game_list[j][2] == zone_list[i][3]:
			    target_ip = zone_list[i][1].split(',')[0]
			    idc_name = zone_list[i][2]
			    task_list.append(dict(zip(CONFIG
			    ['INSERT_KEY'], (game_list[j] + 
			    (idc_name, target_ip)))))
			    del game_list[j]
	    return task_list
	else:
	    LOG.error('game config incorrect.')

    def get_main(self):
	task_list = self.get_task()
	pool = ThreadPool(CONFIG['THREAD_CONF']['POLL_COUNT']
	requests = makeRequests(self.target_query, task_list, 
		exc_callback = exc_log)
	[pool.putRequest(req) for req in requests]
	pool.wait()

		
