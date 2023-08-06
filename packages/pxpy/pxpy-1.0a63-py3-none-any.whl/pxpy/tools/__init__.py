from tqdm import tqdm
import numpy as np
from enum import IntEnum
import os
import csv
import time
import json

from multiprocessing import Process, Queue

Q = Queue()

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

lbar		= None
server		= None

file_log	= None

norm_log	= []
wnorm_log	= []
obj_log		= []
time_log	= []
start_time	= None
state		= None

STATUS_PORT = 10000
if os.environ.get('PX_STATUS_PORT') is not None:
	STATUS_PORT = int(os.environ['PX_STATUS_PORT'])

class WSStatus(WebSocket):

	def handleMessage(self):
	
		elapsed  = Q.get()
		cur_iter = Q.get()
		max_iter = Q.get()
		best_nrm = Q.get()
		best_obj = Q.get()
		best_wnrm= Q.get()

		s = str(elapsed) + '\t' + str(cur_iter) + '\t' + str(best_obj) + '\t' + str(best_nrm) + '\t' + str(best_wnrm)
		
		self.sendMessage(s)

	def handleConnected(self):
		print(self.address, 'connected')

	def handleClose(self):
		print(self.address, 'closed')

def __wsrun(port,start_time,state,norm_log,wnorm_log,obj_log,time_log):
	global server
	server = SimpleWebSocketServer('', port, WSStatus)
	server.serveforever()

STATUS_PROVIDER_PROCESS = None
	
class OptimizerHookType(IntEnum):
	quite = 0
	quite_logfile = 1
	plain = 2
	plain_logfile = 3
	tqdm = 4
	tqdm_logfile = 5

def __optimizer_hook(state_p,hooktype):
	global lbar
	
	global file_log
	
	global norm_log
	global wnorm_log
	global obj_log
	global time_log
	global start_time
	global state
	
	global server

	state = state_p.contents
	
	if start_time is None:
		start_time = time.time()
	
	global STATUS_PROVIDER_PROCESS
	
	if os.environ.get('PX_STATUS_PROVIDER') is not None and STATUS_PROVIDER_PROCESS is None:
		STATUS_PROVIDER_PROCESS = Process(target=__wsrun, args=(STATUS_PORT,start_time,state,norm_log,wnorm_log,obj_log,time_log))
		STATUS_PROVIDER_PROCESS.start()

	if hooktype > 3 and lbar is None:
		lbar = tqdm(total=state.max_iterations)

	if hooktype % 2 == 1 and file_log is None:
		file_log = open('px_'+str(int(start_time))+'.log','w')

	wnrm = np.linalg.norm(state.best_weights)
	
	norm_log.append(state.best_norm)
	wnorm_log.append(wnrm)
	obj_log.append(state.best_obj)
	
	now = time.time()
	time_log.append(now)

	if STATUS_PROVIDER_PROCESS is not None:
		Q.put(now-start_time)	
		Q.put(state.iteration)
		Q.put(state.max_iterations)
		Q.put(state.best_norm)
		Q.put(state.best_obj)
		Q.put(wnrm)

	log_str = "{:.4f}".format(now-start_time) + '\t' + str(state.iteration) + '\t' + str(state.best_obj) + '\t' + str(state.best_norm) + '\t' + str(wnrm)
	
	if hooktype == 2 or hooktype == 3:
		print(log_str)
		
	if hooktype % 2 == 1:
		file_log.write(log_str+'\n')
		
	if hooktype == 4 or hooktype == 5:
		lbar.set_description( "OPT;" + "{:.4f};{:.4f}".format(nrm,val) )
		lbar.update(1)

	if state.iteration == state.max_iterations:
		if hooktype % 2 == 1:
			file_log.close()

		if hooktype > 3:
			lbar.close()
			lbar = None
			
		file_log = None
		start_time = None
		norm_log.clear()
		wnorm_log.clear()
		obj_log.clear()
		
		if STATUS_PROVIDER_PROCESS is not None:
			STATUS_PROVIDER_PROCESS.terminate()

def opt_progress_hook_quite(state_p):
	__optimizer_hook(state_p,OptimizerHookType.quite)
	
def opt_progress_hook_quite_logfile(state_p):
	__optimizer_hook(state_p,OptimizerHookType.quite_logfile)
	
def opt_progress_hook_plain(state_p):
	__optimizer_hook(state_p,OptimizerHookType.plain)
	
def opt_progress_hook_plain_logfile(state_p):
	__optimizer_hook(state_p,OptimizerHookType.plain_logfile)
	
def opt_progress_hook_tqdm(state_p):
	__optimizer_hook(state_p,OptimizerHookType.tqdm)
	
def opt_progress_hook_tqdm_logfile(state_p):
	__optimizer_hook(state_p,OptimizerHookType.tqdm_logfile)

def opt_progress_hook(state_p):
	__optimizer_hook(state_p,OptimizerHookType.tqdm)

def generic_progress_hook(_cur,_tot,_nam):
	if type(_nam) is not str:
		_nam = _nam.decode('utf-8')

	global lbar

	if lbar is None:
		lbar = tqdm(total=_tot, desc=_nam, position=0, leave=True)

	lbar.update(_cur - lbar.n)
	lbar.set_description(_nam)

	if _cur == _tot:
		lbar.close()
		lbar = None
	
def genfromstrcsv(filename, targets=None, has_header=True):
	N = 0
	n = None
	values = None

	csv_data = open(filename)
	csv_reader = csv.reader(csv_data)
	header = next(csv_reader)
	n = len(header)

	if targets is None:
		targets = range(n)
	values = dict()

	if not has_header:
		N = N+1
		for i in targets:
			if i not in values.keys():
				values[i] = set()
			values[i].add(header[i])

	for row in csv_reader:
		N = N+1
		for i in targets:
			if i not in values.keys():
				values[i] = set()
			values[i].add(row[i])

	vmaps  = dict()
	rvmaps = dict()

	for i in targets:
		j = 0

		if i not in vmaps.keys():
			vmaps[i] = dict()
			rvmaps[i] = dict()

		for v in values[i]:
			vmaps[i][v] = j
			rvmaps[i][j] = v

			j = j+1

	result = np.zeros((N,len(targets)), dtype=np.uint16)


	csv_data.seek(0)

	csv_reader = csv.reader(csv_data)
	header = next(csv_reader)

	if targets is None:
		targets = range(n)

	I = 0
	if not has_header:
		J = 0
		for i in targets:
			result[I,J] = vmaps[i][header[i]]
			J = J + 1
		I = 1

	for row in csv_reader:
		J = 0
		for i in targets:
			result[I,J] = vmaps[i][row[i]]
			J = J + 1
		I = I + 1

	return result, rvmaps

