import dash
import dash_core_components as dcc 
import dash_html_components as html 
import plotly.graph_objs as go

from dash.dependencies import Input, Output

from django_plotly_dash import DjangoDash

import pandas as pd


df = pd.read_csv("/Users/nguyenkhacbaoanh/dev/school-HETIC/Project/FAMAE/SavingWater/dataset.csv")

app = DjangoDash(name='WaterWithdrawal')   # replaces dash.Dash

app.layout = html.Div(children=[
				dcc.Checklist(
					id='check',
				    options=[
				        {'label': 'Agricultural', 'value': 'Agricultural water withdrawal (10^9 m3/year)'},
				        {'label': 'Industriel', 'value': 'Industrial water withdrawal (10^9 m3/year)'},
				        {'label': 'Municipal', 'value': 'Municipal water withdrawal (10^9 m3/year)'}
				    ],
				    values=[]
				),
    			dcc.Graph(
    					id="graph-with-check",
    					figure=go.Figure(
    						
    					),
    					#style={"height":900, "width":1200}
    				),
    		])
@app.callback(Output("graph-with-check",'figure'),[Input('check', 'values')])
def update_graph(option):
	print(option)
	return	{'data' : [ dict(
					type = 'choropleth',
					locations = df['codes'],
					z = df[option].sum(axis=1),
					zauto=False,
					zmin=0,
					zmax=800,
					text = list(df['Pays']),
					colorscale = [[0.0, 'rgb(242,240,247)'],[0.25, 'rgb(188,189,220)'],\
        [0.5, 'rgb(158,154,200)'],[0.75, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']],
					autocolorscale = False,
					reversescale = False,
					marker = dict(
					    line = dict (
					        color = 'rgb(180,180,180)',
					        width = 0.5
					    ) ),
					colorbar = dict(
			            autotick = False,
			            tickprefix = '',
			            title = 'Eau'
			        ),
				) ],
	
				'layout' : dict(
					title = 'Water using for agricultural',
					#width=1200,
					#height=800,
					hovermode='closest',
					#margin=dict(l=50,t=50,r=-20,b=0),
					geo = dict(
					showframe = False,
					showcoastlines = False,
					projection = dict(
					    type = 'mercator'
						)
					)
				)}
df_ali = pd.read_excel("/Users/nguyenkhacbaoanh/dev/school-HETIC/Project/FAMAE/SavingWater/alimentation.xlsx", header=0, usecols="A:D")
df_ali_groupbycat = df_ali.groupby('Catégorie')['Water footprint (m3/ton)'].agg('sum')
app_ali = DjangoDash(name='AlimentationData')
app_ali.layout = html.Div(children=[
    			dcc.Graph(
    					id="graph",
    					figure=go.Figure(
    						data = [
    							go.Bar(
    									x = df_ali_groupbycat.index,
    									y = df_ali_groupbycat.values,
    									marker = dict(cauto=True, color=['red','yellow','green','blue','black'], opacity=0.4)
    								)
    						],
    						layout = go.Layout(
    								xaxis = dict(
    										title="Catégorie"
    									),
    								yaxis = dict(
    										title="Niveau d'eau consommé"
    									)
    							)
    					)
    			)
    		])