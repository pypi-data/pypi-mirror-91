from setuptools import setup, find_packages 

#print(find_packages())
#import sys
#sys.exit(0)

with open('requirements.txt') as f:
    requirements = f.readlines() 

long_description = '''Python package used to fill an image's missing data gaps. \ 
    Specifically useful for obscuring image patterns in a machine learning context.''' 

setup(
    name ='missing_pixel_filler', 
    version ='0.0.1', 
    author ='Sarah Chen, Esther Cao', 
    author_email ='sarah.chen6@gmail.com, esthercao888@gmail.com', 
    url ='https://github.com/spaceml-org/empty-image-filler', 
    description ='downloading tool to fill missing image data gaps', 
    long_description = long_description, 
    long_description_content_type ="text/markdown",
    py_modules=['swath_activations', 'missing_pixel_filler'],
    package_dir={'': 'src'},
    #packages = find_packages(), 
    classifiers =( 
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent", 
    ), 
    keywords ='missing_pixel_filler missing_image_filler image_data_filler empty_image_filler pixel_filler image_filler filler pixel image', 
    install_requires = requirements
)
