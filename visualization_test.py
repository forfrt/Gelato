from django.shortcuts import render, render_to_response
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.embed import components
from bokeh.layouts import column
import pandas as pd
from bokeh.models import HoverTool
from collections import OrderedDict
import datetime
import numpy as np

# Create your views here.
def homepage(request):
    '''
    # Graph x and y coordinates
    x = [1,2,3,4,5]
    y = [1,2,3,4,5]

    # setup graph plot for sisplaying line graph
    plot = figure(title = "Line Graph", x_axis_label = 'X-Axis', y_axis_label = 'Y_Axis', plot_width = 400, plot_height = 400)
    plot.line(x,y,line_width = 2)
    # circle Graph
    source = ColumnDataSource(data=dict(
    x=[1, 2, 3, 4, 5],
    y=[2, 5, 8, 2, 7],
    desc=['A', 'b', 'C', 'd', 'E'],
    ))

    TOOLTIPS = [
    ("index", "$index"),
    ("(x,y)", "($x, $y)"),
    ("desc", "@desc"),
    ]

    p = figure(plot_width=400, plot_height=400, tooltips=TOOLTIPS,
           title="Mouse over the dots")

    p.circle('x', 'y', size=20, source=source)

    # store components
    script, div = components(column(p, plot))
    '''
    # Read in our data. We've aggregated it by date already, so we don't need to worry about paging
    query = ("https://data.lacity.org/resource/mgue-vbsx.json?"
        "$group=date"
        "&call_type_code=507P"
        "&$select=date_trunc_ymd(dispatch_date)%20AS%20date%2C%20count(*)"
        "&$order=date")
    raw_data = pd.read_json(query)
    # Augment the data frame with the day of the week and the start of the week that it's in.
    raw_data['day_of_week'] = [date.dayofweek for date in raw_data["date"]]
    raw_data['week'] = [(date - datetime.timedelta(days=date.dayofweek)).strftime("%Y-%m-%d") for date in raw_data["date"]]
     
    # Pivot our data to get the matrix we need
    data = raw_data.pivot(index='week', columns='day_of_week', values='count')
    data = data.fillna(value=0)
     
    # Get our "weeks" and "days"
    weeks = list(data.index)
    days = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]
    # Set up the data for plotting. We will need to have values for every
    # pair of year/month names. Map the rate to a color.
    max_count = raw_data["count"].max()
    day_of_week = []
    week = []
    color = []
    parties = []
    for w in weeks:
        for idx, day in enumerate(days):
            day_of_week.append(day)
            week.append(w)
            count = data.loc[w][idx]
            parties.append(count)
            color.append("#%02x%02x%02x" % (255, int(255 - (count / max_count) * 255),int( 255 - (count / max_count) * 255.0)))

    source = ColumnDataSource(
    data=dict(
        day_of_week=day_of_week,
        week=week,
        color=color,
        parties=parties,
        w = [1]*len(parties),
        h = [1]*len(parties)
        )
    )
    TOOLS = "hover"

    p=figure(
        title='\"Heatmap\" Example', 
        x_range=weeks, 
        y_range=list(reversed(days)),
        tools=TOOLS)
    p.plot_width=900
    p.plot_height = 400
    p.toolbar_location='left'

    p.rect(x="week", y= "day_of_week",height = "h", width = "w", source = source,color="color", line_color=None)

    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "10pt"
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = np.pi/3

    hover = p.select(dict(type=HoverTool))
    hover.tooltips = OrderedDict([
        ('parties', '@parties'),
    ])
    script, div = components(p)

    return render_to_response("visualization.html",{' heatmapscript':script,' heatmapdiv':div})
