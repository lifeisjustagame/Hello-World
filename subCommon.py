import os
import sys

def split_file_name():
	file_dir, file_name = os.path.split(os.path.abspath(sys.argv[0]))
	if file_name.endswith('.py'):
		file_name = filename.replace('.py', '')

print(file_dir, file_name)	
