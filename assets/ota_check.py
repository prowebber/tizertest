from assets.http_requests import HttpClient
import os


class OTACheck:
	def __init__(self, github_repo, module='', tgt_dir='project'):
		self.http_client = HttpClient()
		self.github_repo = github_repo.rstrip('/').replace('https://github.com', 'https://api.github.com/repos')
		self.main_dir = tgt_dir
		self.module = module.rstrip('/')
	
	def start(self):
		current_version = self.get_version(self.modulepath(self.main_dir))
		latest_version = self.get_latest_version()
		
		print('\tCurrent version: ', current_version)
		print('\tLatest version: ', latest_version)
		
		if latest_version > current_version:
			print('New version available, will download and install on next reboot')
			
			if 'next' not in os.listdir(self.module):
				os.mkdir(self.modulepath('next'))
			
			with open(self.modulepath('next/.version_on_reboot'), 'w') as versionfile:
				versionfile.write(latest_version)
				versionfile.close()
	
	def get_version(self, directory, version_file_name='.version'):
		if version_file_name in os.listdir(directory):
			f = open(directory + '/' + version_file_name)
			version = f.read()
			f.close()
			return version
		return '0.0'
	
	def get_latest_version(self):
		"""
		Get the 'latest' version specified in GitHub
		- Open the URL
		- Download the specs and return the version number
		"""
		latest_release = self.http_client.get(self.github_repo + '/releases/latest', dtype='json')
		version = latest_release['tag_name']
		return version
	
	def modulepath(self, path):
		return self.module + '/' + path if self.module else path