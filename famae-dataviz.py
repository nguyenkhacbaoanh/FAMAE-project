import dash
import dash_core_components as dcc 
import dash_html_components as html 
import plotly.graph_objs as go
import json
import numpy as np
from dash.dependencies import Input, Output, Event
# importation data
with open("ftp-volume-deau-facture-par-commune.geojson.json") as f:
	data = json.load(f)
geoshape = data
latitude = []
longtitude = []
volume_facture_eau = []
commune = []
for i in range(len(geoshape['features'])):
	try:
		latitude.append(geoshape['features'][i]['properties']['geo'][0])
		longtitude.append(geoshape['features'][i]['properties']['geo'][1])
		volume_facture_eau.append(geoshape['features'][i]['properties']['volume_facture_eau_m3'])
		commune.append(geoshape['features'][i]['properties']['commune'])
	except:
		continue

#token key for mapbox
mapbox_access_token = 'pk.eyJ1IjoiYmFvYW5oIiwiYSI6ImNqcGllazNjdTAwaGQzcm9mb2N4eGRtb3kifQ.X28yqagleLs04WlO8YrZ-g'

#css design:
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#start app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
							html.H1(children="FAMAE Projet"),
							dcc.Tabs(id="tabs", value='tab-1', children=[
						        dcc.Tab(label='Volume facturé d\'eau', value='tab-1', children=[
																				            dcc.Graph(
																								id='volume',
																								figure=go.Figure(
																										data = [
																										    go.Scattermapbox(
																										        lat = list(latitude),
																										        lon = list(longtitude),
																										        mode = "markers",
																										        marker = dict(
																										            size = volume_facture_eau,
																										            sizeref = 2.*max(volume_facture_eau)/(100**2),
																										            sizemode='area',
																										            color='red',
																										            opacity=0.5,
																										        ),
																										        #text = [str(i) + "-- facturé: " + str(j) for ix, (i,j) in enumerate(commune,volume_facture_eau)],
																										        #geo = "geo"
																										    ),
																										],

																										layout = go.Layout(
																										    autosize=True,
																										    hovermode='closest',
																										    mapbox=dict(
																										        accesstoken=mapbox_access_token,
																										        bearing=0,
																										        center=dict(
																										            lat=50.633333,
																										            lon=3.066667
																										        ),
																										        pitch=0,
																										        zoom=10,
																										        # layers=[
																										        #     dict(
																										        #         sourcetype = 'geojson',
																										        #         source = geoshape,
																										        #         type = 'fill',
																										        #         color = 'rgba(163,22,19,0.8)',
																										        #         opacity=0.3
																										        #     ),
																										        # ]
																										    ),
																										),
																									),
																								style={'height':700, 'width':1300}
																								)
																							]),

						        dcc.Tab(label='Pyramid-nourriture', value='tab-2', children=[
																							dcc.Graph(
																								id='pyramid',
																								figure=go.Figure(
																										data = [go.Scatter(
																										    #y=[8.25, 6.75, 5.15, 3.55, 2],
																										    #x=[3, 3, 3, 3, 3],
																										    #text=['Cat 1', 'Cat 2', 'Cat 3', 'Cat 4', 'Cat 5'],
																										    #mode='text',
																											),],
																										layout = {
																										    'xaxis': {
																										        'range': [0, 7]
																										    },
																										    'yaxis': {
																										        'range': [0, 10]
																										    },
																										    'shapes': [
																										        # Line Diagonal
																										        {
																										            'type': 'line',
																										            'x0': 1.5,
																										            'y0': 10,
																										            'x1': 2,
																										            'y1': 0,
																										            'line': {
																										                'color': 'rgb(128, 0, 128)',
																										                'width': 4,
																										                'dash': 'dashdot',
																										            },
																										        },
																										        # Line Horizontal
																										        {
																										            'type': 'line',
																										            'x0': 2,
																										            'y0': 0.15,
																										            'x1': 4,
																										            'y1': 0.15,
																										            'line': {
																										                'color': 'rgb(128, 0, 128)',
																										                'width': 4,
																										                'dash': 'dashdot',
																										            },
																										        },
																										        # Line Diagonal
																										        {
																										            'type': 'line',
																										            'x0': 4,
																										            'y0': 0,
																										            'x1': 4.5,
																										            'y1': 10,
																										            'line': {
																										                'color': 'rgb(128, 0, 128)',
																										                'width': 4,
																										                'dash': 'dashdot',
																										            },
																										        },
																										        # etage line horizontal
																										        # Line Horizontal
																										        # {
																										        #     'type': 'line',
																										        #     'x0': 2,
																										        #     'y0': 7.75,
																										        #     'x1': 3.45,
																										        #     'y1': 7.75,
																										        #     'line': {
																										        #         'color': 'rgb(50, 171, 96)',
																										        #         'width': 4,
																										        #         'dash': 'dashdot',
																										        #     },
																										        # },
																										        
																										    ]
																										}
																									),
																								style={"height":700, "width":1300}
																								),
																							
																							]),

						        dcc.Tab(id = 'graph-3', label='L\'eau - quantité de plat', value='tab-3',
																						        	children=[
																							    			dcc.Graph(
																							    					id="graph-with-slider",
																							    					figure=go.Figure(
																							    						
																							    					),
																							    					style={"height":600, "width":1200},
																							    					#animate=True
																							    				),
																							    			dcc.Slider(
																										        id='eau-slider',
																										        min=0,
																										        max=8,
																										        step=0.1,
																										        value=0,
																										        marks={f"{i:.1f}": f"{i:.1f}" for i in np.arange(0.,8.,0.5)}
																										    )
																							    		]),
						        dcc.Tab(id='graph-4', label='Live Graph', value='tab-4', 
						        														children=[
						        															dcc.Graph(
						        																id='live-graph',
						        																figure=go.Figure(),
						        																
						        																),
						        															dcc.Interval(
						        																id='graph-update',
						        																interval=1*1000
						        																),
						        														]),
														
						])
					]
					)
# for graph-2:
@app.callback(Output('pyramid', 'figure'), [])
def update_figure():
	return {
			
		}

# for graph-3
x0 = np.random.normal(2, 0.45, 300)
y0 = np.random.normal(2, 0.45, 300)

x1 = np.random.normal(6, 0.4, 200)
y1 = np.random.normal(6, 0.4, 200)

x2 = np.random.normal(4, 0.3, 200)
y2 = np.random.normal(4, 0.3, 200)
@app.callback(Output('graph-with-slider', 'figure'),[Input('eau-slider', 'value')])
def update_figure(selected_water):
	ix0 = [True if i <= selected_water else False for i in x0 ]
	ix1 = [True if i <= selected_water else False for i in x1 ]
	ix2 = [True if i <= selected_water else False for i in x2 ]
	#print(len(ix))
	x0_new = x0[ix0]
	y0_new = y0[ix0]
	x1_new = x1[ix1]
	y1_new = y1[ix1]
	x2_new = x2[ix2]
	y2_new = y2[ix2]
	return {
				'data' : [
					go.Scatter(
					    x=x0_new,
					    y=y0_new,
					    mode='markers',
					),
					go.Scatter(
					    x=x1_new,
					    y=y1_new,
					    mode='markers',
					),
					go.Scatter(
					    x=x2_new,
					    y=y2_new,
					    mode='markers',
					),
					go.Scatter(
					    x=x1_new,
					    y=y0_new,
					    mode='markers',
					),
					go.Scatter(
					    x=x2_new,
					    y=y1_new,
					    mode='markers',
					)
				],
				'layout' : go.Layout(
						    xaxis = dict(
						    	title='niveau d\'eau(en lit)',
						    	range=[0, 8]
						    	),
						    yaxis = dict(
						    	title='quantité de la nourriture (en kg)',
						    	range=[0, 8]
						    	),
						    showlegend = True
						)
			}
# for graph-4
from collections import deque
X = deque(maxlen=100)
X.append(1)
Y = deque(maxlen=100)
Y.append(0)
Y1 = deque(maxlen=100)
Y1.append(0)
@app.callback(Output('live-graph', 'figure'),events=[Event('graph-update', 'interval')])
def update_graph_scatter():
	X.append(X[-1] + 1)
	Y.append(Y[-1] +  np.random.uniform(-1/2, 1/2))
	Y1.append(Y[-1] +  np.random.uniform(-1, 1))
	return {
			'data': [go.Scatter(
								x = list(X),
								y = list(Y),
								#mode = "markers+lines",
								marker = dict(
										color='green'
									)
							),
					go.Scatter(
								x = list(X),
								y = list(Y1),
								mode = "markers+lines",
								marker = dict(
										color='red'
									)
							)
			],
			'layout': go.Layout(
					xaxis = dict(range=[min(X),max(X)]),
					yaxis = dict(range=[min(Y1),max(Y1)])
				)
	}

if __name__ == "__main__":
	app.run_server(debug=True, host='localhost', port=1234)