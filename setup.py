from setuptools import setup,find_packages
hyphen_e_dot='-e .'
def get_requirements(file_path:str)->list[str]:
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]
        if hyphen_e_dot in requirements:
            requirements.remove(hyphen_e_dot)

    return requirements   
setup(
    name='MLops',
    version='0.0.1',
    author='Nayak',
    author_email='nayakamrutansu190@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)     