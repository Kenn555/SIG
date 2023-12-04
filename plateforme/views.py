import datetime
import json
from statistics import mean
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import requests
from .models import Visiteur, Soumission

# Create your views here.

# api = Api('https://ministere_sante.mg', 'Stagiaire_SEMIDSI', '2023@Dhis2')
# Dashboards MSPM : 23
# url_base = "https://play.dhis2.org/40.1.0"
# config = ('admin', 'district')

url_base = "https://ministere-sante.mg"
config = ('Stagiaire_SEMIDSI', '2023@Dhis2')

url_api = url_base + "/api/"

def index(request):
    print('Dashbords...')
    dashboards = get_dashboards()
    first_dashboard_item = dashboards['dashboards'][0]
    print('DHIS2 version...')
    dhis_version = get_version_dhis()

    # print(dashboards['dashboards'])
    return render(request, 'plateforme/index.html',
                  {
                      'dashboards': [a for a in dashboards['dashboards']],
                      'first_dashboard_item': first_dashboard_item,
                      'dhis_version': dhis_version,
                   }
                )

def api_get_data(path: str):
    url = url_api + path

    if path.find('dashboardItems') != -1:
        url += '?paging=false'

    print('Go to', url)
    datas = {'erreur': "API non atteint",
                'dashboards': [
                    {'displayName': 'Erreur1', 'id': 'Erreur1'},
                    {'displayName': 'Erreur2', 'id': 'Erreur2'},
                    {'displayName': 'Erreur3', 'id': 'Erreur3'}
                ]
            }
    try:
        response = requests.get(url, auth=config)
        datas = response.json()
    except:
        pass
    return datas

def reporttable_datas(response: dict)-> dict:
    row_titles = []
    columns = []
    data = []
    
    if len(response['headers']) > 2:
        columns = [{"data": '#0', "title": ''}]
        for row in response['metaData']['dimensions'][response['headers'][1]['name']]:
            if row.find('.'):
                row = row.split('.')[0]
            row_titles += [{row: response['metaData']['items'][row]['name']}]
        if response['headers'][1]['name'] == 'ou':
            response['metaData']['dimensions'][response['headers'][1]['name']].sort()

        for info in row_titles:
            lieu_resultat = {'#0': list(info.items())[0][1]}
            for row in response['rows']:
                if row[1] == list(info.items())[0][0]:
                    if row[0].find('.'):
                        row[0] = row[0].split('.')[0]
                    lieu_resultat[row[0]] = row[-1]
            data.append(lieu_resultat)
    else:
        for row in response['rows']:
            if row[0].find('.'):
                row[0] = row[0].split('.')[0]
            data += [{row[0]: row[-1]} ]

    for column in response['metaData']['dimensions'][response['headers'][0]['name']]:
        if column.find('.'):
            columns += [{"data": column.split('.')[0], "title": response['metaData']['items'][column]['name']}]
        else:
            columns += [{"data": column, "title": response['metaData']['items'][column]['name']}]

    print(columns)
    print(data)
    return {'columns': columns, 'data': data}

def get_analytic_values(dimension_datas, periods: list = []):
    analytic_param = "analytics?"
    for key in dimension_datas:
        if key == 'filters':
            for dimension_values in dimension_datas[key]:
                for id_dimension in dimension_values:
                    if len(periods) != 0 and id_dimension == 'pe':
                        analytic_param += "&filter=" + id_dimension + ":" + ";".join(periods)
                    else:
                        analytic_param += "&filter=" + id_dimension + ":" + ";".join(dimension_values[id_dimension])
        else:
            for dimension_values in dimension_datas[key]:
                for id_dimension in dimension_values:
                    if len(periods) != 0 and id_dimension == 'pe':
                        analytic_param += "&dimension=" + id_dimension + ":" + ";".join(periods)
                    else:
                        analytic_param += "&dimension=" + id_dimension + ":" + ";".join(dimension_values[id_dimension])
    
    print(analytic_param)

    analytic = api_get_data(analytic_param)
    # print(analytic)
    print()
    return analytic

def get_item_infos(items):
    # print(items)
    path = items['href'].split('/')[-2] + "/" + items['href'].split('/')[-1]

    response = api_get_data(path)

    print(response)
    try:
        if response["type"] == "YEAR_OVER_YEAR_LINE":
            items['yearlySeries'] = response["yearlySeries"]
            pass
        # print(response)
    except KeyError:
        pass

    if items['type'] == "VISUALIZATION":
        dimension_parameter = {'columns': [],'rows': [],'filters': []}

        for key in dimension_parameter:
            if len(response[key]) != 0:
                url = items['href'] + '/' + key
                dimension_datas = requests.get(url, auth=config).json()

                for type_dimension in dimension_datas[key]:
                    value_dimension = []
                    try:
                        if len(type_dimension['items']) != 0:
                            value_dimension += [item['id'] for item in type_dimension['items']] if type_dimension['id'] != 'dx' else [item['reportingRate']['dimensionItem'] for item in response['dataDimensionItems']]
                    except KeyError:
                        value_dimension += [item['id'] for item in type_dimension['items']]
                    dimension_parameter[key].append({type_dimension['id']: value_dimension})
        # print(dimension_parameter)

    if items['type'] == 'MAP':
        try:
            mapdisplay_datas = {'name': response['name'], 'longitude': response['longitude'], 'latitude': response['latitude'], 'zoom': response['zoom']}
        except KeyError:
            mapdisplay_datas = {}
        map_views = response['mapViews']
        mapdisplay_datas['mapViews'] = []
        dimension_parameter = {'columns': [],'rows': [],'filters': []}

        for i, map_view in enumerate(map_views):
            mapdisplay_datas['mapViews'].append({})
            mapdisplay_datas['mapViews'][i] = {'name': map_view['name']}
            mapdisplay_datas['mapViews'][i]['organisationUnitLevels'] = int(map_view['organisationUnitLevels'][0])

            try:
                data_dimension_item = [view[view['dataDimensionItemType'].lower()]['id'] for view in map_view['dataDimensionItems']]
            except KeyError:
                s = ""
                for view in map_view['dataDimensionItems']:
                    for n, x in enumerate([c for c in view['dataDimensionItemType'].split('_')]):
                        s += x.capitalize()
                        if n == 0:
                            s = s.lower()
                            
                data_dimension_item = [view[s]['id'] for view in map_view['dataDimensionItems']]

            ou_query = url_api + f"organisationUnits/{map_view['organisationUnits'][0]['id']}?filter=level:eq:{int(map_view['organisationUnitLevels'][0])}&paging=false"
            # print(ou_query)
            try:
                ou_response = requests.get(ou_query, auth=config).json()
            except requests.exceptions.JSONDecodeError:
                ou_query = url_api + f"organisationUnits?fields=name,id,level,parent&filter=parent.id:eq:{map_view['organisationUnits'][0]['id']}&level={int(map_view['organisationUnitLevels'][0])}&paging=false"
                ou_response = requests.get(ou_query, auth=config).json()

            # print(ou_response)

            for key in dimension_parameter: # parametre de la sequence i
                if len(map_view[key]) != 0:
                    for j, type_dimension in enumerate(map_view[key]):
                        value_dimension = []
                        if len(dimension_parameter[key]) == 0:
                            dimension_parameter[key].append({})

                        if type_dimension['id'] == 'ou':
                            try:
                                value_dimension += [ou_value['id'] for ou_value in ou_response['organisationUnits']]
                            except KeyError:
                                value_dimension += [ou_value['id'] for ou_value in ou_response['children']]
                            mapdisplay_datas['mapViews'][i]['organisationUnits'] = value_dimension
                            try:
                                dimension_parameter[key][j][type_dimension['id']] += value_dimension
                                mapdisplay_datas['mapViews'][i]['organisationUnits'] += value_dimension
                                continue
                            except KeyError:
                                pass
                        elif type_dimension['id'] == 'dx':
                            if len(data_dimension_item) == 0:
                                data_dimension_item = None
                                break
                            value_dimension = data_dimension_item
                        elif type_dimension['id'] == 'pe':
                            for period in map_view['periods']:
                                value_dimension += [period['id']]
                        else:
                            pass
                        dimension_parameter[key][j][type_dimension['id']] = value_dimension
                    if data_dimension_item == None:
                        continue

    return dimension_parameter

def get_html_data():
    return api_get_data("organisationUnits")

def get_dashboards():
    return api_get_data('dashboards')

def set_grid(items: dict, nb_col: int):
    new_items = {}
    nb_constant = len(items['dashboardItems'])
    d_item = []
    nb_counter = 0
    nb_mod_max = int(nb_constant / nb_col)
    print(nb_constant)
    items['dashboardItems'].reverse()
    
    for nb, item in enumerate(items['dashboardItems']):
        print(nb_counter, len(d_item), nb)
        # Vérifier les valeurs avant
        if nb != 0 and (nb % nb_col) == 0: # nb est un multiple de 3
            new_items[nb_counter] = d_item
            d_item = []
            nb_counter += 1

        d_item += [item]

        # Vérifier les valeurs après
        if (nb + 1) == nb_constant:
            print("fin")
            new_items[nb_counter] = d_item

        print(d_item)
        print(nb_counter, len(d_item), nb)
        print()

    return new_items

def get_dashboards_items(id_dashboard: str):
    dashboard_items = {"dashboardItems":[]}
    dashboards = api_get_data(f"dashboards/{id_dashboard}?fields=dashboardItems[type,href,id,name,visualization,map]")
    for i, dashboard_item in enumerate(dashboards['dashboardItems']):
        if dashboard_item['type'] == 'MAP':
            item_uid = dashboard_item['map']['id']
        elif dashboard_item['type'] in ['TEXT', 'MESSAGES']:
            continue
        else :
            item_uid = dashboard_item['visualization']['id']

        item = requests.get(url_api + dashboard_item['type'].lower() + 's' + '/' + item_uid + '/?fields=name,href', auth=config).json()

        data = {
            'name': item['name'],
            'type': dashboard_item['type'],
            'id': item_uid, 
            'href': item['href']
            # 'href': url_api + dashboard_item['type'].lower() + 's' + '/' + item_uid
            }
        # data['data'] = get_item_infos(data)
        
        # ['type', 'id', 'href']
        dashboard_items['dashboardItems'].append(data)

    
    return set_grid(dashboard_items, 3)

def get_version_dhis2():
    infos = api_get_data("system/info")
    return infos['version']

def get_graph_value(graph_id, periode, organisation_unit_id):
    import requests

    url = "analytics"
    params = {
        "dimension": f"dx:{graph_id}",
        "dimension": f"pe:{periode}",
        "filter": f"ou:{organisation_unit_id}"
    }

    response = requests.get(url, params=params, auth=config)
    data = response.json()

def get_version_dhis():
    request = api_get_data('system/info')

    print("Version du DHIS2 :", request['version'])
    return request['version']

def multipolygon_center(multipolygon):
    # Initialiser les variables pour les coordonnées X et Y
    total_x = 0
    total_y = 0
    nombre_de_points = 0

    # Parcourir les polygones
    for polygon in multipolygon:
        # Parcourir les anneaux du polygone
        for ring in polygon:
            # Parcourir les points de l'anneau
            for point in ring:
                # Ajouter les coordonnées du point aux totaux
                total_x += point[0]
                total_y += point[1]
                nombre_de_points += 1

    # Calculer les coordonnées moyennes
    centre_x = total_x / nombre_de_points
    centre_y = total_y / nombre_de_points

    return [centre_x, centre_y]

def polygon_center(coordinates):
    coordinates = coordinates[0]  # La première liste de coordonnées représente le polygone extérieur

    # Calculer les moyennes des coordonnées x et y
    center_x = sum(coord[0] for coord in coordinates) / len(coordinates)
    center_y = sum(coord[1] for coord in coordinates) / len(coordinates)

    return [center_x, center_y]

def get_item_map(analytic: dict, info):
    # organisationUnits (id, name, value, geometry)
    # legendSets

    print(info['id'])

    '/legends?fields=startValue,endValue,color'

    data_dimension_items = None
    legend_set = None
    response = None

    if info['type'] == 'VISUALIZATION':
        parent_geometry = requests.get(url= info['href'] + '/organisationUnits?fields=geometry', auth=config).json()['organisationUnits'][0]['geometry']
        data_dimension_items = requests.get(info['href'] + '/dataDimensionItems', auth=config).json()
        
        if data_dimension_items != None :
            try:
                for data_dimension_item in data_dimension_items['dataDimensionItems']:
                    print(data_dimension_item)
                    if data_dimension_item['dataDimensionItemType'] == 'REPORTING_RATE':
                        legend_ = api_get_data('dataSets/' + data_dimension_item['reportingRate']['dataSet']['id'] + '/legendSets')[0]['id']
                    elif data_dimension_item['dataDimensionItemType'] == "DATA_ELEMENT":
                        legend_ = api_get_data('dataElements/' + data_dimension_item[data_dimension_item['dataDimensionItemType'].lower()]['id'] + '/legendSets')[0]['id']
                    else:
                        legend_ = api_get_data(data_dimension_item['dataDimensionItemType'].lower() + 's/' + data_dimension_item[data_dimension_item['dataDimensionItemType'].lower()]['id'] + '/legendSets')[0]['id']
            except KeyError:
                pass


    elif info['type'] == 'MAP':
        response = requests.get(url= info['href'] + '/mapViews?fields=organisationUnits,dataDimensionItems', auth=config).json()
        print(response)
        id_parent = response['mapViews'][0]['organisationUnits'][0]['id']
        for mapview in response['mapViews']:
            print(mapview)

            try:
                api_type = mapview['dataDimensionItems'][0]['dataDimensionItemType'].lower()
            except IndexError:
                continue

            try:
                if data_dimension_items != None:
                    break
                if mapview['dataDimensionItems'][0]['dataDimensionItemType'] == 'DATA_ELEMENT':
                    api_type = 'dataElement'
                elif mapview['dataDimensionItems'][0]['dataDimensionItemType'] == 'REPORTING_RATE':
                    api_type = 'dataSet'
                else:
                    api_type = mapview['dataDimensionItems'][0]['dataDimensionItemType'].lower()

                data_dimension_items = mapview['dataDimensionItems'][0][api_type]['id']
            except IndexError:
                continue
        parent_geometry = requests.get(url= url_api + 'organisationUnits/' + id_parent + '/geometry', auth=config).json()['geometry']

        if data_dimension_items != None :
            legend_ = api_get_data(api_type + 's/' + data_dimension_items + '/legendSets')['legendSets'][0]['id']
    
    try:
        if data_dimension_items != None :
            legend_set = api_get_data('/legendSets/' + legend_ + '/legends?fields=startValue,endValue,color')
    except:
        pass

    print(data_dimension_items)
    
    if parent_geometry['type'] == 'Polygon':
        center = polygon_center(parent_geometry['coordinates'])
    elif parent_geometry['type'] == 'MultiPolygon':
        center = multipolygon_center(parent_geometry['coordinates'])
        
    center.reverse()
    try:
        statesData = {"type": "FeatureCollection", "features": [], "center": center, "legends": legend_set['legends']}
    except:
        statesData = {"type": "FeatureCollection", "features": [], "center": center, "legends": legend_set}


    print(analytic)

    for ou_item in analytic['metaData']['dimensions']['ou']:
        url = url_api + '/organisationUnits/' + ou_item + '?fields=name,geometry'
        # print(url)
        response = requests.get(url=url, auth=config).json()
        try:
            statesData['features'] += [{"type":"Feature","id":ou_item,"properties":{"name": response['name'],"density":[]},"geometry":response['geometry']}]
        except:
            continue

    for row in analytic['rows']:
        # print(row)
        for i, ou_item in enumerate(statesData['features']):
            if ou_item['id'] in row:
                statesData['features'][i]['properties']['density'] += [float(row[-1])]
                # print(statesData['features'][i]['properties']['density'])
    
    for i, ou_item in enumerate(statesData['features']):
        # print(statesData['features'][i]['id'], statesData['features'][i]['properties']['density'])
        statesData['features'][i]['properties']['density'] = round(mean(statesData['features'][i]['properties']['density']), 1)

    return statesData

def get_item_chart(data, info):
    
    chart_data = {'labels': [], 'datasets': []}

    if info['type'] == 'VISUALIZATION':
        # Récupération du type de VISUALIZATION (Graphique) utilisé
        chart_info = requests.get(info['href'] + '?fields=type,axes', auth=config).json()
        chart_type = chart_info['type']

        if len(chart_info) == 2:
            chart_data['annotation'] = []
            for axe in chart_info['axes']:
                if axe['type'] == 'RANGE':
                    chart_data['annotation'] += [{'value': axe['targetLine']['value'], 'label': axe['targetLine']['title']['text']}]
            pass

    elif info['type'] == 'MAP':
        chart_type = 'COLUMN'
        pass

    # print()
    # print(chart_type)

    # Récupération des labels
    try:
        chart_data['labels'] = [item['#0'] for item in data['data']]
    except KeyError:
        chart_data['labels'] = [item['title'] for item in data['columns']]
        pass

    print(data)
    print()
    print(info)

    if chart_type != 'year_over_year_line'.upper():
        # Récupération des datasets
        for col in data['columns'][1:]:
            print(col)
            try:
                dataset = {'label': col['title'], 'data': []}
                dataset['data'] = [item[col['data']] for item in data['data']]
                chart_data['datasets'].append(dataset)
            except KeyError:
                continue
    else:
        print(info['yearlySeries'])
        dataset = {'label': datetime.date.today().year, 'data': []}
        for col in data['columns']:
            print(col)
            for item in data['data']:
                print(item)
                try:
                    print()
                    dataset['data'] += [item[col['data']]]
                except KeyError:
                    continue
            
        chart_data['datasets'].append(dataset)
    
    
    if chart_type == "COLUMN":
        chart_type = 'bar'
    elif chart_type == 'year_over_year_line'.upper():
        chart_type = 'line'
    else:
        chart_type = chart_type.lower()
    
    # print(chart_type)
    # print()
    
    # Conversion des données en format souhaité pour Chart.js
    chart_data['type'] = chart_type

    print(chart_data)

    return chart_data

def save_form(data):
    nom = data['nom']
    prenom = data['prenom']
    structure = data['structure']
    lieu_travail = data['lieu_travail']
    telephone = data['telephone']
    email = data['email']

    # Vérifiez si l'utilisateur existe déjà dans la table Visiteur
    print("Vérifiez si l'utilisateur existe déjà dans la table Visiteur...")
    existing_user = Visiteur.objects.filter(email=email).first()

    data = {'message': 'Informations soumises !'}

    if existing_user:
        # Si l'utilisateur existe déjà, ajoutez simplement la soumission
        Soumission.objects.create(information=existing_user)
    else:
        # Si l'utilisateur n'existe pas, créez-le dans la table Visiteur
        new_user = Visiteur.objects.create(
            nom=nom,
            prenom=prenom,
            structure=structure,
            lieu_travail=lieu_travail,
            telephone=telephone,
            email=email
        )
        data = {'message': 'Informations créées !!!'}

        # Créez la soumission pour le nouvel utilisateur
        Soumission.objects.create(information=new_user)

    print('Done !!!!!!!!!!!!!')

    return data

def action(request):
    if request.method == 'POST':
        data = dict(json.loads(request.body))
        print(data)
        
        if data['query'] == "dashboardItem":
            # data['data'] doit contenir l'ID du dashboard
            data = get_dashboards_items(data['datas'])
            # print(data)
        elif data['query'] == 'reportTable':
            # data['data'] doit contenir l'ID du dashboardItem
            if 'filter' in  data:
                data = reporttable_datas(get_analytic_values(get_item_infos(data['datas']), data['filter']))
            else:
                data = reporttable_datas(get_analytic_values(get_item_infos(data['datas'])))
        elif data['query'] == 'chart':
            if 'filter' in  data:
                data = get_item_chart(reporttable_datas(get_analytic_values(get_item_infos(data['datas']), data['filter'])), data['datas'])
            else:
                data = get_item_chart(reporttable_datas(get_analytic_values(get_item_infos(data['datas']))), data['datas'])
        elif data['query'] == 'map':
            if 'filter' in  data:
                data = get_item_map(get_analytic_values(get_item_infos(data['datas']), data['filter']), data['datas'])
            else:
                data = get_item_map(get_analytic_values(get_item_infos(data['datas'])), data['datas'])
        elif data['query'] == 'form':
            print('Form')
            data = save_form(data['datas'])

        return JsonResponse(data)
    return JsonResponse({'Erreur': 'Erreur !!!'})