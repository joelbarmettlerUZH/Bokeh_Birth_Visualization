from bokeh.io import output_file, show
from bokeh.layouts import layout, widgetbox
from chartsclass import *
from bokeh.models.widgets import Div

####################################
####Joel Barmettler - 17-727-877####
####################################

#defining the output file for bokeh
output_file("dashboard.html")

#Creating a HTML-Element for the title section with some CSS styling
title = Div(text="""<h1 style="text-align: center; font-weight: 200; padding-top: 20px; font-size: 250%; font-family: Sans-Serif;">
            Dashboard: Births in Zurich, CH from 1993 - 2013</h1>"""
            , width=1050, height=60)

#Creating a HTML-Element for the description sentense under the title, again with some CSS styling
description = Div(text="""<p style="text-align: center; font-weight: 200; font-size: 100%; font-family: Sans-Serif; color: DimGrey ;" >
                 This Dashboard show different Visualizations of the Births that occurred in canton of Zurich from 1993 to 2015. The data are provided from the swiss national institute of statistics.
                 <br>This project is executed for the course "Data Visualization" at the University of Zurich, UZH.</p>
                 """
                  , width=1050, height=70)

#calling the BarChart class and creating an instance relying on the dataset given as an argument
StackedBar_MF_2015 = BarChart("bevgeburtenjahrgeschlquartstz.csv")
#Setting propper index column names to later adress data with fitting names
StackedBar_MF_2015.set_columns("Year", "Sex-ID", "Sex", "SubareaID", "Subarea", "AreaID", "Area", "Births")
#redefining some values in the dataset, namely W (Weiblich) to F (Feminin) to match the english langauge of the course
StackedBar_MF_2015.map("Sex", {"M": "M", "W": "F"})
#Transforming the dataset, namely selecting the needed rows and collumns, converting it into fitting datatypes to prepare for plotting. More info in chartsclass
StackedBar_MF_2015.transform_data(2015)
#Getting the bar returned to later plot it
bar = StackedBar_MF_2015.create_bar()

#calling the LineChart class and creating an instance relying on the dataset given as an argument
TimeSeries = LineChart("bevgeburtenjahrgeschlquartstz.csv")
TimeSeries.set_columns("Year", "Sex-ID", "Sex", "SubareaID", "Subarea", "AreaID", "Area", "Births")
TimeSeries.map("Sex", {"M": "M", "W": "F"})
TimeSeries.transform_data()
TimeSeries.create_line()
#Setting additional attributes to the LineChart class cause we deal with multiple lines in one plot, more detailed description in the chartsclass
line = TimeSeries.set_attributes()

#calling the DonutChart class and creating an instance relying on the dataset given as an argument
Donut_MF_2015 = DonutChart("bevgeburtenjahrgeschlquartstz.csv")
Donut_MF_2015.set_columns("Year", "Sex-ID", "Sex", "SubareaID", "Subarea", "AreaID", "Area", "Births")
Donut_MF_2015.map("Sex", {"M": "M", "W": "F"})
Donut_MF_2015.transform_data()
donut = Donut_MF_2015.create_Donut()

#calling the GlyphChart class and creating an instance relying on the dataset given as an argument
Glyph_TopX_Area = GlyphChart("bevgeburtenjahrgeschlquartstz.csv")
Glyph_TopX_Area.set_columns("Year", "Sex-ID", "Sex", "SubareaID", "Subarea", "AreaID", "Area", "Births")
Glyph_TopX_Area.map("Sex", {"M": "M", "W": "F"})
Glyph_TopX_Area.transform_data("Oerlikon", 5)
glyph = Glyph_TopX_Area.create_Glyph()

#Rendering the plot to the output file with a grid layout: Title --> description --> bar --> line, donut, glyph from top to bottom
show(layout([widgetbox(title)],[widgetbox(description)],[bar],[line, donut, glyph]))
