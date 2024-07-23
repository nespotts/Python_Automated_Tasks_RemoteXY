import threading
import time
val1 = 0
val2 = 0
 
class th1:
	def __init__(self):
		self.val1 = 0
 
	def run(self):
		while 1:
			self.val1 += 1
			time.sleep(0.05)
 
class th2:
	def __init__(self):
		self.val2 = 0
 
	def run(self):
		while 1:
			self.val2 += 1
			time.sleep(0.5)
 
if __name__ =="__main__":
	thread1 = th1()
	thread2 = th2()
	 # creating thread
	t1 = threading.Thread(target=thread1.run)
	t2 = threading.Thread(target=thread2.run)
 
	 # starting thread 1
	t1.start()
	# starting thread 2
	t2.start()
 
	while 1:
		print(thread1.val1, thread2.val2)
		time.sleep(0.1)
 
	 # wait until thread 1 is completely executed
	t1.join()
	 # wait until thread 2 is completely executed
	t2.join()
 
	 # both threads completely executed
	print("Done!")