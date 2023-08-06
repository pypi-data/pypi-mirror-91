import setuptools

INSTALL_REQUIRES = ["Flask==1.1.2", "firebase-admin==4.5.0"]

setuptools.setup(
    name="flask-FCMAdmin", # Replace with your own username
    version="0.0.2",
    author="chienaeae",
    author_email="chienaeae@gmail.com",
    description="fcm admin with flask",
    long_description="fcm admin with flask",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=INSTALL_REQUIRES,
    python_requires='>=3.6',
)