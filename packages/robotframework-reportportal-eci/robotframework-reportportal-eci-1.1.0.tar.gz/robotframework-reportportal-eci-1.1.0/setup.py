from setuptools import setup, find_packages


__version__ = '1.1.0'

requirements = [
    "reportportal-client-eci==1.2.3",
    "six",
]

setup(
    name='robotframework-reportportal-eci',
    packages=find_packages(),
    version=__version__,
    description='Listener for RobotFramework reporting to ReportPortal',
    author='Artsiom Tkachou',
    author_email='SupportEPMC-TSTReportPortal@epam.com',
    url='https://github.com/reportportal/agent-Python-RobotFramework',
    download_url=(
        'https://github.com/reportportal/agent-Python-RobotFramework/'
        'tarball/{version}'.format(version=__version__)),
    keywords=['testing', 'reporting', 'robot framework', 'reportportal'],
    classifiers=[],
    install_requires=requirements
)
