def f_read(path):
	with open(path, 'rt') as f:
		[print(line) for line in f.readlines()]
