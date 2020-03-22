# Project : OSM, Photos, and Tours

​	Open Street Map (OSM) is an online map collaboration project for the construction of free content. In this project, we are provided with the processed OSM data, that is, some important attributes extracted from the geotagged photos of Vancouver. In this project, we discussed 4 problems we were interested in, including the urban functional zone problem, where to choose a hotel, the distribution of chain restaurants and non-chain restaurants and tourist attractions recommendation. Throughout the document we explain how we collect and process our data, how we analyze them and what results we got.

## Getting Start

These instructions will help you running the project on your local machine.

### Prerequisites

You need install [python](https://www.python.org/) and some third-party libraries of python. After installing python, you need open your terminal and install some libraries.

~~~
MacBook-Air:program charlie$ pip3 install folium
~~~

~~~ 
MacBook-Air:program charlie$ pip3 install pandas
~~~

~~~
MacBook-Air:program charlie$ pip3 install seaborn
~~~

~~~
MacBook-Air:program charlie$ pip3 install matplotlib
~~~

~~~
MacBook-Air:program charlie$ pip3 install sklearn
~~~

~~~
MacBook-Air:program charlie$ pip3 install scipy
~~~



### Test with the project

After you installing all of the libraries, you can open your ternimal and You need to open your terminal and change directory to the directory where the python files are located

~~~ 
MacBook-Air:program charlie$ cd /.../program
~~~

And then, you can start run the python file.

~~~
MacBook-Air:program charlie$ python3 attractions.py
0.5266666666666666
0.5866666666666667
0.66
Successfully Create HTML Files in folder output_attraction!
~~~

Then, you can find some HTML files and png files in the output directory.



 