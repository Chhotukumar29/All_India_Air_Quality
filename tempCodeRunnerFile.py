from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = '-e .'
def get_requirements(file_path:str) -> List[str]:
    '''
    This function will return a list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements = file_path.readlines()
        requirements= [req.replace("\n", " ") for req in requirements]
        
        if HYPEN_E_DOT_RE in requirements:
            requirements.remove(HYPEN_E_DOT_RE)
            
    return requirements

setup(
    Name = 'Air Quality Gurugram',
    Version = '0.0.1',
    author= 'Chhotu Kumar',
    author_email= 'Chhotuchiitodiya@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)