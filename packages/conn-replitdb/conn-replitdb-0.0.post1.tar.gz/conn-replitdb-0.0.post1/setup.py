from setuptools import setup,find_packages

setup(
	name='conn-replitdb',
	version='0.0-1',
	author='Yarik0urWorld',
	description='Send data from computer to computer using repl.it database.',
	packages=find_packages(),
	python_requires='>=3.5',
	install_requires=[
		'replit'
	]
)
