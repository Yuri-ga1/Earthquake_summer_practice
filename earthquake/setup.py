from setuptools import setup
import json
import os

def read_pipenv_dependencies(fname):
    """Получаем из Pipfile.lock зависимости по умолчанию."""
    filepath = os.path.join(os.path.dirname(__file__), fname)
    with open(filepath) as lockfile:
        lockjson = json.load(lockfile)
        return [dependency for dependency in lockjson.get('default')]

setup(
       name='eq',
       version='1.0',
       description='Data of global GNSS network are available at https://simurg.space, ionosonde data availabel through https://giro.uml.edu. The data paper uses along with notebook (with outputs preserved) are available here https://cloud.iszf.irk.ru/index.php/s/3RcnGdohf38kmAO . Email artem_vesnin@iszf.irk.ru if you have any questions about data format or behaviour of particular piece of code.',
       license='MIT',
       author='Artem Vesnin',
       author_email='artemvesnin@gmail.com',
       url='https://github.com/NikitaBagulov/earthquake.git',
       packages=['app'],
       install_requires=[*read_pipenv_dependencies('Pipfile.lock')],
       extras_require={
            'test': [
                'pytest',
                'coverage',
            ],
       },
       python_requires='>=3.10',
    )