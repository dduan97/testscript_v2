"""
TestParser class blah blah blah
feed it test files and it'll parse them and stuff
"""

class TestParser:

	def __init__(self, esc_args="#ARGS", esc_lines="#LINES"):
		self.esc_args = esc_args
		self.esc_lines = esc_lines
		self.test_queue = []

	def sink(self, test_string):
		"""
		Takes in a string and parses it to be later retrieved as command line
		arguments and standard input strings by TestParser.poll()
		"""
		if not test_string:
			self.test_queue.append(("", ""))
			return

		lines = test_string.split("\n")
		first_line = lines.pop(0)

		# check if the first line says it's a line-by-line file
		if first_line.startswith(self.esc_lines):
			cmd_args = []
			# then we want to loop through the rest line by line
			while lines:
				# pop off the first line. if it denotes args, set the args,
				# otherwise assume it's standard input and append to the 
				# queue
				current_line = lines.pop(0)
				if current_line.startswith(self.esc_args):
					cmd_args = first_line[len(cmd_args):].split()
				else:
					std_in = current_line
					self.test_queue.append((cmd_args, std_in))
			return

		else:
			# we have a whole-file test case

			# initialize the command line arguments to nothing
			cmd_args = []

			# if the first line denotes args, set cmd_args accordingly
			if first_line.startswith(self.esc_args):
				cmd_args = first_line[len(self.esc_args):].split()
			else:
				lines.insert(0, first_line)

			# now the rest of the lines are stdin
			std_in = "\n".join(lines)
			self.test_queue.append((cmd_args, std_in))

	def has_test(self):
		return bool(self.test_queue)

	def poll(self):
		if self.test_queue:
			return self.test_queue.pop(0)
		return None
