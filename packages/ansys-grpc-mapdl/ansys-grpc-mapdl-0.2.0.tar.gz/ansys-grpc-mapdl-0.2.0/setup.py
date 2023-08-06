"""Installation file for the ansys-grpc-mapdl package"""
from setuptools import setup

install_requires = ['grpcio',
                    'google-api-python-client',
                    'protobuf']

setup(
    name='ansys-grpc-mapdl',
    packages=['ansys.grpc.mapdl'],
    version='0.2.0',
    license='MIT',
    url='https://github.com/pyansys/protos-mapdl',
    maintainer_email='alexander.kaszynski@ansys.com',
    description='Package for ansys-grpc-mapdl python gRPC client built on 10:45:01 on 12 January 2021',
    python_requires='>=3.5.*',
    install_requires=install_requires,
)
