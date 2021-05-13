#!/usr/bin/env python
# coding: utf-8

# In[5]:


#!/usr/bin/env python
# coding: utf-8

# In[145]:


import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html 
import plotly.express as px
import plotly.graph_objects as go
import dash_table
# from jupyter_dash import JupyterDash
import dash_labs as dl

# df = pd.read_excel('/home/alex/source/backup/df_source+personal_工号_merge.xlsx', index_col=0)


# In[6]:


# Choose the app's layout template ***************************************
# Templates list: FlatDiv, HtmlCard, DbcCard, DbcRow, DbcSidebar, DbcSidebarTabs, 
#  https://github.com/plotly/dash-labs/blob/main/docs/04-PredefinedTemplates.md
tpl = dl.templates.DbcSidebar(
#     tab_roles=['graph1', 'graph2'],
    title="Dash App Demo",
    sidebar_columns=3,
    theme=dbc.themes.COSMO,     # change theme: https://hellodash.pythonanywhere.com/dash_labs
    figure_template=True,       # aligns plotly.py figure template with bootstrap theme
)

app = dash.Dash(__name__, plugins=[dl.plugins.FlexibleCallbacks()])
server = app.server

df = px.data.gapminder()
print(df.head())


# Create the app components **********************************************
dropdown = dcc.Dropdown(
    options=[{"label": str(i), "value": i} for i in ["gdpPercap", "lifeExp", "pop"]],
    value="gdpPercap",
    clearable=False,
)

checklist = dbc.Checklist(
    options=[{"label": i, "value": i} for i in df.continent.unique()],
    value=df.continent.unique()[1:],
    inline=True,
)

yrs = df.year.unique()
range_slider = dcc.RangeSlider(
    min=yrs[0],
    max=yrs[-1],
    step=2,
    marks={int(i): str(i) for i in [1952, 1962, 1972, 1982, 1992, 2007]},
    value=[1982, yrs[-1]],
)


# Create interaction between app components ******************************
@app.callback(
    
#     tpl.div_output( role='graph1'),
#     tpl.div_output( role='graph2'),
    
    dl.Input(dropdown, label="Select indicator (y-axis)"),
    dl.Input(checklist, label="Select continents"),
    dl.Input(range_slider, label="Select time period"),
    
    
    template=tpl,
)
def update_charts(indicator, continents, years):
    if continents == []:
        return {}

    dff = df[df.year.between(years[0], years[1])]
    dff = dff[dff.continent.isin(continents)]
    line_fig = px.line(
        dff,
        x="year",
        y=indicator,
        color="continent",
        line_group="country",
        title=indicator + " from %.0f to %.0f" % (years[0], years[1]),
    )

    dff = dff[dff.year == years[1]]

    hist_fig = px.histogram(
        dff, x="lifeExp", nbins=10, title=f"Life Expectancy {years[1]}")

#     return [dcc.Graph(figure=line_fig), dcc.Graph(figure=hist_fig)]
    return dbc.Row([ dbc.Col(dcc.Graph(figure=line_fig)), 
                    dbc.Col(dcc.Graph(figure=hist_fig)),
                   ])
app.layout = tpl.layout(app)


if __name__ == "__main__":
#    app.run_server(mode = 'jupyterlab', debug=True)
    app.run_server( debug=True)  

