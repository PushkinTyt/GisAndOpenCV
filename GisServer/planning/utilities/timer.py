import time



class Timer:
	def __init__(self, template):
		self.template = template
		
		
		
	def __enter__(self):
		self.start = time.time()
		return self
		
	def __exit__(self, *args):
		self.end = time.time()
		self.secs = self.end - self.start
		self.msecs = self.secs * 1000  # millisecs
		print(self.template % self.secs)
		