from bokeh.plotting import figure
from bkcharts import Bar, Donut
import pandas as pd
from bokeh.models import HoverTool, ColumnDataSource, Span, LabelSet, Label

####################################
####Joel Barmettler - 17-727-877####
####################################

class Chart():
    #Every instance of Chart has a corresponding csv file, a figure and a dataframe. Timeseries is optional. The file path is given, the other values set to none
    def __init__(self, file):
        self._csv = pd.read_csv(file)
        self._timeseries = None
        self._dataframe = None
        self._figure = None

    def set_columns(self,*args):
        #We let the user set the collumns by itself, from left to right. The missing collumns on the right are not set and left as the standard value from the csv itself.
        self._csv.columns = args

    def map(self, collumn, maprule):
        #Some values in the csv might be suboptimal, so we replace the values in "collumn" with the stated rule, which needs a dict with
        #current values as keys and their wished new value as values. The dataset is transformed and overwritten.
        self._csv[collumn] = self._csv[collumn].map(maprule)

    def create_timeseries(self):
        #Here, we transform the data to make creating a timeseries possible, we do this in general Chart class cause we might (and do) need it several times
        #We seperate the data in Masculin and Feminin data, and only extract the collumns regarding Year and Birth number.
        df_2_m = self._csv.loc[self._csv["Sex"] == "M"][["Year", "Births"]].to_dict()
        df_2_f = self._csv.loc[self._csv["Sex"] == "F"][["Year", "Births"]].to_dict()
        #We then transform the dict created from pandas to a form that we can easily use. The goal is to have propper formatted df_m and df_f
        df_m = {}
        df_f = {}
        #We don't want to write two for-loops, so we just map the corresponding df_2_f and df_f together and deal with the container instead
        container = [[df_2_m, df_m],[df_2_f, df_f]]
        #Outer for loop: Taking one of the container pairs that belong together and apply the inner rules to them
        for workingdata, finaldata in container:
            #for every year that exists in the dataset
            for index, year in workingdata["Year"].items():
                #When this year is not in the final, transformed dataset already
                if year not in finaldata.keys():
                    #create a new entry in the final dataset with the year as an key and the corresponding birth-value as its value. Continue then.
                    finaldata[year] = workingdata["Births"][index]
                    continue
                #the year seems to be in the final dataset already, so we just add the birth number to this entry by adding it to its value
                finaldata[year] += workingdata["Births"][index]
        #Now that we propperly transformed our individual, M and F datasets, we group them together into a dictionary and store it in the class variable self.timeseries
        self._timeseries = {
            "M":df_m,
            "F":df_f
        }


class BarChart(Chart):
    def transform_data(self, year):
        #Only select data from the year that the user provided
        csv_1 = self._csv.loc[self._csv["Year"] == year]
        #Select Sex, Area and Births from this year
        df = csv_1[["Sex", "Area", "Births"]].to_dict()
        #Now, the dataset is a dictionary with indices and values. But what we want is a dict that has the form: {area: (), Sex: (), Births: ()}
        #We therefore need to get rid of the indices and, in the same step, create a list out of the values AND sort it according to the index, otherwise we would loose the relation between
        #Area, Sex and Births.
        for key in df.keys():
            #With a zip, we concatenate the indices and the values for each key (area, sex, births) together, sort by the index and assign them to two variables.
            waste, df[key] = zip(*sorted(zip(df[key].keys(),df[key].values())))
            #Indices are not needed anymore, so I delete the variable to free space
            del waste

        #Now that we have the right data, we need to get ridd of the duplicates cause every region also has several subregions. So, We create a new frame in which we get ridd of the subregions and only preserve
        #a region two times, one for each gender
        dataframe = {
            "Area":[],
            "Sex":[],
            "Births":[]
        }
        #We set the initial values for the list
        for area in set(df["Area"]):
            dataframe["Area"].insert(0, area)
            dataframe["Area"].insert(0, area)
            dataframe["Sex"].insert(0, "F")
            dataframe["Sex"].insert(0, "M")
            dataframe["Births"].insert(0, 0)
            dataframe["Births"].insert(0, 0)
        #Now we go through the df dataframe and for every entry,
        for df_i in range(len(df["Area"])):
            #we find out to the corresponding entry in the final dataframe ("Affoltern M" might be the 543th entry in the df, but the 23 entry in the dataframe)
            dataframe_i = dataframe["Area"].index(df["Area"][df_i])
            #Females are always following the males, so when we got a female we need to hop to the next field cause we always found the male-entry with the search above, cause male is the first entry
            if df["Sex"][df_i] == "F":
                dataframe_i += 1
            #Now increment the birth value in the dataframe by the number of births in the df
            dataframe["Births"][dataframe_i] += df["Births"][df_i]
        #Now we assign this dataframe to the class-variable dataframe in order to use it later for plotting
        self._dataframe = dataframe

    def create_bar(self):
        #Here, we interact with bokeh to create the bar chart. We use the dataframe we created above, set birth to the values on the y-axis and stack the data by sex.
        #The x axis label is represented by the areas. We define hover over the tooltips and define Gender and Births, with the corresponding value of the y axis.
        #Last but not least, we colour the data with always coloring female red and male blue.
        bar = Bar(
            self._dataframe, values='Births', label='Area', stack="Sex", agg="mean",
            title="Births in Zurich, 2015 per Area", legend='top_right', height=450, width=1050,
            tooltips=[('Gender:', '@Sex'), ('Births:', '@height')], palette=["#cc3737", "#0053d8"]
        )
        #we return the bar to plot in on the Dashboard class
        return bar


class LineChart(Chart):
    def transform_data(self):
        #Linechart is a typical timeseries, so we create a dataset from a timeseries
        self.create_timeseries()
        self._dataframe = self._timeseries
        #We want three lines: Male, Female and their Sum, so we create another entry in our dataset for the sum
        self._dataframe["SUM"] = {}
        # Now we go through both genders
        for gender in ["M","F"]:
            #For every year in the specific gender
            for year, births in self._dataframe[gender].items():
                #When the year is not already in the SUM-dataset, add an entry and set the corresponding births-value, continue then
                if year not in self._dataframe["SUM"].keys():
                    self._dataframe["SUM"][year] = births
                    continue
                #If the there is already an entry for the current year in the sum-dataset, we just add the current birth-value to it
                self._dataframe["SUM"][year] += births



    def create_line(self):
        #To be able to hover over a line, we specify a hover tool
        hover = HoverTool()
        #The y axis symbolizes the number of birts, the x axis the year. So we set these two values to our hover tool and add fitting descriptions to them
        hover.tooltips = [("Births", "@y"),
                          ("Year", "@x")]
        #Then we plot the figure. I set the y-range a bit higher so that the legend does not cover important data. We add the hover to the toolbox
        #And stick the toolbar to the top where I think it looks nicer than to the right.
        fig = figure(plot_width=350, plot_height=250, title="Births per Year in Zurich",
                    y_range=(0, max(self._dataframe["SUM"].values()) * 1.3),
                    tools=[hover, "pan", "box_zoom", "wheel_zoom", "reset", "save"],
                    toolbar_location="below", toolbar_sticky=False
                    )
        #We label the axis and set the class attribute figure to the created figure
        fig.xaxis.axis_label = "Year"
        fig.yaxis.axis_label = "Number of Births"
        self._figure = fig

    def set_attributes(self):
        #In this method, we want to set the attributes like colour and legend to all the lines in the graph

        #A method intern function that setts the line attribute of a line object, so that all lines fit into the same graph with the same properties
        #We set the legend to a horizontal one and make it transparent to not disturb from the data, add a bit of padding etc.
        def apply_attributes(obj):
            obj.min_border_left = 100
            obj.legend.orientation = "horizontal"
            obj.legend.background_fill_alpha = 0.5
            obj.legend.padding = 2

        #We create a Zip out of the data, with the first, second and third entries belonging together
        datazip = zip(
            [self._dataframe["F"], self._dataframe["M"], self._dataframe["SUM"]],
            ["#cc3737", "#0053d8", "#0c9600"],
            ["Female", "Male", "Both"]
        )

        #Then we loop through all the grouped data in the zip after each other
        for (dct, colr, leg) in datazip:
            #The x and y axis is set by the year-births tuple, ordered by year
            x, y = zip(*sorted(zip(dct.keys(), dct.values())))
            #We create the figure with the corresponding line colour and line width
            self._figure.line(x, y, color=colr, legend=leg, line_width=1.5)
            #Finally, we apply the standard attributes like legend, boarder, padding etc. through the function
            apply_attributes(self._figure)

        #We are done with adding the attributes to our figure, so we again return it to later plot it in the dashboard
        return self._figure

class DonutChart(Chart):
    def transform_data(self):
        #We are only interested in data from 2015, namely sex and birth, so we only select these data and convert it to a dict
        csv_1 = self._csv.loc[self._csv["Year"] == 2015]
        df = csv_1[["Sex", "Births"]].to_dict()
        #now we go through the dict and, to each key (births, sex), we add a list of its values sorted by index, like we already did earlier above
        for key in df.keys():
            waste, df[key] = zip(*sorted(zip(df[key].keys(), df[key].values())))
        #Now we sum up all the births of males and females, by going thorugh the sex-list and, each time the sex is male, add it to a new list with only
        #male birth numbers. When we went through the whole sex list, we sum all the values up and assign it to a new variable called total_m.
        #We do the same for the female sex.
        total_m = sum([df["Births"][i] for i in range(len(df["Sex"])) if df["Sex"][i] == "M"])
        total_f = sum([df["Births"][i] for i in range(len(df["Sex"])) if df["Sex"][i] == "F"])
        #Out of these two variables, we create a dictionary with sex as key and their corresponding total births in 2015 as a percentage value
        self._dataframe = {
            "% Male": round(total_m / (total_m + total_f)*100, 3),
            "% Female": round(total_f / (total_m + total_f)*100, 3)
        }

    def create_Donut(self):
        #We transform the dictionary to a panda series with the birth-numbers as the index, cause the Donut needs a pandas dataframe to deal with
        series = pd.DataFrame(self._dataframe, index=["Births"]).transpose()
        #Then, we create the donut chart out of this data, with individual colours for both entries, a toolbar and only a few tools cause the other ones
        #are quiet unnecessary for a donut chart. The label on the donut segments corresponds to the index, which we set to the Births.
        d = Donut(series, title="Births per Gender, 2015",
                  width=300, height=250, palette=["#cc3737", "#0053d8"], legend=True, label='index',
                  toolbar_location="below", toolbar_sticky=False, match_aspect=True,
                  tools=["pan", "reset", "save"]
                  )
        d.min_border_left = 150
        #We return the donut to later plot it in the dashboard
        return d

class GlyphChart(Chart):
    def transform_data(self, area, number):
        #The user can chose a valid area and the top "number" subareas he wants to have presented, so we set them as class variables to deal with them later on
        self._area = area
        self._number = number
        #We select the data where "Area" corresponds to the users chosen area and the year is 2015, from there we want to have the subareas and Births
        df = self._csv.loc[self._csv["Area"] == self._area][self._csv["Year"] == 2015][["Subarea", "Births"]].to_dict()
        #We quickly sum up the total number of births to mark it later on the graph
        self._total_births = sum(df["Births"].values())
        #We now want to transfrom our dataset, cause every subarea may appear multiple times in the list
        self._dataframe = {}
        #We do the same procedure as we did many times above, so I won't fully explain all of it again. For every subarea, when it is not in the new dataset
        #already, add it and its birth value, otherwise just add the birth value to the existing entry. Done.
        for key, value in df["Subarea"].items():
            if value not in self._dataframe.keys():
                self._dataframe[value] = df["Births"][key]
                continue
            self._dataframe[value] += df["Births"][key]
        #We again create a list out of the dictionaries values, ordered by index
        y, x = zip(*sorted(zip(self._dataframe.values(), self._dataframe.keys())))
        #We select the highest X values, or the maximal number of possible values when there are not enough subareas
        self._x_topX = x[:-min(self._number + 1, len(x) + 1):-1]
        self._y_topX = y[:-min(self._number + 1, len(x) + 1):-1]

    def create_Glyph(self):
        #We format the dataset for our glyph chart. Cause we deal with unnumerical values on the x axis, we just plot the data uniformly distributed one after another
        #Thats why we just create a range of values on the x axis. The area is meant as a description, so we assign the subarea names to it
        glyph_source = ColumnDataSource(data=dict(
            x = range(1,self._number+1),
            y = self._y_topX,
            area = self._x_topX
        ))
        #We again create the hover tool with Area corresponding to the above set area attribute (subarea names) and value corresponding to the y axis, which is the number of births
        hover = HoverTool(
            tooltips = [("Area", "@area"),
                        ("Births","@y")],
            #We use the vline mode this time so that the user does not have to directly hover over the point only but can be above or under it and it still shows the data in the hover box
            mode="vline"
        )

        #Now we creat the figure with the range in y direction being 1.2 times the total births, cause I later want to draw a horicontal line at that value and want two declare the lines meaning
        #aboce it, so we need some space there. The x range is just the number of values + a bit space to the left + a bit space to the right to have enough space for the writing
        p = figure(plot_width=400, plot_height=250, title="Top {} Birth areas in {}, 2015".format(self._number, self._area),
                   toolbar_location="below", toolbar_sticky=False,
                   y_range=(0, self._total_births * 1.2), x_range=(0.5, self._number+1),
                   tools=[hover, "pan", "box_zoom", "wheel_zoom", "reset", "save"]
                   )
        #Now we define the squares, with the x axis just being the uniform values, and the y axis being the birth rate, the colour is green to match the general "SUM" colour of our dashboard
        p.square(x="x", y = "y", size=8, color="#0c9600", source=glyph_source)
        #Then, at each datapoint, we also set the area name as a textlabel with a 45° angle so that the subarea names do not overlap
        datapoint_name = LabelSet(x="x", y = "y", text="area", level="glyph", x_offset=5, angle=45, text_font_size = "8pt",
                          y_offset=5, source=glyph_source, render_mode='canvas'
                          )
        #We finally create the description for the top-line at the total-birth value
        line_name = Label(x=110, y=270, x_units='screen',
                         text='Total Births in {}'.format(self._area), render_mode='css',
                         text_font_size="8pt",
                         background_fill_color='white', background_fill_alpha=0.5
                         )
        #Then, we create the line as a Span at total_births height, make it dashed and again the green color
        x_line = Span(location=self._total_births, dimension="width", line_dash="dashed", line_color='#0c9600')
        #We add the line to the layout, make the x axis invisible because it does not contain any usefull data (just 1,2,3,4..X) and add the datapoint_name & horizontal line description to the model
        p.add_layout(x_line)
        p.xaxis.visible = False
        p.add_layout(datapoint_name)
        p.add_layout(line_name)
        p.min_border_left = 150
        #We  name the axis and return the chart to later plot it to the Dashboard
        p.xaxis.axis_label = ("Subarea of " + str(self._area))
        p.yaxis.axis_label = "Number of Births"
        return p
