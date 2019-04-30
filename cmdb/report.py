




from django.template.loader import get_template
from django.db import connection
import pandas as pd

def generate_report(module_code):
    path = "report.html"
    template = get_template(path)
    data = list(query(module_code))
    df = pd.DataFrame(data, columns=['Module Code',"Academic",'Assignment',"Format","Percentage","Duration","Release Date","Due Date"])
    df["Release Date"] = df["Release Date"].dt.strftime('%m/%d/%Y')
    df["Due Date"] = df["Due Date"].dt.strftime('%m/%d/%Y')
    df = df.drop(["Module Code"],axis = 1)
    df["Assignment No."] = [i for i in range(1,len(df)+1)]
    df["Percentage"] = [x+"%" for x in df["Percentage"]]

    if len(df.Academic.unique()) == 1 and len(df.Duration.unique())==1:
        cols = ["Assignment No.", 'Assignment',"Format","Percentage","Release Date","Due Date"]
    else:
        cols = ["Assignment","Academic", "Duration","Format","Percentage","Release Date","Due Date"]


    sorted_df = df[cols]

    df_html = (
        sorted_df.style
        .set_properties(**{'font-size': '10pt', 'font-family': 'Calibri','text-align': 'center'})
        .hide_index()
        .render()
    )
    academics = ", ".join(df.Academic.unique())
    durations = ", ".join(df.Duration.unique())
    params = {"module_code":module_code,"academics":academics,"durations":durations,"assig_table":df_html}
    html = template.render(params)
    return html


def query(module_code):
    with connection.cursor() as cursor:
        cursor.execute("select m.module_code, a.name, ass.name, ass.assignment_format,ass.percentage,ass.duration,ass.realease_date, ass.submission_date from Modules as m, Assignments as ass, Academics as a where m.module_code= %s and m.module_id=ass.module_id and m.academic_id=a.academic_id", [module_code])
        res = cursor.fetchall()
    return res





















#
#
# def generate_report(module_code):
#     path = "report.html"
#     template = get_template(path)
#     data = list(query(module_code))
#     df = pd.DataFrame(data, columns=['Module Code',"Academic",'Assignment',"Format","Percentage","Duration","Release Date","Due Date"])
#     df["Release Date"] = df["Release Date"].dt.strftime('%m/%d/%Y')
#     df["Due Date"] = df["Due Date"].dt.strftime('%m/%d/%Y')
#     df = df.drop(["Module Code"],axis = 1)
#     df["Assignment No."] = [i for i in range(1,len(df)+1)]
#     df["Percentage"] = [x+"%" for x in df["Percentage"]]
#
#     if len(df.Academic.unique()) == 1 and len(df.Duration.unique())==1:
#         cols = ["Assignment No.", 'Assignment',"Format","Percentage","Release Date","Due Date"]
#     else:
#         cols = ["Assignment","Academic", "Duration","Format","Percentage","Release Date","Due Date"]
#
#
#     sorted_df = df[cols]
#
#     df_html = (
#         sorted_df.style
#         .set_properties(**{'font-size': '10pt', 'font-family': 'Calibri','text-align': 'center'})
#         .hide_index()
#         .render()
#     )
#     academics = ", ".join(df.Academic.unique())
#     durations = ", ".join(df.Duration.unique())
#     params = {"module_code":module_code,"academics":academics,"durations":durations,"assig_table":df_html}
#     html = template.render(params)
#     return html
#
#
# def query(module_code):
#     with connection.cursor() as cursor:
#         cursor.execute("select m.module_code, a.name, ass.name, ass.assignment_format,ass.percentage,ass.duration,ass.realease_date, ass.submission_date from Modules as m, Assignments as ass, Academics as a where m.module_code= %s and m.module_id=ass.module_id and m.academic_id=a.academic_id", [module_code])
#
#         res = cursor.fetchall()
#     return res
