from setuptools import setup

requirements = [
	'plumbum'
]

setup(
	# Metadata
	name='postage_code',
	version='0.0',
	install_requires=requirements,
	entry_points={
		'console_scripts':
			['postage = app.main:PostageApp.run']
		}
)