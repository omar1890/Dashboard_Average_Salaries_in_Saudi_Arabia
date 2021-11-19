import pandas as pd 
import numpy as np
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output,State
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("Salary by Education.csv")
df['Year'] = df['Year Quarter'].str.slice(0, 4)

total_salary = go.Figure(go.Indicator(
    mode = "number",
    value = df['Salary'].sum(),
    title = {"text": "Total Salary"},
    domain = {'row': 0, 'column': 0}))

total_saudi = go.Figure(go.Indicator(
    mode = "number",
    value = len(df[df['Nationality']=='Saudi']),
    title = {"text": "Total Saudi"},
    domain = {'row': 0, 'column': 0}))

total_female = go.Figure(go.Indicator(
    mode = "number",
    value = len(df[df['Gender']=='Female']),
    title = {"text": "Total Female"},
    domain = {'row': 0, 'column': 0}))

total_degree_level = go.Figure(go.Indicator(
    mode = "number",
    value = len(df[df['Degree Level']=='Doctorate']),
    title = {"text": "Total Doctorate Degree"},
    domain = {'row': 0, 'column': 0}))


#pie charts
degree_level_pie_char = px.pie(df,names='Degree Level',color_discrete_sequence=px.colors.sequential.Turbo)

degree_level_pie_char.update_layout(
    title_x=0.5,
    title_font_color='rgb(42, 1, 52)',
    margin=dict(l=0, r=0, t=60, b=110),
    font=dict(
        family="Courier New, monospace",
        size=18,
    ))

year_quarter_pie_char = px.pie(df,names='Year Quarter',color_discrete_sequence=px.colors.sequential.Turbo)

year_quarter_pie_char.update_layout(
    title_x=0.5,
    title_font_color='rgb(42, 1, 52)',
    margin=dict(l=0, r=0, t=60, b=110),
    font=dict(
        family="Courier New, monospace",
        size=18,
    ))

nationality_pie_char = px.pie(df,names='Nationality',color_discrete_sequence=px.colors.sequential.Turbo)

nationality_pie_char.update_layout(
    title_x=0.5,
    title_font_color='rgb(42, 1, 52)',
    margin=dict(l=0, r=0, t=60, b=110),
    font=dict(
        family="Courier New, monospace",
        size=18,
    ))

fig1 = px.scatter(df,x="Year", y="Salary",color="Degree Level", symbol="Degree Level",hover_data=['Gender'])
fig2 = px.scatter(df, x="Salary", y="Degree Level", color="Gender", facet_col="Gender", facet_row="Nationality")
fig3 = px.bar(df,x='Degree Level',y='Salary',color="Gender",barmode="group",hover_data=['Nationality'])

# Create a dash application
app=dash.Dash("Dashboard", external_stylesheets =['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server
app.layout=html.Div([
                         html.H1('Average Salaries in Saudi Arabia Between 2017-2021',style={'color':'white','padding':'5px',"border":"2px black solid",'text-align':'center', 'font-size':85 ,'background':'#006C35'})
     ,html.Hr(style={'size':'50px'}),
    
    #Indicators
    html.Div([
        
        html.Div([
            dcc.Graph(figure= total_salary),
        ],className='four columns'), 
        
        
        html.Div([
            dcc.Graph(figure= total_female),
        ],className='four columns'),        
        
        
        html.Div([
            dcc.Graph(figure= total_degree_level),
        ],className='four columns'),
      
    ],style={'size':'100px'}),

    html.Div([

    #pie charts
    html.Div([
        html.H1('Degree Level Percentage',style={"border":"2px black solid",'color':'white','text-align':'center', 'font-size':30 ,'background':'#006C35'}),
        dcc.Graph(figure= degree_level_pie_char),
    ],className='four columns'),  

    html.Div([
        html.H1('Saudi vs Non-Saudi Percentage',style={'padding':'3px',"border":"2px black solid",'color':'white','text-align':'center', 'font-size':30 ,'background':'#006C35'}),
        dcc.Graph(figure= nationality_pie_char),
    ],className='four columns'),  

    html.Div([
        html.H1('Year Quarter Percentage',style={'padding':'3px',"border":"2px black solid",'color':'white','text-align':'center', 'font-size':30 ,'background':'#006C35'}),
        dcc.Graph(figure= year_quarter_pie_char),
    ],className='four columns'),  
    ]),

    html.Br(),
    html.Div(children=[html.H1('Degree Level vs Salary',style={'padding':'3px',"border":"2px black solid",'color':'white','text-align':'center', 'font-size':30 ,'background':'#006C35'}),
            dcc.Graph(figure=fig3)
], className="sex columns"),
  
    html.Br(),
    html.Div(children=[html.H1('Year vs Salary',style={'padding':'3px',"border":"2px black solid",'color':'white','text-align':'center', 'font-size':30 ,'background':'#006C35'}),
                 dcc.Dropdown(id='demo-dropdown1',style=dict(width='220px',size='100px'),options=[
                {'label': '--', 'value': 'No'},
                {'label': 'Female', 'value': 'Female'},
                {'label': 'Male', 'value': 'Male'}
                ],value= 'Response'),html.Button('Submit',id='submit_val1', n_clicks=0,style=dict(width='220px',size='100px')),
                dcc.Graph( id='mygraph1',figure={} )
    ], className="sex columns"),
    html.Br(), 
    html.Div(children=[ html.H1('Salary vs Degree Level',style={'padding':'3px',"border":"2px black solid",'color':'white','text-align':'center', 'font-size':30 ,'background':'#006C35'}),
                dcc.Graph(figure=fig2)
    ], className="sex columns"),
    html.Br(),
    html.Br()

])

@app.callback(
    
Output(component_id='mygraph1',component_property='figure'),
State(component_id='demo-dropdown1',component_property='value'),
Input(component_id='submit_val1',component_property='n_clicks')
)


def update_My_Div(gender,n_clicks):
    if gender=='No':
        print("here")   
        fig1 = px.scatter(df,x="Year", y="Salary",color="Degree Level", symbol="Degree Level",hover_data=['Gender']) 
    else :
        df1= df[df['Gender'] == str(gender)]
        fig1 = px.scatter(df1,x="Year", y="Salary",color="Degree Level", symbol="Degree Level",hover_data=['Gender']) 
    
    fig1.update_layout(
    title_font_color='rgb(42, 1, 52)',
    title_x=0.4,
    xaxis_title="Year",
    yaxis_title="Salary",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
        ))
        

    return fig1

# # Run the app
# if __name__ == '__main__':
#     app.run_server()