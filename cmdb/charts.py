from bokeh.plotting import figure, ColumnDataSource
from bokeh.embed import components
import pandas as pd
from bokeh.models import HoverTool, Range1d
from collections import OrderedDict
import numpy as np
from cmdb.models import Assignments, Modules
import datetime
from datetime import timedelta
from dateparser import parse
import random
from bokeh.io import curdoc
from cmdb import models

from bokeh.plotting import figure, ColumnDataSource
from bokeh.embed import components
import pandas as pd
from bokeh.models import HoverTool, Range1d
from collections import OrderedDict
import numpy as np
import datetime
from datetime import timedelta
from bokeh.io import curdoc
from django.db import connection

curdoc().theme = 'dark_minimal'


# Create your views here.
def sqlquery():
    with connection.cursor() as cursor:
        cursor.execute(
            "select ass.name,m.module_code,m.level,ass.realease_date,ass.submission_date,ass.assignment_format from Assignments as ass, Modules as m where ass.submission_date between '2019-01-01 00:00:00' and '2019-12-31 23:59:00' and ass.assignment_format in ('MOLE quiz', 'Formal exam') and m.level in ('PGT','4') and m.module_code in ('COM6014','COM6012',' COM4525') and ass.module_id=m.module_id;")
        res = cursor.fetchall()
    return list(res)


def query(start_date, end_date, assig_format=[], modules=[], levels=[]):
    q = "select ass.name,m.module_code,m.level,ass.realease_date,ass.submission_date as date,ass.assignment_format from Assignments as ass, Modules as m where ass.submission_date between %s and %s "
    if len(assig_format) > 0:
        q += "and ass.assignment_format in ({}) ".format(",".join(["'" + x + "'" for x in assig_format]))
    if len(modules) > 0:
        q += "and m.module_code in ({}) ".format(",".join(["'" + x + "'" for x in modules]))
    if len(levels) > 0:
        q += "and m.level in ({}) ".format(",".join(["'" + x + "'" for x in levels]))
    q += "and ass.module_id=m.module_id"
    print(q)
    with connection.cursor() as cursor:
        cursor.execute(q, [start_date, end_date])
    data = list(cursor.fetchall())

    if len(data) == 0:
        # if the query is empty, return all

        start_date, end_date = "2018-01-01 00:00:00", "2019-12-31 23:59:00"
        q = "select ass.name,m.module_code,m.level,ass.realease_date,ass.submission_date as date,ass.assignment_format from Assignments as ass, Modules as m where ass.submission_date between %s and %s"
        with connection.cursor() as cursor:
            cursor.execute(q, [start_date, end_date])
        data = list(cursor.fetchall())

    df = pd.DataFrame(data=data, columns=["name", "module_code", "level", "release_date", "date", "assignment_format"])
    df = df[df["module_code"]!= 'COM6509']
    df = df[df["module_code"] != 'COM6012']
    df = df[df["module_code"] != 'COM4509']

    return df


def generate_charts(start_date, end_date, assig_format=[], modules=[], levels=[]):
    df = query(start_date, end_date, assig_format=assig_format, modules=modules, levels=levels)
    hscript, hdiv = generate_heatmap(df)
    tscript, tdiv = generate_timeline(df)
    return hscript, hdiv, tscript, tdiv


def generate_heatmap(df):
    title = '\"Heatmap\" Count of Assessments'
    # aggregate data
    df = df.groupby(['date']).count().reset_index().rename(index=str, columns={"name": "agg"})
    weeks, days, week, assignments, day_of_week, color = prepare_heatmap_data(df)
    p = heatmap(weeks, days, week, assignments, day_of_week, color, title)
    script, div = components(p)
    return script, div


def generate_timeline(df):
    df = prepare_data_timeline(df, max_items=25)
    p = timeline(df)
    script, div = components(p)
    return script, div


def prepare_heatmap_data(df):
    # parse to weeks and days
    df['day_of_week'] = [date.dayofweek for date in df["date"]]
    df['week'] = [(date - timedelta(days=date.dayofweek)).strftime("%Y-%m-%d") for date in df["date"]]
    # Pivot our data to get the matrix we need
    data = df.pivot(index='week', columns='day_of_week', values='agg')
    data = data.fillna(value=0)
    # Get our "weeks" and "days"
    weeks = list(data.index)
    days = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]
    # prepare lists for bokeh
    max_count = df["agg"].max()
    day_of_week = []
    week = []
    color = []
    assignments = []
    for w in weeks:
        for idx, day in enumerate(days):
            day_of_week.append(day)
            week.append(w)
            count = data.loc[w][idx] if idx in data.loc[w] else 0
            assignments.append(count)
            # 2ca25f
            # 44,162,95
            color.append(
                "#%02x%02x%02x" % (int(255 - (count / max_count) * 255), 255, int(255 - (count / max_count) * 255)))
    return (weeks, days, week, assignments, day_of_week, color)


def heatmap(weeks, days, week, assignments, day_of_week, color, title):
    # source
    source = ColumnDataSource(
        data=dict(
            day_of_week=day_of_week,
            week=week,
            color=color,
            assignments=assignments,
            w=[1] * len(assignments),
            h=[1] * len(assignments)
        )
    )

    p = figure(
        title=title,
        x_range=weeks,
        y_range=list(reversed(days)),
        tools="hover")
    p.plot_width = 900
    p.plot_height = 400
    p.rect(x="week", y="day_of_week", height="h", width="w", source=source, color="color", line_color=None)
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "10pt"
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = np.pi / 3
    p.toolbar.logo = None
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = OrderedDict([
        ('Assessments', '@assignments'),
    ])
    return p


def prepare_data_timeline(df, max_items=30):
    df['start'] = pd.to_datetime(df.release_date)
    df['end'] = pd.to_datetime(df.date)  # (df.submission_date)
    df["release_date"] = [str(s.date()) for s in df.start.tolist()]
    df["submission_date"] = [str(s.date()) for s in df.end.tolist()]
    df["color"] = ["mediumseagreen"] * len(df)
    df = df[df["end"] > df["start"]]
    df = df.sort_values(by="release_date", ascending=False).reset_index(drop=True).iloc[:max_items]
    df["uname"] = [n + " (" + str(i) + ")" for n, i in zip(df.name.tolist(), reversed(range(1, len(df) + 1)))]
    return df


def timeline(d):
    source = ColumnDataSource(d)
    p = figure(y_range=d.uname.tolist(), x_axis_type='datetime', x_range=Range1d(d.start.min(), d.end.max()),
               toolbar_location=None,
               title="Assessments Timeline")
    p.plot_width = 900
    p.plot_height = 600
    p.xaxis.major_label_orientation = np.pi / 3
    p.hbar(y="uname", left='start', right='end', height=0.4, source=source, color="color")
    p.ygrid.grid_line_color = None
    p.outline_line_color = None
    hover = HoverTool(tooltips="Task: @name<br>\
    Module: @module_code <br>\
    Start: @release_date<br>\
    End: @submission_date")
    p.add_tools(hover)
    return p









#
#
#
#
#
#
# curdoc().theme = 'dark_minimal'
# # Create your views here.
# def query(start_date,end_date,assig_type = None, modules = None, levels = None):
#     start_date, end_date = parse(start_date), parse(end_date)
#     all_assignments = models.Assignments.objects.filter(submission_date__range = [start_date, end_date]).only("name","submission_date","realease_date")
#     print("assig",len(all_assignments))
#     df_dict = []
#     for x in all_assignments:
#         if assig_type is not None:
#             for t in assig_type:
#                 if t in x.name.lower():
#                     df_dict.append({"date":x.submission_date, "name":x.name,"release_date":x.realease_date})
#                     break
#         else:
#             df_dict.append({"date":x.submission_date, "name":x.name, "release_date":x.realease_date})
#     # data to pandas
#     df = pd.DataFrame(df_dict)
#     print("dfass",df.head())
#     # modules
#     all_modules = models.Modules.objects.only("module_id","module_code","level")
#     print("modules",len(all_modules))
#     d = [{"module_code":m.module_code,"module_id":m.module_id,"level":m.level} for m in all_modules]
#     df = df.join(pd.DataFrame(d), lsuffix='_assig', rsuffix='_mods').reset_index()
#     if modules is not None:
#         df = df[df['module_code'].isin(modules)][["date","name","module_code"]]
#     if levels is not None:
#         df = df[df['level'].isin(levels)][["date","name","module_code"]]
#     df = df.reset_index(drop=True)
#     return df
#
# def generate_charts(start_date,end_date,assig_type = None, modules = None, levels = None):
#     df = query(start_date,end_date,assig_type = assig_type, modules = modules, levels = levels)
#     hscript,hdiv = generate_heatmap(df)
#     tscript,tdiv = generate_timeline(df)
#     return hscript,hdiv,tscript,tdiv
#
# def generate_heatmap(df):
#     title = '\"Heatmap\" Count of Assessments'
#     # aggregate data
#     print(df.head())
#     df = df.groupby(['date']).count().reset_index().rename(index=str, columns={"name":"agg"})
#     weeks,days,week,assignments,day_of_week,color = prepare_heatmap_data(df)
#     p = heatmap(weeks,days,week,assignments,day_of_week,color,title)
#     script, div = components(p)
#     return script, div
#
# def generate_timeline(df):
#     df = prepare_data_timeline(df,max_items = 25)
#     p = timeline(df)
#     script, div = components(p)
#     return script, div
#
# def prepare_heatmap_data(df):
#     # parse to weeks and days
#     df['day_of_week'] = [date.dayofweek for date in df["date"]]
#     df['week'] = [(date - timedelta(days=date.dayofweek)).strftime("%Y-%m-%d") for date in df["date"]]
#     # Pivot our data to get the matrix we need
#     data = df.pivot(index='week', columns='day_of_week', values='agg')
#     data = data.fillna(value=0)
#     # Get our "weeks" and "days"
#     weeks = list(data.index)
#     days = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]
#     # prepare lists for bokeh
#     max_count = df["agg"].max()
#     day_of_week = []
#     week = []
#     color = []
#     assignments = []
#     for w in weeks:
#         for idx, day in enumerate(days):
#             day_of_week.append(day)
#             week.append(w)
#             count = data.loc[w][idx] if idx in data.loc[w] else 0
#             assignments.append(count)
#             #2ca25f
#             #44,162,95
#             color.append("#%02x%02x%02x" % (int(255 - (count / max_count) * 255),255,int( 255 - (count / max_count) * 255)))
#     return (weeks,days,week,assignments,day_of_week,color)
#
# def heatmap(weeks,days,week,assignments,day_of_week,color,title):
#     # source
#     source = ColumnDataSource(
#         data=dict(
#             day_of_week=day_of_week,
#             week=week,
#             color=color,
#             assignments=assignments,
#             w = [1]*len(assignments),
#             h = [1]*len(assignments)
#         )
#     )
#
#     p = figure(
#         title=title,
#         x_range=weeks,
#         y_range=list(reversed(days)),
#         tools="hover")
#     p.plot_width=900
#     p.plot_height = 400
#     p.rect(x="week", y= "day_of_week",height = "h", width = "w", source = source,color="color", line_color=None)
#     p.grid.grid_line_color = None
#     p.axis.axis_line_color = None
#     p.axis.major_tick_line_color = None
#     p.axis.major_label_text_font_size = "10pt"
#     p.axis.major_label_standoff = 0
#     p.xaxis.major_label_orientation = np.pi/3
#     p.toolbar.logo = None
#     hover = p.select(dict(type=HoverTool))
#     hover.tooltips = OrderedDict([
#         ('Assessments', '@assignments'),
#     ])
#     return p
#
# def prepare_data_timeline(df,max_items = 30):
#     df['start'] = pd.to_datetime(df.release_date)
#     df['end'] = pd.to_datetime(df.date)#(df.submission_date)
#     df["release_date"] =  [str(s.date()) for s in df.start.tolist()]
#     df["submission_date"] = [str(s.date()) for s in df.end.tolist()]
#     df["color"] = ["mediumseagreen"]*len(df)
#     df = df[df["end"]>df["start"]]
#     df = df.sort_values(by ="release_date",ascending=False).reset_index(drop = True).iloc[:max_items]
#     df["uname"] = [n+ " ("+str(i)+")" for n,i in zip(df.name.tolist(),reversed(range(1,len(df)+1)))]
#     return df
#
# def timeline(d):
#     source = ColumnDataSource(d)
#     p = figure(y_range=d.uname.tolist(),x_axis_type='datetime', x_range=Range1d(d.start.min(),d.end.max()), toolbar_location=None,
#                title="Assessments Timeline")
#     p.plot_width=900
#     p.plot_height = 600
#     p.xaxis.major_label_orientation = np.pi/3
#     p.hbar(y="uname", left='start', right='end', height=0.4, source=source,color = "color")
#     p.ygrid.grid_line_color = None
#     p.outline_line_color = None
#     hover=HoverTool(tooltips="Task: @name<br>\
#     Module: @module_code <br>\
#     Start: @release_date<br>\
#     End: @submission_date")
#     p.add_tools(hover)
#     return p
