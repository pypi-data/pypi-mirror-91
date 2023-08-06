from setuptools import setup, find_packages 
  
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
  
setup( 
        name ='Trello-CLI-Example-hanabou', 
        version ='1.0.1', 
        author ='Hana Bou-Ghannam', 
        author_email ='hanaboughannam@gmail.com', 
        url ='https://github.com/hanaboughannam/Trello-CLI-Example', 
        description ='Example CLI Script to Create Trello Cards', 
        long_description = long_description, 
        long_description_content_type ="text/markdown", 
        license ='MIT', 
        packages = find_packages(), 
        entry_points ={ 
            'console_scripts': [ 
                'trello_cli = trello_cli_example.trello_cli:main'
            ] 
        }, 
        classifiers =( 
            "Programming Language :: Python :: 3", 
            "License :: OSI Approved :: MIT License", 
            "Operating System :: OS Independent", 
        ), 
        python_requires='>=3.6',
        install_requires = [
            'requests==2.25.1',
            'docopt==0.6.2'
        ], 
        zip_safe = False
)