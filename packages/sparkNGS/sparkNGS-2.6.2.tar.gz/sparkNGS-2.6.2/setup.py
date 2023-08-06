from setuptools import setup, find_packages 
 
#with open('requirements.txt') as f: 
#    requirements = f.readlines() 
requirements = 'numpy'
 
long_description = ''
  
setup( 
        name ='sparkNGS', 
        version ='2.6.2', 
        author ='Stefan Kurtenbach', 
        author_email ='stefan.kurtenbach@med.miami.edu', 
        #url ='https://github.com/amcruise/practice_party', 
        description ='', 
        long_description = long_description, 
        long_description_content_type ="text/markdown", 
        license ='MIT', 
        packages = find_packages(),
        entry_points = {
         'console_scripts': [
             'sparkNGS=spark.sparkmain:main',
          ],
        },
        classifiers =[ 
            "Programming Language :: Python :: 3", 
            "License :: OSI Approved :: MIT License", 
            "Operating System :: OS Independent", 
        ], 
        keywords ='', 
        install_requires = requirements, 
        zip_safe = False
) 
