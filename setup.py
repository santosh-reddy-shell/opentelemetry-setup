from setuptools import setup, find_packages

setup(
    name='opentelemetry-setup',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'opentelemetry-api',
        'opentelemetry-sdk',
        'opentelemetry-exporter-otlp-proto-http',
        'requests'  # Add any other dependencies here
    ],
    entry_points={
        'console_scripts': [
            # Define any console scripts if needed
        ],
    },
    author='Your Name',
    author_email='your-email@example.com',
    description='A package to set up OpenTelemetry for logging, tracing, and metrics',
    url='https://github.com/your-username/opentelemetry-setup',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
