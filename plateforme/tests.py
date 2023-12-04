# from statistics import mean
# from django.test import TestCase

# # Create your tests here.
# import requests


# # api = Api('https://ministere_sante.mg', 'Stagiaire_SEMIDSI', '2023@Dhis2')

# url_base = "https://ministere-sante.mg"
# config = ('Stagiaire_SEMIDSI', '2023@Dhis2')
# path = 'dashboards'

# # url_base = "https://play.dhis2.org/40.1.0"
# # config = ('admin', 'district')

# url_api = url_base + "/api/"
# url = url_api + path

# dashboard_items = {}

# def get_detailElement(path_base, id, title):
#     path = path_base + f"/{id}"

#     print("Ouverture de \'" + title + "\' : " + path)
#     print()

#     datas = requests.get(path, auth=config).json()

#     print(', '.join(data for data in datas))

# def get_dataElements(title, path, plural):
#         print("Ouverture de " + title + " : " + path)
#         print()
#         datas = requests.get(path, auth=config).json()
#         # print(donnees)

#         try:
#             page_info = datas['pager']
#             # print(page_info)
#         except KeyError:
#             pass

#         try:
#             elements = datas[plural]
#             el_number = get_response(elements)

#             get_detailElement(path, elements[el_number]['id'], elements[el_number]['displayName'])
#         except KeyError:
#             print(datas)

# def get_resources(datas): # Obtenir tous les api de la plateforme
#     resources = datas['resources']
#     rc_number = get_response(resources=resources)

#     get_dataElements(resources[rc_number]['displayName'], resources[rc_number]['href'], resources[rc_number]['plural'])


# def get_response(resources):
#     rc_names = []
#     for resource in resources:
#         # print(resource['plural'] + " : " + resource['href'])
#         rc_names.append(resource['displayName'])
#     print("==> " + ', '.join(rc + f" ({i})" for i,rc in enumerate(rc_names, 1)) + ".")
#     print()
#     try:
#         rc_number = int(input("Entrez un numéro de groupe de données : ")) - 1
#         print()
        
#         if rc_number > (len(rc_names)):
#             print("Le numéro est dépassé !!")
#             exit()
#     except:
#         print("Entrée incorrecte : Veillez entrer que des entiers !")
#         exit()

#     return rc_number

# def get_map(analytic: dict):
#     # organisationUnits (id, name, value, geometry)
#     # legendSets

#     statesData = {"type":"FeatureCollection","features":[]}

#     for ou_item in analytic['metaData']['dimensions']['ou']:
#         url = url_api + '/organisationUnits/' + ou_item + '?fields=name,geometry'
#         print(url)
#         response = requests.get(url=url, auth=config).json()
#         statesData['features'] += [{"type":"Feature","id":ou_item,"properties":{"name": response['name'],"density":[]},"geometry":response['geometry']}]

#     for row in analytic['rows']:
#         print(row)
#         for i, ou_item in enumerate(analytic['metaData']['dimensions']['ou']):
#             if ou_item in row:
#                 statesData['features'][i]['properties']['density'] += [float(row[-1])]
                
#         pass
    
#     for i, ou_item in enumerate(analytic['metaData']['dimensions']['ou']):
#         statesData['features'][i]['properties']['density'] = round(mean(statesData['features'][i]['properties']['density']), 1)

#     return statesData
    

# def reporttable_datas(response: dict)-> dict:
#     row_titles = []
#     columns = []
#     data = []
    
#     if len(response['headers']) > 2:
#         columns = [{"data": '#0', "title": ''}]
#         for row in response['metaData']['dimensions'][response['headers'][1]['name']]:
#             row_titles += [{row: response['metaData']['items'][row]['name']}]
#         if response['headers'][1]['name'] == 'ou':
#             response['metaData']['dimensions'][response['headers'][1]['name']].sort()

#         for info in row_titles:
#             lieu_resultat = {'#0': list(info.items())[0][1]}
#             density = []
#             densities = {}
#             for row in response['rows']:
#                 if row[1] == list(info.items())[0][0]:
#                     lieu_resultat[row[0]] = float(row[-1])
#             data.append(lieu_resultat)
#     else:
#         for row in response['rows']:
#             data += [{row[0]: row[-1]}]

#     for column in response['metaData']['dimensions'][response['headers'][0]['name']]:
#         columns += [{"data": column, "title": response['metaData']['items'][column]['name']}]

#     print(columns)
#     print()
#     print(data)
#     print(len(data))


# def get_analytic_values(dimension_datas):
#     analytic_param = "analytics?"
#     for key in dimension_datas:
#         if key == 'filters':
#             for dimension_values in dimension_datas[key]:
#                 for id_dimension in dimension_values:
#                     analytic_param += "&filter=" + id_dimension + ":" + ";".join(dimension_values[id_dimension])
#         else:
#             for dimension_values in dimension_datas[key]:
#                 for id_dimension in dimension_values:
#                     analytic_param += "&dimension=" + id_dimension + ":" + ";".join(dimension_values[id_dimension])

#     url = url_api + analytic_param
    
#     print(analytic_param)
#     analytic = requests.get(url, auth=config).json()
#     print(analytic['rows'])


#     # print(analytic)
#     # print()
#     # reporttable_datas(analytic)

# def get_item_infos(items: dict):
#     reporttable_datas = {}
#     type_item = ""
#     href_item = {}
#     id_item = input("Entrez l'ID de l'élément : ")

#     # Obtenir le type et le href de l'item entré
#     for item_key in items:
#         item_value = ""
#         print(item_key)
#         for value in items[item_key]:
#             if item_value != id_item:
#                 for item_value in value:
#                     if item_value == id_item:
#                         print(item_value, id_item)
#                         item_value = id_item
#                         type_item = item_key
#                         href_item = value[id_item]
#                         break
#             else:
#                 break


#     print(type_item, href_item)

#     response = requests.get(href_item, auth=config)

#     response = dict(response.json())

#     if type_item == "VISUALIZATION":
#         dimension_parameter = {'columns': [],'rows': [],'filters': []}
#         for key in dimension_parameter:
#             if len(response[key]) != 0:
#                 url = href_item + '/' + key
#                 dimension_datas = requests.get(url, auth=config).json()
#                 for type_dimension in dimension_datas[key]:
#                     value_dimension = []
#                     try:
#                         value_dimension += [item['id'] for item in type_dimension['items']] if type_dimension['id'] != 'dx' else [item['reportingRate']['dimensionItem'] for item in response['dataDimensionItems']]
#                     except KeyError:
#                         value_dimension += [item['id'] for item in type_dimension['items']]
#                     dimension_parameter[key].append({type_dimension['id']: value_dimension})
#         print(dimension_parameter)

#     elif type_item == "MAP":
#         try:
#             mapdisplay_datas = {'name': response['name'], 'longitude': response['longitude'], 'latitude': response['latitude'], 'zoom': response['zoom']}
#         except KeyError:
#             mapdisplay_datas = {}
#         map_views = response['mapViews']
#         mapdisplay_datas['mapViews'] = []
#         data_dimension_items = []
#         dimension_parameter = {'columns': [],'rows': [],'filters': []}

#         for i, map_view in enumerate(map_views):
#             mapdisplay_datas['mapViews'].append({})
#             mapdisplay_datas['mapViews'][i] = {'name': map_view['name']}
#             mapdisplay_datas['mapViews'][i]['organisationUnitLevels'] = int(map_view['organisationUnitLevels'][0])

#             try:
#                 data_dimension_item = [view[view['dataDimensionItemType'].lower()]['id'] for view in map_view['dataDimensionItems']]
#             except KeyError:
#                 s = ""
#                 for view in map_view['dataDimensionItems']:
#                     for n, x in enumerate([c for c in view['dataDimensionItemType'].split('_')]):
#                         s += x.capitalize()
#                         if n == 0:
#                             s = s.lower()
                            
#                 data_dimension_item = [view[s]['id'] for view in map_view['dataDimensionItems']]

#             ou_query = url_api + f"organisationUnits/{map_view['organisationUnits'][0]['id']}?filter=level:eq:{int(map_view['organisationUnitLevels'][0])}&paging=false"
#             print(ou_query)
#             try:
#                 ou_response = requests.get(ou_query, auth=config).json()
#             except requests.exceptions.JSONDecodeError:
#                 ou_query = url_api + f"organisationUnits?fields=name,id,level,parent&filter=parent.id:eq:{map_view['organisationUnits'][0]['id']}&level={int(map_view['organisationUnitLevels'][0])}&paging=false"
#                 ou_response = requests.get(ou_query, auth=config).json()

#             print(ou_response)

#             for key in dimension_parameter: # parameter de la sequence i
#                 if len(map_view[key]) != 0:
#                     for j, type_dimension in enumerate(map_view[key]):
#                         value_dimension = []
#                         if len(dimension_parameter[key]) == 0:
#                             dimension_parameter[key].append({})

#                         if type_dimension['id'] == 'ou':
#                             try:
#                                 value_dimension += [ou_value['id'] for ou_value in ou_response['organisationUnits']]
#                             except KeyError:
#                                 value_dimension += [ou_value['id'] for ou_value in ou_response['children']]
#                             mapdisplay_datas['mapViews'][i]['organisationUnits'] = value_dimension
#                             try:
#                                 dimension_parameter[key][j][type_dimension['id']] += value_dimension
#                                 mapdisplay_datas['mapViews'][i]['organisationUnits'] += value_dimension
#                                 continue
#                             except KeyError:
#                                 pass
#                         elif type_dimension['id'] == 'dx':
#                             if len(data_dimension_item) == 0:
#                                 data_dimension_item = None
#                                 break
#                             value_dimension = data_dimension_item
#                         elif type_dimension['id'] == 'pe':
#                             for period in map_view['periods']:
#                                 value_dimension += [period['id']]
#                         else:
#                             pass
#                         dimension_parameter[key][j][type_dimension['id']] = value_dimension
#                     if data_dimension_item == None:
#                         continue
#             # dimension_parameters.append(dimension_parameter)
#         print(dimension_parameter)
#         print(mapdisplay_datas)

#             # dimension_parameter = dimension_parameters
#             # if len(reporttable_datas) != 0:
#             #     reporttable_datas['media']
#             #     pass
#     reporttable_datas = get_analytic_values(dimension_parameter)
#     print(reporttable_datas)
#     # print(item_name)
#     # print(coordonate_initial)
#     # print(dimension_parameter)
#     # print(ou_level)
#     # print(data_dimension_items)
#     # print(periods)




# response = requests.get(url, auth=config)

# if response.status_code == 200:
#     datas = response.json()

#     print(datas['dashboards'])

#     id = input("Entrez l'ID : ")

#     url += '/' + id
#     response = requests.get(url, auth=config)
#     dashboards = response.json()

#     for dashboard_item in dashboards['dashboardItems']:
#         dashboard_item_href = dashboard_item['href']
#         if dashboard_item['type'] == 'MAP':
#             item_uid = dashboard_item['map']['id']
#         elif dashboard_item['type'] == 'TEXT':
#             continue
#         else :
#             item_uid = dashboard_item['visualization']['id']

#         print(f"L'ID de la {dashboard_item['type']} est : {item_uid}")

#         item_dict = {item_uid: url_api + dashboard_item['type'].lower() + 's' + '/' + item_uid}
#         print(item_dict)

#         if not dashboard_item['type'] in dashboard_items.keys():
#             dashboard_items[dashboard_item['type']] = [item_dict]
#         else:
#             dashboard_items[dashboard_item['type']] += [item_dict]

#     print(dashboard_items)
#     get_item_infos(dashboard_items)

#     # get_resources()
# else:
#     print(f'Erreur {response.status_code} lors de la requête GET.')


# # response = requests.get("https://ministere-sante.mg/api/maps/z9fvd8eoGz3", auth=config).json()

# # statesData = {"type": "MAP", "features": []}

# # for mapView in response['mapViews']:
# #     ou = requests.get(mapView['href'] + "/organisationUnits?fields=name", auth=config).json()

# #     print(ou['organisationUnits'])

data = {
    "legends": [
        {"startValue": 80, "endValue": 100, "color": "#009427"},
        {"startValue": 0,"endValue": 20,"color": "#FF0000"},
        {"startValue": 60,"endValue": 80,"color": "#9DFF9C"},
        {"startValue": 20,"endValue": 40,"color": "#FEF98F"},
        {"startValue": 40,"endValue": 60,"color": "#fd8d3c"}
    ]
}

sorted_legends = sorted(data["legends"], key=lambda x: x["startValue"])

sorted_data = {"legends": sorted_legends}

def find_color(value, legends):
    for legend in legends:
        if legend["startValue"] <= value <= legend["endValue"]:
            return legend["color"]
    return None

# Exemple d'utilisation
input_value = float(input("entrez une valeur : "))  # Remplacez cette valeur par celle que vous avez en entrée
color_result = find_color(input_value, sorted_data["legends"])

if color_result:
    print(f"La couleur correspondante pour la valeur {input_value} est : {color_result}")
else:
    print(f"Aucune couleur correspondante trouvée pour la valeur {input_value}")