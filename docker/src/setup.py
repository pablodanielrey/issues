"""
    https://packaging.python.org/distributing/
    https://pypi.python.org/pypi?%3Aaction=list_classifiers
    http://semver.org/

    zero or more dev releases (denoted with a ”.devN” suffix)
    zero or more alpha releases (denoted with a ”.aN” suffix)
    zero or more beta releases (denoted with a ”.bN” suffix)
    zero or more release candidates (denoted with a ”.rcN” suffix)
"""

from setuptools import setup, find_packages

setup(name='issues',
          version='0.1.0.dev0',
          description='Interface web del sistema de tareas redmine',
          url='https://github.com/pablodanielrey/issues',
          author='Desarrollo DiTeSi, FCE',
          author_email='ditesi@econo.unlp.edu.ar',
          classifiers=[
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5'
          ],
          packages=find_packages(exclude=['contrib', 'docs', 'test*']),
          install_requires=['psycopg2',
                            'dateutils>=0.6.6',
                            'requests',
                            'redis',
                            'Flask',
                            'flask_jsontools',
                            'Flask-OIDC',
                            'SQLAlchemy',
                            'google-api-python-client',
                            'httplib2',
                            'pyjwt',
                            'itsdangerous',
                            'python-redmine',
                            'microservices_common'],
          entry_points={
            'console_scripts': [
                'wamp=issues.api.wamp.main:main',
                'rest=issues.api.rest.main:main',
                'flask=issues.web.main:main'
            ]
          }

      )
