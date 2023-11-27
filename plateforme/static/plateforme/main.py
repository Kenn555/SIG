# response = {
#   "headers": [
#     {
#       "name": "pe",
#       "column": "Period",
#       "valueType": "TEXT",
#       "type": "java.lang.String",
#       "hidden": False,
#       "meta": True
#     },
#     {
#       "name": "ou",
#       "column": "Organisation unit",
#       "valueType": "TEXT",
#       "type": "java.lang.String",
#       "hidden": False,
#       "meta": True
#     },
#     {
#       "name": "value",
#       "column": "Value",
#       "valueType": "NUMBER",
#       "type": "java.lang.Double",
#       "hidden": False,
#       "meta": False
#     }
#   ],
#   "metaData": {
#     "items": {
#       "IsROud9LtOF": { "name": "Amparafaravola" },
#       "mQEM6Pdzg8p.REPORTING_RATE": {
#         "name": "Nouveau Formulaire RMA CSB - Reporting rate"
#       },
#       "202309": { "name": "Septembre 2023" },
#       "CjWDQW1TaaX": { "name": "Moramanga" },
#       "ou": { "name": "Organisation unit" },
#       "JChr4ml1sQq": { "name": "Anosibe An'ala" },
#       "202307": { "name": "Juillet 2023" },
#       "202308": { "name": "Août 2023" },
#       "202305": { "name": "Mai 2023" },
#       "202306": { "name": "Juin 2023" },
#       "202310": { "name": "Octobre 2023" },
#       "LAST_6_MONTHS": { "name": "6 derniers mois" },
#       "RGATf8waYNn": { "name": "Andilamena" },
#       "dx": { "name": "Data" },
#       "pe": { "name": "Period" },
#       "sSDIBMoRBPf": { "uid": "sSDIBMoRBPf", "name": "District" },
#       "MskGiUGbWJ8": {
#         "uid": "MskGiUGbWJ8",
#         "code": "33",
#         "name": "Alaotra Mangoro"
#       },
#       "lsCrRfgm2hS": { "name": "Ambatondrazaka" }
#     },
#     "dimensions": {
#       "dx": ["mQEM6Pdzg8p.REPORTING_RATE"],
#       "pe": ["202305", "202306", "202307", "202308", "202309", "202310"],
#       "ou": [
#         "lsCrRfgm2hS",
#         "IsROud9LtOF",
#         "RGATf8waYNn",
#         "JChr4ml1sQq",
#         "CjWDQW1TaaX"
#       ],
#       "co": []
#     }
#   },
#   "rows": [
#     ["202308", "lsCrRfgm2hS", "95.7"],
#     ["202309", "lsCrRfgm2hS", "97.1"],
#     ["202306", "lsCrRfgm2hS", "98.5"],
#     ["202305", "lsCrRfgm2hS", "98.5"],
#     ["202309", "RGATf8waYNn", "100"],
#     ["202305", "IsROud9LtOF", "100"],
#     ["202310", "JChr4ml1sQq", "0"],
#     ["202307", "IsROud9LtOF", "100"],
#     ["202308", "IsROud9LtOF", "100"],
#     ["202307", "RGATf8waYNn", "95.2"],
#     ["202308", "RGATf8waYNn", "90.5"],
#     ["202306", "IsROud9LtOF", "100"],
#     ["202307", "lsCrRfgm2hS", "97.1"],
#     ["202309", "CjWDQW1TaaX", "100"],
#     ["202309", "JChr4ml1sQq", "95.8"],
#     ["202308", "JChr4ml1sQq", "91.7"],
#     ["202308", "CjWDQW1TaaX", "100"],
#     ["202309", "IsROud9LtOF", "100"],
#     ["202306", "RGATf8waYNn", "100"],
#     ["202306", "CjWDQW1TaaX", "100"],
#     ["202307", "CjWDQW1TaaX", "100"],
#     ["202305", "RGATf8waYNn", "100"],
#     ["202305", "CjWDQW1TaaX", "98.6"],
#     ["202310", "CjWDQW1TaaX", "0"],
#     ["202306", "JChr4ml1sQq", "100"],
#     ["202310", "IsROud9LtOF", "17.1"],
#     ["202305", "JChr4ml1sQq", "95.8"],
#     ["202307", "JChr4ml1sQq", "91.7"],
#     ["202310", "RGATf8waYNn", "0"],
#     ["202310", "lsCrRfgm2hS", "0"]
#   ],
#   "height": 30,
#   "width": 3,
#   "headerWidth": 3
# }

# response['headers']
# response['metaData'] # items dimensions
# # items 
# # dimensions [dx, pe, ou, co]
# response['rows']

# columns = []
# data = []
# col_titles = []
# result = []

# ###### column_titles ####### response['headers'][0][]
# if len(response['headers']) > 2:
#     col_titles += ['#0']
#     columns = [{"data": '#0', "title": ''}]
#     for row in response['metaData']['dimensions'][response['headers'][1]['name']]:
#         data += [{row: response['metaData']['items'][row]['name']}]
#     if response['headers'][1]['name'] == 'ou':
#         response['metaData']['dimensions'][response['headers'][1]['name']].sort()

#     for info in data:
#         lieu_resultat = {'#0': list(info.items())[0][1]}
#         for row in response['rows']:
#             if row[1] == list(info.items())[0][0]:
#                 lieu_resultat[row[0]] = row[-1]
#         result.append(lieu_resultat)

# col_titles += [col_title for col_title in response['metaData']['dimensions'][response['headers'][0]['name']]]
# for column in response['metaData']['dimensions'][response['headers'][0]['name']]:
#     columns += [{"data": column, "title": response['metaData']['items'][column]['name']}]
# print(col_titles)

# print(data)

# result += [{row[0]: row[-1]} for row in response['rows']]

# # Affichage du résultat
# print(result)


response = {
  "lastUpdated": "2021-08-11T20:26:40.055",
  "href": "https://play.dhis2.org/2.37.10/api/visualizations/xiLNqnSaWP3",
  "id": "xiLNqnSaWP3",
  "created": "2021-08-11T20:26:40.055",
  "name": "ANC: Coverage by quarter and district (two-category)",
  "legend": { "showKey": False },
  "publicAccess": "--------",
  "userOrganisationUnitChildren": False,
  "type": "COLUMN",
  "hideEmptyColumns": False,
  "subscribed": False,
  "userOrganisationUnit": False,
  "rowSubTotals": False,
  "cumulativeValues": False,
  "showDimensionLabels": False,
  "sortOrder": 0,
  "fontSize": "NORMAL",
  "favorite": False,
  "topLimit": 0,
  "userOrganisationUnitGrandChildren": False,
  "displayName": "ANC: Coverage by quarter and district (two-category)",
  "percentStackedValues": False,
  "noSpaceBetweenColumns": False,
  "showHierarchy": False,
  "seriesKey": { "hidden": False },
  "hideTitle": False,
  "colorSet": "DEFAULT",
  "skipRounding": False,
  "showData": True,
  "fixRowHeaders": False,
  "numberType": "VALUE",
  "hideEmptyRows": False,
  "parentGraphMap": {
    "jUb8gELQApl": "ImspTQPwCqd",
    "PMa2VCrupOd": "ImspTQPwCqd",
    "O6uvpzGd5pu": "ImspTQPwCqd",
    "lc3eMKXaEfw": "ImspTQPwCqd",
    "fdc6uOvgoji": "ImspTQPwCqd"
  },
  "displayDensity": "NORMAL",
  "regressionType": "NONE",
  "completedOnly": False,
  "colTotals": False,
  "displayFormName": "ANC: Coverage by quarter and district (two-category)",
  "hideEmptyRowItems": "NONE",
  "aggregationType": "DEFAULT",
  "hideSubtitle": False,
  "hideLegend": False,
  "fixColumnHeaders": False,
  "externalAccess": False,
  "colSubTotals": False,
  "rowTotals": False,
  "digitGroupSeparator": "SPACE",
  "regression": False,
  "fontStyle": {},
  "access": {
    "read": False,
    "update": False,
    "externalize": True,
    "delete": False,
    "write": False,
    "manage": False
  },
  "reportingParams": {
    "parentOrganisationUnit": False,
    "reportingPeriod": False,
    "organisationUnit": False,
    "grandParentOrganisationUnit": False
  },
  "lastUpdatedBy": {
    "displayName": "Tom Wakiki",
    "name": "Tom Wakiki",
    "id": "GOLswS44mh8",
    "username": "system"
  },
  "sharing": {
    "owner": "GOLswS44mh8",
    "external": False,
    "public": "--------"
  },
  "relativePeriods": {
    "thisYear": False,
    "quartersLastYear": False,
    "last10Years": False,
    "last30Days": False,
    "last52Weeks": False,
    "thisWeek": False,
    "last90Days": False,
    "last60Days": False,
    "lastMonth": False,
    "last14Days": False,
    "biMonthsThisYear": False,
    "monthsThisYear": False,
    "last2SixMonths": False,
    "yesterday": False,
    "thisQuarter": False,
    "last12Months": False,
    "last5FinancialYears": False,
    "thisSixMonth": False,
    "lastQuarter": False,
    "thisFinancialYear": False,
    "last4Weeks": False,
    "last3Months": False,
    "thisDay": False,
    "thisMonth": False,
    "last5Years": False,
    "last6BiMonths": False,
    "last10FinancialYears": False,
    "last4BiWeeks": False,
    "lastFinancialYear": False,
    "lastBiWeek": False,
    "weeksThisYear": False,
    "last6Months": False,
    "last3Days": False,
    "quartersThisYear": False,
    "monthsLastYear": False,
    "lastWeek": False,
    "last7Days": False,
    "last180Days": False,
    "thisBimonth": False,
    "lastBimonth": False,
    "lastSixMonth": False,
    "thisBiWeek": False,
    "lastYear": False,
    "last12Weeks": False,
    "last4Quarters": True
  },
  "createdBy": {
    "displayName": "Tom Wakiki",
    "name": "Tom Wakiki",
    "id": "GOLswS44mh8",
    "username": "system"
  },
  "user": {
    "displayName": "Tom Wakiki",
    "name": "Tom Wakiki",
    "id": "GOLswS44mh8",
    "username": "system"
  },
  "dataElementGroupSetDimensions": [],
  "axes": [],
  "attributeDimensions": [],
  "translations": [],
  "yearlySeries": [],
  "filterDimensions": [],
  "interpretations": [],
  "userGroupAccesses": [],
  "subscribers": [],
  "optionalAxes": [],
  "columns": [{ "id": "dx" }],
  "dataElementDimensions": [],
  "periods": [],
  "categoryDimensions": [],
  "rowDimensions": ["pe", "ou"],
  "series": [],
  "itemOrganisationUnitGroups": [],
  "programIndicatorDimensions": [],
  "attributeValues": [],
  "columnDimensions": ["dx"],
  "userAccesses": [],
  "favorites": [],
  "dataDimensionItems": [
    {
      "dataDimensionItemType": "INDICATOR",
      "indicator": { "id": "Uvn6LCg7dVU" }
    },
    {
      "dataDimensionItemType": "INDICATOR",
      "indicator": { "id": "OdiHJayrsKo" }
    }
  ],
  "categoryOptionGroupSetDimensions": [],
  "organisationUnitGroupSetDimensions": [],
  "organisationUnitLevels": [],
  "organisationUnits": [
    { "id": "O6uvpzGd5pu" },
    { "id": "fdc6uOvgoji" },
    { "id": "lc3eMKXaEfw" },
    { "id": "jUb8gELQApl" },
    { "id": "PMa2VCrupOd" }
  ],
  "filters": [],
  "rows": [{ "id": "pe" }, { "id": "ou" }]
}


type_item = items['type']

if type_item == "VISUALIZATION":
        dimension_parameter = {'columns': [],'rows': [],'filters': []}
        for key in dimension_parameter:
            if len(response[key]) != 0:
                url = href_item + '/' + key
                dimension_datas = requests.get(url, auth=config).json()
                for type_dimension in dimension_datas[key]:
                    value_dimension = []
                    try:
                        value_dimension += [item['id'] for item in type_dimension['items']] if type_dimension['id'] != 'dx' else [item['reportingRate']['dimensionItem'] for item in response['dataDimensionItems']]
                    except KeyError:
                        value_dimension += [item['id'] for item in type_dimension['items']]
                    dimension_parameter[key].append({type_dimension['id']: value_dimension})
        print(dimension_parameter)