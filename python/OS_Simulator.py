from Task import Task
from Task import Job
import datetime
import random
from multiprocessing import Process, Pipe, Queue
import signal
import os
import time
import math
import sys
class OS_Simulator:
	TIME_SLICE_LEN = 10 #each time slice is 10 ms
	MAX_WCET=100 #WCET ranges from 10 ms to 1000 ms
	def __init__(self, task_list):
		'''

		Args:
			task_list:		type: Task[]; The array of tasks running
			#start_time: 	type: datetime; The booting time of the OS_simulator


		'''

		#generate the task set here based on the load

		self.task_list = task_list
		self.total_tasks = len(self.task_list)

		#for t in self.task_list:
		#	print(t.task_info())
		#set the start_time here
		
		#construct a pipe here and save the pipe ends in the job_pipe
		#self.job_pipe_read, self.job_pipe_send = Pipe(duplex=False)
		#self.info_pipe_read, self.info_pipe_send = Pipe(duplex=False)

		#start the non-stop process that generate jobs

		#p = Process(target=self.generate_jobs, args=(self.start_time,))
		#p.start()




	

	def generate_jobs(self, start_time, job_send, core_rank):
		#f = open("log/job_generation.log", "a")
		#old = sys.stdout
		#sys.stdout = f
		self.job_pipe_send = job_send
		#print(self.job_pipe_send)
		r = os.popen("taskset -p -c " +str(core_rank)+" "+str(os.getpid()))
		#print(r.read())
		arrived_task_list = []
		phases = []#use the phases array to record which job of the task is to come next
		counter = 0
		all_arrived = False
		while True:
			time_now = datetime.datetime.now()
			interval = (time_now - start_time).total_seconds()*1000

			#add newly arrived tasks

			if not all_arrived:
				arr_time_now = start_time+datetime.timedelta(milliseconds = self.task_list[counter].arr_time)
				#print(arr_time_now)
				#print(self.start_time)
				while arr_time_now<=time_now:#(time_now - self.task_list[counter].arr_time).total_second()>=0
					#print("A task has arrived")
					#print(counter)
					arrived_task_list.append(self.task_list[counter])
					counter += 1
					phases.append(0)
					if counter>= len(self.task_list):
						all_arrived = True
						#print("All tasks' first instances have arrived.")
						break
					#f.flush()
					arr_time_now = start_time+datetime.timedelta(self.task_list[counter].arr_time)


			#maintain tasks that already arrived
			for i in range(len(arrived_task_list)):
				if interval>= arrived_task_list[i].arr_time + phases[i]*arrived_task_list[i].period:
					if arrived_task_list[i].is_periodic == False:
						dice = random.random.ranind(0,5)#only 20% of sporadic arrives at the first minimal interval
						if dice > 0:
							break
					arb_ddl = time_now+datetime.timedelta(milliseconds=arrived_task_list[i].ddl)
					phases[i]+= 1
					j = Job(arrived_task_list[i].WCET, arb_ddl, arrived_task_list[i].task_id)
					#send it through the pipe
					#print("Trying to send through pipes")
					self.job_pipe_send.put(j)#change the pipe sender to queue
					#os.system("ps -o pid,psr,comm -p "+str(os.getpid()))


'''
#code for the test of OS_Simulator: test passed!
core_count = 0
a = OS_Simulator(10)
#job_pipe_read, job_pipe_send = Pipe(duplex=False)
#info_pipe_read, info_pipe_send = Pipe(duplex=False)
job_q = Queue()
#info_q = Queue.Queue(0) #leave the info analysis to Scheduler.py

start_time = datetime.datetime.now() 

p = Process(target=a.generate_jobs, args=(start_time, job_q, core_count))
p.start()
core_count += 1
job_receiver= job_q
while True:
	#time.sleep(5)
	while not job_q.empty():
		job_now = job_receiver.get()
		print(job_now.job_info())
'''
