from core.http_requests import HttpClient
import os
import gc


class OTADownload:
	def __init__(self, github_repo, module='', tgt_dir='project'):
		self.http_client = HttpClient()
		self.github_repo = github_repo.rstrip('/').replace('https://github.com', 'https://api.github.com/repos')
		self.main_dir = tgt_dir
		self.module = module.rstrip('/')
	
	def start(self):
		if 'next' in os.listdir(self.module):
			if '.version_on_reboot' in os.listdir(self.modulepath('next')):
				latest_version = self.get_version(self.modulepath('next'), '.version_on_reboot')
				print('New update found: ', latest_version)
				self._download_and_install_update(latest_version)
		else:
			print('No new updates found...')
	
	def dev_download(self):
		"""
		Download and install the latest push to the Master branch
		"""
		# Create the 'next' directory
		if 'next' not in os.listdir():  # If 'next' dir does not exist
			os.mkdir('next')
		self._download_and_install_update(None)
	
	def _download_and_install_update(self, latest_version):
		self.download_all_files(self.github_repo + '/contents/' + self.main_dir, latest_version)
		
		if self.main_dir in os.listdir():  # If the target directory exists
			self.rmtree(self.modulepath(self.main_dir))
		if 'next' in os.listdir(self.module):
			if '.version_on_reboot' in os.listdir(self.modulepath('next')):
				os.rename(self.modulepath('next/.version_on_reboot'), self.modulepath('next/.version'))
			os.rename(self.modulepath('next'), self.modulepath(self.main_dir))
		print('Update installed (', latest_version, '), will reboot now')
		import machine, sys
		sys.exit()
	

	def rmtree(self, directory):
		print("Remove Directory: %s" % directory)
		for entry in os.ilistdir(directory):
			is_dir = entry[1] == 0x4000
			if is_dir:
				self.rmtree(directory + '/' + entry[0])
			else:
				os.remove(directory + '/' + entry[0])
		os.rmdir(directory)
	
	def download_all_files(self, root_url, version):
		print("\tFetching Directory: %s" % root_url)
		
		# Get Master if no version; otherwise get the specified version
		target_url = root_url if not version else root_url + '?ref=refs/tags/'
		file_list = self.http_client.get(target_url, dtype='json')
		
		# Create a much smaller version of the data
		file_params = {
			'file': [],
			'dir': []
		}
		for file in file_list:
			if 'type' in file:
				file_type = file['type']
				
				file_params[file_type].append({
					'download_url': file['download_url'],
					'path': file['path'],
					'name': file['name'] if 'name' in file else None
				})
		
		del file_list  # Reset/erase data
		gc.collect()
		
		for file_type in file_params:  # Loop through each file type
			for file in file_params[file_type]:  # Loop through each file
				download_url = file['download_url']
				file_path = file['path']
				file_name = file['name']
				
				if file_type == 'file':
					download_path = self.modulepath('next/' + file_path.replace(self.main_dir + '/', ''))
					print("Downloading: %s" % file_name)
					if not version:
						self.download_file(download_url, download_path)
					else:
						self.download_file(download_url.replace('refs/tags/', ''), download_path)
				elif file_type == 'dir':
					path = self.modulepath('next/' + file_path.replace(self.main_dir + '/', ''))
					
					try:
						os.mkdir(path)
					except OSError:
						print('Directory exists; skipping: ' + path)
					
					self.download_all_files(root_url + '/' + file_name, version)
			gc.collect()
	
	def download_file(self, url, path):
		with open(path, 'w') as outfile:
			try:
				response = self.http_client.get(url, dtype='text')
				outfile.write(response)
			finally:
				outfile.close()
				gc.collect()
	
	def modulepath(self, path):
		return self.module + '/' + path if self.module else path
	
	def get_version(self, directory, version_file_name='.version'):
		if version_file_name in os.listdir(directory):
			f = open(directory + '/' + version_file_name)
			version = f.read()
			f.close()
			return version
		return '0.0'
