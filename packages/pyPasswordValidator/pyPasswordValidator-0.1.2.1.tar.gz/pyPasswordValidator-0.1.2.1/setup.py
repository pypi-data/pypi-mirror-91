from setuptools import setup

setup(
    name='pyPasswordValidator',
    version='0.1.2.1',
    description='Attempts to detect if a password(s) passed meets requirements according to the The National Institute of Standards and Technology',
    url='https://github.com/jonjpbm/pyPasswordValidator',
    author='Jon Duarte',
    author_email='jonjpbm@gmail.com',
    license='MIT',
    packages=['pyPasswordValidator'],
    install_requires=['argparse',
                      ],
    classifiers=[
       'Development Status :: 1 - Planning',
	   'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
