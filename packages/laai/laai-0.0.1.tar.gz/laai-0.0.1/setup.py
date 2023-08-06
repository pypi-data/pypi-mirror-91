from setuptools import setup

setup(
	name='laai',
	version='0.0.1',
	py_modules=['laai'],
	install_requires=['click', 'docker'],
    include_package_data=True,
	entry_points='''
		[console_scripts]
		laai=laai:cli
	'''
)

