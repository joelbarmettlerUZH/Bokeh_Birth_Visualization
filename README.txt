I used PyCharm as IDE with the newest version of anaconda, used libraries are pandas, bokeh and my own created class "chartclass"
To run the program, simply run the "Dashboard.py" and open up the output file called "dashboard.html". 
I created a chart Class and the charts BarChart, LineChart, DonutChart and GlyphChart which inherit from class Chart and share some functionality. 
The class definition is found in "chartclass.py", all the interaction with it is done in "Dashboard.py", which imports "chartclass.py". 
Therefore, make sure to place both files into the same directorie. The output html-file from bokeh will also be placed in thid directory.
I tested the code on Windows 10 Professional as well as on Mac OS X and it worked fine both times. 
I inserted a lot of comments to make my thoughts better understandable, and added some (in my opinion) cool features to some of the graphs. 
In the zip, there is also a screenshot from the last version of the dashboard, also called "dv_ex_1_16727877.jpg" and "dv_ex_1_16727877.pdf".
The code is all written by myself, but following the official bokeh-documentation. Therefore, the code will at some parts have reliance to the code snippets
that are presented on bokehs homepage.
The __init__.py is just to indicate that python can choose local modules from this folder. 


Hire us: [Software Entwickler in Zürich](https://polygon-software.ch)!
