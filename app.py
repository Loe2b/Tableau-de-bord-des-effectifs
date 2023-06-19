from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

#Initialisation de la page et des datas
app = Dash(__name__)

#Associe les campus à leur Coordonées pour les afficher sur la carte
df_Campus = pd.read_csv('Data/Campus.csv')

df = pd.read_csv('Data/new_data.csv')
df = df.astype({'Sexe': 'string', 'Domaine': 'string', 'Type de poste': 'string', 'Campus': 'string'})

#Annees dans l'ordre
order = df['Annee de recrutement'].unique()
order[::-1].sort()

app.layout = html.Div(style={'padding':'3%'}, children=[
	
    #Header
	html.Div(className="app-header", children=[
        html.H1('Tableau de bord des Effectifs')]),
	    
    #Tous les filtres
    html.Div(className='padding', children=[

            html.Div(className='content-box', children=[
                html.Div(className='padding', children=[dcc.Dropdown(
                    order,
                    placeholder="Selectionner une année (2023)",
                    id='annee--dropdown',
                    value=None
                    )], style={'width': '20%', 'display': 'inline-block'}),

                html.Div(className='padding', children=[dcc.Dropdown(
                    df['Campus'].unique(),
                    placeholder="Selectionner un Campus",
                    id='campus--dropdown',
                    value=None
                    )], style={'width': '20%', 'display': 'inline-block'}),

                html.Div(className='padding', children=[dcc.Dropdown(
                    df['Domaine'].unique(),
                    placeholder="Selectionner un Domaine",
                    id='domaine--dropdown',
                    value=None
                    )], style={'width': '20%', 'display': 'inline-block'}),

                html.Div(className='padding', children=[dcc.Dropdown(
                    df['Type de poste'].unique(),
                    placeholder="Selectionner un type de poste",
                    id='type--dropdown',
                    value=None
                    )], style={'width': '20%', 'display': 'inline-block'})

                ]),

            #Pour changer entre Employés et Recrutement
            html.Div(style={'background-color' :'#1e2130'},children =[
                dcc.Tabs(id='tabs', value='Employés',
                         parent_className='custom-tabs',
                         className='custom-tabs-container',
                         children=[
                            dcc.Tab(label='Employés', value='Employés', className='custom-tab', selected_className='custom-tab--selected'),
                            dcc.Tab(label='Recrutement', value='Recrutements', className='custom-tab', selected_className='custom-tab--selected')
                    ])
                ])
                
            ]),
   

        #Tous les graphes, cartes et courbes

        html.Div(className='padding', children=[
            html.Div(className='content-box', children=[
                dcc.Graph(id='map')], style={'margin-bottom': '10px', 'margin-top': '-16px'}),

            html.Div(className='content-box', children=[
                dcc.Graph(id='graph3')], style={'margin-bottom': '10px'}),

            ], style={'width': '47%', 'display': 'inline-block'}),


        html.Div(className='padding', children=[
            html.Div(className='content-box', children=[
                dcc.Graph(id='graph1')], style={'margin-bottom': '10px', 'margin-top': '-16px'}),

            html.Div(className='content-box', children=[
                dcc.Graph(id='graph2')], style={'margin-bottom': '10px'}),

            html.Div(className='content-box', children=[
                dcc.Graph(id='Courbe')], style={'margin-bottom': '10px'})

            ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})

    ])


@app.callback(
    Output('graph1', 'figure'),
    Output('graph2', 'figure'),
    Output('graph3', 'figure'),
    Output('Courbe', 'figure'),
    Output('map', 'figure'),
    Input('annee--dropdown', 'value'),
    Input('campus--dropdown', 'value'),
    Input('domaine--dropdown', 'value'),
    Input('type--dropdown', 'value'),
    Input('tabs', 'value'))
def update_graph(annee_value,campus_value, domaine_value, type_value, tabs_value):
    dff = df    

    #Filtre la base de données
    if campus_value != None:
        dff = dff[dff['Campus'] == campus_value]

    if domaine_value != None:
        dff = dff[dff['Domaine'] == domaine_value]

    if type_value != None:
        dff = dff[dff['Type de poste'] == type_value]

    df_Courbe = pd.DataFrame(dff)

    if annee_value == None :
        annee_value = 2023

    if tabs_value == 'Recrutements' :
        texte_graph_3 = "Moyenne d'age par Domaine au recrutement"

        dff = dff[dff['Annee de recrutement'] == annee_value]

    else :
        texte_graph_3 = "Moyenne d'age par Domaine"

        dff = dff[dff['Annee de recrutement'] <= annee_value]
        dff = dff[dff['Annee de fin de contrat'] >= annee_value]
    

    Graph1 = px.histogram(dff, x='Domaine', color='Sexe',
        color_discrete_map= {'H' : '#58d68d', 'F' :'#7fb3d5'})

    Graph1["layout"] = dict(
        title={'text': f"Répartition des {tabs_value} par Domaine", 'font':{'size' :35},'x': 0.5, 'xanchor': 'center'},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend={"font": {"color": '#d6eaf8'}, "orientation": "h", "x": 0, "y": 1.1},
        font={"color": '#d6eaf8'},
        showlegend=True,
        xaxis={
            "zeroline": False,
            "showgrid": False,
            "title": "Domaine",
            "showline": False,
            "titlefont": {"color": '#d6eaf8'},
        },
        yaxis={
            "title": tabs_value,
            "zeroline": False,
            "autorange": True,
            "titlefont": {"color": '#d6eaf8'},
        },
    )


    Graph2 = px.histogram(dff, y='Type de poste', color='Sexe', 
        color_discrete_map= {'H' : '#58d68d', 'F' :'#7fb3d5'})

    Graph2["layout"] = dict(
        title={'text': f"Répartition des {tabs_value} par Type de Poste", 'font':{'size' :35},'x': 0.5, 'xanchor': 'center'},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend={"font": {"color": '#d6eaf8'}, "orientation": "h", "x": 0, "y": 1.1},
        font={"color": '#d6eaf8'},
        showlegend=True,
        xaxis={
            "zeroline": False,
            "showgrid": False,
            "title": tabs_value,
            "showline": False,
            "titlefont": {"color": '#d6eaf8'},
        },
        yaxis={
            "title": "Type de Poste",
            "zeroline": False,
            "autorange": True,
            "titlefont": {"color": '#d6eaf8'},
        },
    )


    Graph3 = px.histogram(dff, 
                          x='Domaine',
                          y=annee_value-dff['Annee de Naissance'],
                          color='Sexe',
                          histfunc='avg',
                          color_discrete_map= {'H' : '#58d68d', 'F' :'#7fb3d5'},
                          labels ={'y' : 'Age'}

    )

    Graph3["layout"] = dict(
        title={'text': texte_graph_3, 'font':{'size' :35},'x': 0.5, 'xanchor': 'center'},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend={"font": {"color": '#d6eaf8'}, "orientation": "h", "x": 0, "y": 1.1},
        font={"color": '#d6eaf8'},
        showlegend=True,
        xaxis={
            "zeroline": False,
            "showgrid": False,
            "title": "Domaine",
            "showline": False,
            "titlefont": {"color": '#d6eaf8'},
        },
        yaxis={
            "title": "Age",
            "zeroline": False,
            "autorange": True,
            "titlefont": {"color": '#d6eaf8'},
        },
    )

    if tabs_value == "Recrutements" :
        #Groupe les recrutements par année et par sexe
        df_grouped = df_Courbe.groupby(df_Courbe['Annee de recrutement'])['Annee de recrutement'].count().rename('All').to_frame()

        dfH = pd.DataFrame(df_Courbe[df_Courbe['Sexe'] == 'H'], columns =['Annee de recrutement'])
        df_groupedH = dfH.groupby(dfH['Annee de recrutement'])['Annee de recrutement'].count().rename('H').to_frame()

        dfF = pd.DataFrame(df_Courbe[df_Courbe['Sexe'] == 'F'], columns =['Annee de recrutement'])
        df_groupedF = dfF.groupby(dfF['Annee de recrutement'])['Annee de recrutement'].count().rename('F').to_frame()
        
        df_grouped = df_grouped.assign(H = df_groupedH['H'])
        df_grouped = df_grouped.assign(F = df_groupedF['F'])

    else :
        df_grouped = pd.DataFrame(index=[i for i in range(df_Courbe['Annee de recrutement'].min(), df_Courbe['Annee de recrutement'].max()+1)])

        df_grouped.insert(0, "H", None)
        df_grouped.insert(0, "F", None)

        for year in range(df_Courbe['Annee de recrutement'].min(), df_Courbe['Annee de recrutement'].max()+1):

            dfF = pd.DataFrame(df_Courbe[df_Courbe['Annee de recrutement'] <= year], columns =['Sexe', 'Annee de fin de contrat'])
            dfF =dfF[dfF['Annee de fin de contrat'] >= year]
            #print(dfF)
            dfH = dfF.groupby(dfF['Sexe'])['Sexe'].count()

            for i, S in enumerate(dfH.index.tolist()):
                df_grouped.loc[year, S] = dfH[i]


    Courbe = px.line(df_grouped,
                     y=['F', 'H'],
                     markers=True,
                     color_discrete_sequence=['#7fb3d5', '#58d68d'],
                     labels={'variable': 'Sexe', 'value' : tabs_value, 'index' : 'Année', 'Annee de recrutement' : 'Année'})
    
    Courbe["layout"] = dict(
        title={'text': f"Evolution des {tabs_value}", 'font':{'size' :35},'x': 0.5, 'xanchor': 'center'},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend={"font": {"color": '#d6eaf8'}, "orientation": "h", "x": 0, "y": 1.1},
        font={"color": '#d6eaf8'},
        hovermode="x",
        xaxis={
            "zeroline": False,
            "showgrid": False,
            "title": "Année",
            "showline": False,
            "titlefont": {"color": '#d6eaf8'},
        },
        yaxis={
            "title": tabs_value,
            "zeroline": False,
            "autorange": True,
            "titlefont": {"color": '#d6eaf8'},
        },)

    #Associe le nombre de personne total par Campus et par sexe
    df_Campus1 = df_Campus
    df_map = dff.groupby(dff['Campus'])['Campus'].count().rename('All').to_frame()
    df_Campus1 = df_Campus1.set_index('Campus')
    df_Campus1 = df_Campus1.assign(All = df_map['All'])

    dfH = pd.DataFrame(dff[dff['Sexe'] == 'H'], columns =['Campus'])
    df_CampusH = dfH.groupby(dfH['Campus'])['Campus'].count().rename('H').to_frame()

    dfF = pd.DataFrame(dff[dff['Sexe'] == 'F'], columns =['Campus'])
    df_CampusF = dfF.groupby(dfF['Campus'])['Campus'].count().rename('F').to_frame()
    
    df_Campus1 = df_Campus1.assign(H = df_CampusH['H'])
    df_Campus1 = df_Campus1.assign(F = df_CampusF['F'])

    df_Campus1 = df_Campus1.dropna(subset='All')
    df_Campus1['H'] = df_Campus1['H'].fillna(0)

    map = px.scatter_mapbox(df_Campus1,
                            lat = 'Lat',
                            lon = 'Lon',
                            size='All',
                            color="All",
                            hover_name= df_Campus1.index,
                            hover_data={'Lat':False, 'Lon': False, 'F' : True, 'H' : True},
                            title=f'Répartition des {tabs_value} par département',
                            color_continuous_scale="Aggrnyl",
                            range_color=(0, df_Campus1['All'].max()),
                            mapbox_style='carto-darkmatter',
                            zoom=4.5,
                            center = {"lat": 46.5, "lon": 2.4},
                            height=700,
                            labels=({'All': tabs_value}))
    
    map.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={"color": '#d6eaf8'},
                    title={'font':{'size' :35},'x': 0.5, 'xanchor': 'center'})

    return Graph1, Graph2, Graph3, Courbe, map




if __name__ == '__main__':
	app.run_server(debug=True)