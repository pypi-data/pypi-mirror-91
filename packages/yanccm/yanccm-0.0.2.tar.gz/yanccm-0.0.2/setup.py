from distutils.core import setup

setup(
    name='yanccm',
    packages=[
        'controller',
        'sot',
        'ncservice',
        'ncservice.configDb',
        'ncservice.ncDeviceOps',
        'ncservice.ncDeviceOps.threaded',
        'view'],
    version='0.0.2',
    license='MIT',
    description='''YANCCM (pronounced yank'em) - Yet Another Network Configuration and Change Managment tool, is 
    multi-threaded configuration manger for network devices that leverages the NETCONF protocol''',
    author='Richard Cunningham',
    author_email='cunningr@gmail.com',
    url='https://github.com/cunningr/yanccm',
    download_url='https://github.com/cunningr/yanccm',
    keywords=['Netconf', 'Cisco', 'configuration management'],
    install_requires=[
        'ncclient',
        'lxml',
        'pyyaml',
        'pymongo',
        'tabulate',
        'requests',
        'jinja2'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],
    entry_points={
        'console_scripts': [
            'yanccm = controller.cli:main'
        ]
    }
)
