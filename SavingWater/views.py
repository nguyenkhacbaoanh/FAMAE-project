from django.shortcuts import render
import dash
import dash_core_components as dcc 
import dash_html_components as html 
import plotly.graph_objs as go
import random
from django.conf import settings
from dash.dependencies import Input, Output

from django_plotly_dash import DjangoDash

import ast
import igraph as ig

import pandas as pd

with pd.ExcelFile(settings.BASE_DIR + "/SavingWater/Dataset_Aquastat.xlsx") as xlsx:
    aquastat = pd.read_excel(xlsx, "aquastat", header=0, nrows=181)
    food = pd.read_excel(xlsx, "food", header=0)
    #geo = pd.read_excel(xlsx,"geo",header=0)
    WS_c = pd.read_excel(xlsx,"WS-C",header=0)
    WS_a = pd.read_excel(xlsx,"WS-A",header=0)
    WS_b = pd.read_excel(xlsx,"WS-B",header=0)

# Create your views here.
def BaseView(request):

	return render(request, "index.html", {})
def consommation(request):
	return render(request, "consommation.html", {})
def limited_ressource(request):
	return render(request, "limited-ressource.html", {})
def alimentation(request):
	return render(request, "alimentation.html", {})
def water_stress(request):
	return render(request, "water-stress.html", {})
def DataNet(request):
	http = urllib3.PoolManager()
	r = http.request('GET', "https://raw.githubusercontent.com/plotly/datasets/master/miserables.json")
	data = json.loads(r.data.decode('utf-8'))
	N=len(data['nodes'])
	L=len(data['links'])
	Edges=[(data['links'][k]['source'], data['links'][k]['target']) for k in range(L)]
	G=ig.Graph(Edges, directed=False)
	labels=[]
	group=[]
	for node in data['nodes']:
	    labels.append(node['name'])
	    group.append(node['group'])
	layt=G.layout('kk', dim=3) 
	Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
	Yn=[layt[k][1] for k in range(N)]# y-coordinates
	Zn=[layt[k][2] for k in range(N)]# z-coordinates
	Xe=[]
	Ye=[]
	Ze=[]
	for e in Edges:
	    Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
	    Ye+=[layt[e[0]][1],layt[e[1]][1], None]  
	    Ze+=[layt[e[0]][2],layt[e[1]][2], None] 
	axis=dict(showbackground=False,
          showline=False,
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          ) 
	app = DjangoDash(name='NetWorkData')
	app.layout = html.Div(children=[
	    			dcc.Graph(
	    					id="graph",
	    					figure=go.Figure(
	    						data=[
	    							go.Scatter3d(
	    										x=Xe,
								               	y=Ye,
								               	z=Ze,
								               	mode='lines',
								               	line=dict(color='rgb(125,125,125)', width=1),
								               	hoverinfo='none'
	    								),
	    							go.Scatter3d(
	    										x=Xn,
												y=Yn,
												z=Zn,
												mode='markers',
												name='actors',
												marker=dict(symbol='diamond',
															 size=6,
															 color=group,
															 colorscale='Viridis',
															 line=dict(color='rgb(50,50,50)', width=0.5)
															 ),
												text=labels,
												hoverinfo='text'
												)
	    						],
	    						layout=go.Layout(
												title="Net Work Data(3D visualization)",
												#width=1200,
												#height=900,
												showlegend=False,
												scene=dict(
													xaxis=dict(axis),
													yaxis=dict(axis),
													zaxis=dict(axis),
													),
												margin=dict(
													t=50,
													),
												hovermode='closest',
												annotations=[
														dict(
														showarrow=False,
														text="Data source: <a href='http://bost.ocks.org/mike/miserables/miserables.json'>[1] miserables.json</a>",
														xref='paper',
														yref='paper',
														x=0,
														y=0.1,
														xanchor='left',
														yanchor='bottom',
														font=dict(
															size=14
															)
														)
												],)
	    					),
	    					style={"height":600, "width":1500}
	    				),
	    		])
	return render(request, "datanet.html", {})


def DataAli(request):
	# df_ali = pd.read_excel("/Users/nguyenkhacbaoanh/dev/school-HETIC/Project/FAMAE/SavingWater/alimentation.xlsx", header=0, usecols="A:D")
	# df_ali_groupbycat = food.groupby('Catégorie')['Water footprint (m3/ton)'].agg('sum')
	df = food[['Aliment (100g)','Water footprint (m3/ton)']].sort_values(by=['Water footprint (m3/ton)'])
	app_ali = DjangoDash(name='AlimentationData')
	app_ali.layout = html.Div(children=[
	    			dcc.Graph(
	    					id="graph",
	    					figure = go.Figure(
								data = [
									dict(
										type = 'bar',
										x=df['Water footprint (m3/ton)'].values,
										y=df['Aliment (100g)'].values,
										marker=dict(
											color='lightgreen',
											),
										orientation='h',
										hoverinfo='y+x',
										hoverlabel=dict(bgcolor='green', bordercolor='white'),
										),
									],
								layout = go.Layout(
									margin=dict(l=150,pad=50),
									yaxis=dict(automargin=True, domain=[0,1], side='right',),
									xaxis=dict(side='top', title='Waste Water m3/an',
											titlefont=dict(
											size=20,
											color='red'
											)),
									legend=dict(
										x=-0.7, 
										y=1, 
										bgcolor='#E2E2E2',
								        bordercolor='#FFFFFF',
								        borderwidth=2),
									)
								),
							style={"height":3500, "width":1000, "margin-left":100}
							
	    			)
	    		])
	return render(request, "dataali.html", {})


def ws_a_1(request):
	#df = pd.read_csv("/Users/nguyenkhacbaoanh/dev/school-HETIC/Project/FAMAE/SavingWater/dataset.csv")
	facecolor = ['rgba(123,24,247,0.5)', 'rgba(23,224,45,0.5)', 'rgba(13,34,97,0.5)', 'rgba(121,124,2,0.5)','rgba(101,124,207,0.5)', 'rgba(0,124,247,0.5)', 'rgba(121,124,0,0.5)', 'rgba(158,154,200,0.5)']
	app = DjangoDash(name='WaterWithdrawal')   # replaces dash.Dash

	app.layout = html.Div(children=[
	    			dcc.Graph(
	    					id="graph-with-check",
	    					style={"height":800, "width":1300},
	    					figure = go.Figure(
	    						data = [
										dict(
										type = 'choropleth',
										locationmode='country names',
										locations = WS_a['Name'],
										z = WS_a['Industrial'].values,
										zauto=False,
										zmin=0,
										zmax=5,
										text = list(WS_a['Name']),
										colorscale = 'Blues',
										autocolorscale = False,
										reversescale = True,
										marker = dict(
										    line = dict (
										        color = 'rgb(180,180,180)',
										        width = 0.5
										    ) ),
										colorbar = dict(
								            #autotick = False,
								            tickprefix = '',
								            title = 'Score'
								        	),
										),
	    							],
	    							layout = dict(
												title = 'Water Stress (Industrial)',
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
												),
										
	    						)
	    				),
	    		)])
	return render(request, "dataviz.html", {})
def ws_a_2(request):
	#df = pd.read_csv("/Users/nguyenkhacbaoanh/dev/school-HETIC/Project/FAMAE/SavingWater/dataset.csv")
	facecolor = ['rgba(123,24,247,0.5)', 'rgba(23,224,45,0.5)', 'rgba(13,34,97,0.5)', 'rgba(121,124,2,0.5)','rgba(101,124,207,0.5)', 'rgba(0,124,247,0.5)', 'rgba(121,124,0,0.5)', 'rgba(158,154,200,0.5)']
	app = DjangoDash(name='WaterWithdrawal')   # replaces dash.Dash

	app.layout = html.Div(children=[
	    			dcc.Graph(
	    					id="graph-with-check",
	    					style={"height":800, "width":1300},
	    					figure = go.Figure(
	    						data = [
										dict(
										type = 'choropleth',
										locationmode='country names',
										locations = WS_a['Name'],
										z = WS_a['All sectors'].values,
										zauto=False,
										zmin=0,
										zmax=5,
										text = list(WS_a['Name']),
										colorscale = 'Blues',
										autocolorscale = False,
										reversescale = True,
										marker = dict(
										    line = dict (
										        color = 'rgb(180,180,180)',
										        width = 0.5
										    ) ),
										colorbar = dict(
								            #autotick = False,
								            tickprefix = '',
								            title = 'Score'
								        	),
										),
	    							],
	    							layout = dict(
												title = 'Water Stress (All sectors)',
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
												),
										
	    						)
	    				),
	    		)])
	return render(request, "dataviz.html", {})
def ws_a_3(request):
	#df = pd.read_csv("/Users/nguyenkhacbaoanh/dev/school-HETIC/Project/FAMAE/SavingWater/dataset.csv")
	facecolor = ['rgba(123,24,247,0.5)', 'rgba(23,224,45,0.5)', 'rgba(13,34,97,0.5)', 'rgba(121,124,2,0.5)','rgba(101,124,207,0.5)', 'rgba(0,124,247,0.5)', 'rgba(121,124,0,0.5)', 'rgba(158,154,200,0.5)']
	app = DjangoDash(name='WaterWithdrawal')   # replaces dash.Dash

	app.layout = html.Div(children=[
	    			dcc.Graph(
	    					id="graph-with-check",
	    					style={"height":800, "width":1300},
	    					figure = go.Figure(
	    						data = [
										dict(
										type = 'choropleth',
										locationmode='country names',
										locations = WS_a['Name'],
										z = WS_a['Domestic'].values,
										zauto=False,
										zmin=0,
										zmax=5,
										text = list(WS_a['Name']),
										colorscale = 'Blues',
										autocolorscale = False,
										reversescale = True,
										marker = dict(
										    line = dict (
										        color = 'rgb(180,180,180)',
										        width = 0.5
										    ) ),
										colorbar = dict(
								            #autotick = False,
								            tickprefix = '',
								            title = 'Score'
								        	),
										),
	    							],
	    							layout = dict(
												title = 'Water Stress (Domestic)',
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
												),
										
	    						)
	    				),
	    		)])
	return render(request, "dataviz.html", {})
def ws_a_4(request):
	#df = pd.read_csv("/Users/nguyenkhacbaoanh/dev/school-HETIC/Project/FAMAE/SavingWater/dataset.csv")
	facecolor = ['rgba(123,24,247,0.5)', 'rgba(23,224,45,0.5)', 'rgba(13,34,97,0.5)', 'rgba(121,124,2,0.5)','rgba(101,124,207,0.5)', 'rgba(0,124,247,0.5)', 'rgba(121,124,0,0.5)', 'rgba(158,154,200,0.5)']
	app = DjangoDash(name='WaterWithdrawal')   # replaces dash.Dash

	app.layout = html.Div(children=[
	    			dcc.Graph(
	    					id="graph-with-check",
	    					style={"height":800, "width":1300},
	    					figure = go.Figure(
	    						data = [
										dict(
										type = 'choropleth',
										locationmode='country names',
										locations = WS_a['Name'],
										z = WS_a['Agricultural'].values,
										zauto=False,
										zmin=0,
										zmax=5,
										text = list(WS_a['Name']),
										colorscale = 'Blues',
										autocolorscale = False,
										reversescale = True,
										marker = dict(
										    line = dict (
										        color = 'rgb(180,180,180)',
										        width = 0.5
										    ) ),
										colorbar = dict(
								            #autotick = False,
								            tickprefix = '',
								            title = 'Score'
								        	),
										),
	    							],
	    							layout = dict(
												title = 'Water Stress (Agricultural)',
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
												),
										
	    						)
	    				),
	    		)])
	return render(request, "dataviz.html", {})
def pie_chart(request):
	app = DjangoDash(name='pie-chart-1')
	app.layout = html.Div(children=[
						dcc.Graph(
							figure = go.Figure(
								data = [
									dict(
										type = 'pie',
										labels = ['Agricultural water withdrawal',\
													'Industrial water withdrawal',\
													'Municipal water withdrawal'],
										values = [aquastat['Agricultural water withdrawal'].sum(), \
												aquastat['Industrial water withdrawal'].sum(), \
												aquastat['Municipal water withdrawal'].sum()],
										name = 'Les secteurs qui consomment le plus',
										text = ['Agricultural water withdrawal',\
													'Industrial water withdrawal',\
													'Municipal water withdrawal'],
										hoverinfo = 'text+value+percent',
										textinfo = 'label+percent',
										hole = 0.5,
										marker = dict(
												colors = ['#fac1b7','#a9bb95','#92d8d8']
											),
										domain = {"x": [0,0.6], 'y':[0.2, 0.8]}
										)
									],
								layout = go.Layout(
										#font = dict(color='#777777'),
										legend=dict(
												font=dict(color='#000000', size=15),
												orientation='h',
												#bgcolor='rgba(0,0,0,0)'
											)
									)
								),
							#style={"height":600, "width":1500}
							)
		])
	return render(request, "pie_chart_1.html", {})

def bar_chart_water_per_cap(request):
	df = aquastat[['Pays','Total water withdrawal per capita']].dropna().sort_values(by=['Total water withdrawal per capita'])
	app = DjangoDash(name='bar-chart-1')
	app.layout = html.Div(children=[
						dcc.Graph(
							figure = go.Figure(
								data = [
									dict(
										type = 'bar',
										x=df['Total water withdrawal per capita'].values,
										y=df['Pays'].values,
										orientation='h',
										#opacity = 0.8, 
									  	text = df['Total water withdrawal per capita'].astype(str).values + " m3/inhab/an", 
									  	textposition = 'outside',
									  	textfont = dict(color='green',size=15),
									  	hoverinfo='y+x',
									  	hoverlabel=dict(bgcolor='orange', bordercolor='white'),
									  	marker = dict(
									  		color=[i for i in range(len(df['Pays'].values))],
									  		colorscale='Blues', 
									  		reversescale=True
									  		)
										)
									],
								layout = go.Layout(
									margin=dict(l=150,pad=50),
									yaxis=dict(automargin=True, domain=[0,1], side='right',),
									xaxis=dict(
										side='top', 
										title='Total water withdrawal per capita (m3/inhab/an)',
										titlefont=dict(
											size=20,
											color='red'
											)
										),
									legend=dict(
										x=-0.7, 
										y=1, 
										bgcolor='#E2E2E2',
								        bordercolor='#FFFFFF',
								        borderwidth=2)
									)
								),
							style={"height":3500, "width":1100, "margin-left":100}
							)
		])
	return render(request, "bar_chart_1.html", {})

def bar_chart_water_municipal(request):
	df = aquastat[['Pays','Produced municipal wastewater','Direct use of treated municipal wastewater']].\
						fillna(0).\
						sort_values(by=['Produced municipal wastewater','Direct use of treated municipal wastewater'])
	df2 = aquastat[['Pays','Total water withdrawal','Total internal renewable water resources']].\
						fillna(0).\
						sort_values(by=['Total water withdrawal','Total internal renewable water resources'])
	app = DjangoDash(name='bar-chart-2')
	
	app.layout = html.Div(children=[
						dcc.Graph(
							figure = go.Figure(
								data = [
									dict(
										type = 'bar',
										x=df['Produced municipal wastewater'].values,
										y=df['Pays'].values,
										orientation='h',
										name='Produced municipal wastewater',
										hoverinfo='y+x',
										hoverlabel=dict(bgcolor='blue', bordercolor='white'),
										),
									dict(
										type = 'bar',
										x=df['Direct use of treated municipal wastewater'].values,
										y=df['Pays'].values,
										orientation='h',
										name='Direct use of treated municipal wastewater',
										hoverinfo='y+x',
										hoverlabel=dict(bgcolor='orange', bordercolor='white'),
										)
									],
								layout = go.Layout(
									margin=dict(l=150,pad=50),
									yaxis=dict(automargin=True, domain=[0,1], side='right',),
									xaxis=dict(side='top', title='Waste Water m3/an'),
									legend=dict(
										x=-0.7, 
										y=1, 
										bgcolor='#E2E2E2',
								        bordercolor='#FFFFFF',
								        borderwidth=2),
									)
								),
							style={"height":6000, "width":1100, "margin-left":100}
							)
		])
	return render(request, "bar_chart_2.html", {})

def map_irrigation_water(request):
	mapbox_access_token = 'pk.eyJ1IjoiYmFvYW5oIiwiYSI6ImNqcGllazNjdTAwaGQzcm9mb2N4eGRtb3kifQ.X28yqagleLs04WlO8YrZ-g'
	facecolor = ['rgba(123,24,247,0.5)', 'rgba(23,224,45,0.5)', 'rgba(13,34,97,0.5)', 'rgba(121,124,2,0.5)','rgba(101,124,207,0.5)', 'rgba(0,124,247,0.5)', 'rgba(121,124,0,0.5)', 'rgba(158,154,200,0.5)']
	external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"]
	external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.js']
	app = DjangoDash(name='IrrigationWater',external_stylesheets=external_css, external_scripts=external_js)
	
	app.layout = html.Div(children=[
					dcc.Dropdown(
						id='data_to_viz',
		    			options=[{'label': c, 'value': c} for c in ['Area equipped for full control irrigation: total',\
		    													'Total population with access to safe drinking-water',\
		    													'Long-term average annual precipitation in volume',
		    													'Groundwater produced internally']],
		    			value=[],
		    			multi=True
		    		),
	    			html.Div(children=html.Div(id='graph-map'), className='row'),
	    		])
	@app.callback(Output('graph-map', 'children'),[Input('data_to_viz','value')])
	def graph_update(data_names):
		graphs = []
		class_choice = 'col s12'

		for data_name in data_names:
			data = dict(
						type = 'scattermapbox',
				        lat = aquastat["latitude"],
				        lon = aquastat["longitude"],
				        mode = "markers",
				        marker = dict(
				            size = aquastat[data_name]\
				            		.fillna(min(aquastat[data_name])),
				            sizeref = 2.*max(aquastat[data_name])/(100**2),
				            sizemode='area',
				            colorscale='Blues',
				            opacity=0.5,
				        ),
				        text = aquastat['Pays'] +"\n"+\
				        		 [ str(i) for i in aquastat[data_name]],
				        #geo = "geo"
				    )

			graphs.append(html.Div(dcc.Graph(
			    id=data_name,
			    #animate=True,
			    figure={'data': [data],'layout' : dict(
													title = data_name,
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
													),
													mapbox=dict(
												        accesstoken=mapbox_access_token,
												        bearing=0,
												        pitch=0,
												        zoom=1,
												        center=dict(
													            lat=4.469936,
													            lon=50.503887
													        ),
												        style='light',
												        layers=[
												            dict(
												                sourcetype = 'geojson',
												                source = 'https://raw.githubusercontent.com/supig/FAMAE-project/master/South%20America.json',
												                type = 'fill',
												                color = facecolor[0],
												                opacity=0.3
												            ),
												            dict(
												                sourcetype = 'geojson',
												                source = 'https://raw.githubusercontent.com/supig/FAMAE-project/master/Africa.json',
												                type = 'fill',
												                color = facecolor[1],
												                opacity=0.3
												            ),
												            dict(
												                sourcetype = 'geojson',
												                source = 'https://raw.githubusercontent.com/supig/FAMAE-project/master/Oceania.json',
												                type = 'fill',
												                color = facecolor[2],
												                opacity=0.3
												            ),
												            dict(
												                sourcetype = 'geojson',
												                source = 'https://raw.githubusercontent.com/supig/FAMAE-project/master/Asia.json',
												                type = 'fill',
												                color = facecolor[3],
												                opacity=0.3
												            ),
												            dict(
												                sourcetype = 'geojson',
												                source = 'https://raw.githubusercontent.com/supig/FAMAE-project/master/Europe.json',
												                type = 'fill',
												                color = facecolor[4],
												                opacity=0.3
												            ),
												            dict(
												                sourcetype = 'geojson',
												                source = 'https://raw.githubusercontent.com/supig/FAMAE-project/master/North%20America.json',
												                type = 'fill',
												                color = facecolor[5],
												                opacity=0.3
												            ),
												            ],
							             
										
												    ),
												    updatemenus=list([
																    dict(
																        buttons=list([   
																            dict(
																                args=[{
																                	'mapbox.zoom': 3,
																                	'mapbox.center.lat': '29.8405555556',
																                	'mapbox.center.lon': '89.2966666667',
							                                    					'mapbox.bearing': 0,
																                	}],
																                #args=[{'type':'choropleth'}],
																                label='Asia',
																                method='relayout'
																            ),
																            dict(
																                args=[{
																                	'mapbox.zoom': 3,
																                	'mapbox.center.lon': '9.14055555556',
																                	'mapbox.center.lat': '48.6908333333',
							                                    					'mapbox.bearing': 0,
																                	}],
																                #args=[{'type':'scattermapbox'}],
																                label='Europe',
																                method='relayout'
																            ),
																            dict(
																                args=[{
																                	'mapbox.zoom': 3,
																                	'mapbox.center.lon': '138.515555556',
																                	'mapbox.center.lat': '-18.3127777778',
							                                    					'mapbox.bearing': 0,
																                	}],
																                #args=[{'type':'scattermapbox'}],
																                label='Oceania',
																                method='relayout'
																            ),
																            dict(
																                args=[{
																                	'mapbox.zoom': 3,
																                	'mapbox.center.lon': '21.0936111111',
																                	'mapbox.center.lat': '7.18805555556',
							                                    					'mapbox.bearing': 0,
																                	}],
																                #args=[{'type':'scattermapbox'}],
																                label='Africa',
																                method='relayout'
																            ),
																            dict(
																                args=[{
																                	'mapbox.zoom': 3,
																                	'mapbox.center.lon': '-83.753428',
																                	'mapbox.center.lat': '9.748917',
							                                    					'mapbox.bearing': 0,
																                	}],
																                #args=[{'type':'scattermapbox'}],
																                label='America',
																                method='relayout'
																            ),
																            dict(
																                args=[{
																                	'mapbox.zoom': 1,
																                	'mapbox.center.lon': '50.503887',
																                	'mapbox.center.lat': '4.469936',
							                                    					'mapbox.bearing': 0,
																                	}],
																                #args=[{'type':'scattermapbox'}],
																                label='World',
																                method='relayout'
																            ),   
																        ]),
																        direction="down",
													                    pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
													                    showactive=False,
													                    bgcolor="rgb(50, 100, 48, 0)",
													                    type='buttons',
													                    yanchor='bottom',
													                    xanchor='left',
													                    font=dict(
													                        color="#FFF0FF"
													                    ),
													                    x=0,
													                    y=0.05 
																    ),
													])
												)},
				style={"height":800, "width":1300}
			    ), className=class_choice))
		return graphs
	return render(request, 'map_1.html', {})

def bar_chart_water_com_renou(request):
	df = aquastat[['Pays','Total water withdrawal','Total internal renewable water resources']].\
						fillna(0).\
						sort_values(by=['Total internal renewable water resources','Total water withdrawal'])
	app = DjangoDash(name='bar-chart-3')
	
	app.layout = html.Div(children=[
						dcc.Graph(
							figure = go.Figure(
								data = [
									dict(
										type = 'bar',
										x=df['Total water withdrawal'].values,
										y=df['Pays'].values,
										orientation='h',
										name='Total water withdrawal',
										hoverinfo='y+x',
										hoverlabel=dict(bgcolor='blue', bordercolor='white'),
										),
									dict(
										type = 'bar',
										x=df['Total internal renewable water resources'].values,
										y=df['Pays'].values,
										orientation='h',
										name='Total internal renewable water resources',
										hoverinfo='y+x',
										hoverlabel=dict(bgcolor='orange', bordercolor='white'),
										)
									],
								layout = go.Layout(
									margin=dict(l=150,pad=50),
									yaxis=dict(automargin=True, domain=[0,1], side='right',),
									xaxis=dict(side='top', title='Waste Water m3/an'),
									legend=dict(
										x=-0.7, 
										y=1, 
										bgcolor='#E2E2E2',
								        bordercolor='#FFFFFF',
								        borderwidth=2),
									)
								),
							style={"height":6000, "width":1100, "margin-left":100}
							)
		])
	return render(request, "bar_chart_3.html", {})
