def f_read(path):
	with open(path, 'rt') as f:
		[print(line) for line in f.readlines()]


def move_files():
	import os
	# # one liner (only calls os.rename once)
	[os.rename(f, f.replace('\\', '/').replace('\t', '/t').replace('\r', '/r')) for f in os.listdir()]


# # correct path from pycharm bullshit
# [os.rename(f, f.replace('\\', '/')) for f in os.listdir()]
#
# # Correct tabs (\\t) in file name bullshit
# [os.rename(f, f.replace('\t', '/t')) for f in os.listdir()]
#
# # Correct (\\r) in file name bullshit
# [os.rename(f, f.replace('\r', '/r')) for f in os.listdir()]


def rmtree(dir_name):
	"""
	Delete all files and sub-directories of the specified directory
	"""
	import os
	if dir_name in os.listdir():  # If 'next' dir does not exist
		print("Deleting contents of: %s" % dir_name)
		for entry in os.ilistdir(dir_name):
			is_dir = entry[1] == 0x4000
			if is_dir:
				rmtree(dir_name + '/' + entry[0])
			else:
				print("\tDeleted: %s" % entry[0])
				os.remove(dir_name + '/' + entry[0])
		os.rmdir(dir_name)


def wipe_all(dir_list = ['api', 'assets', 'multiserver', 'project', 'webserver']):
	"""
	Delete all files (and sub-directories) in the list of directories
	"""
	for dir_name in dir_list:
		rmtree(dir_name)
	print("Done wiping")
