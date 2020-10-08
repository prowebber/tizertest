


def move_files():
	import os
	
	# correct path from pycharm bullshit
	[os.rename(f, f.replace('\\', '/')) for f in os.listdir()]
	
	# Correct tabs (\\t) in file name bullshit
	[os.rename(f, f.replace('\t', '/t')) for f in os.listdir()]
	
	# Correct (\\r) in file name bullshit
	[os.rename(f, f.replace('\r', '/r')) for f in os.listdir()]


def wipe_all():
	"""
	Delete all files (and sub-directories) in the list of directories
	"""
	dir_list = ['api', 'assets', 'multiserver', 'project', 'webserver']
	for dir_name in dir_list:
		rmtree(dir_name)
	print("Done wiping")


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