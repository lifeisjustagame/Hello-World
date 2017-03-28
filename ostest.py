import os
import sys

file_dir, file_name = os.path.split(os.path.abspath(sys.argv[0]))

print('sys.argv[0]= ', sys.argv[0])
print('os.path.abspath= ', os.path.abspath(sys.argv[0]))
print('file_dir = ', file_dir)
print('file_name = ', file_name)

if file_name.endswith('.py'):
	file_name = file_name.replace('.py', '')

print('reviesed result:', file_dir, file_name)


LOG_DIR = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]), "log"))
print('LOG_DIR = ', LOG_DIR)


