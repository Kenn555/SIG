// import '../jquery/jquery-3.7.1'

var content = $('.content');
var container = $('#grid-container') ;
var dataDashboard = {};
var curIdDashboard = idFirstDashboard;
var periods = [];

showElement();

getDashboardItem(curIdDashboard);


            
// Gestionnaire d'événement sur le bouton "Ajouter"
$('#add-btn').on('click', function() {
  // Récupération de la date sélectionnée
  var filterSelected = $('#filter').val();

  let period = filterSelected.split('-');
  period.reverse();
  periods.push(period.join(''));
  
  console.log(periods); // Cela affichera le résultat dans la console

  getDashboardItem(curIdDashboard);
  
  // Affichage de la date dans la console à titre d'exemple
  console.log('Date sélectionnée :', filterSelected);
});

// Gestionnaire d'événement sur le bouton "Rétablir"
$('#reset-btn').on('click', function() {

  $('input').val('').attr('placeholder', 'Filtre...');
  periods.length = 0;

  getDashboardItem(curIdDashboard);

});

async function validateAndSubmitForm() {
  // Récupérez les valeurs des champs du formulaire
  const nom = $('#lastname').val();
  const prenom = $('#firstname').val();
  const structure = $('#structure').val();
  const lieu_travail = $('#jobplace').val();
  const telephone = $('#phone').val();
  const email = $('#email').val();

  // Validez les champs du formulaire
  if (!nom || !structure || !lieu_travail || !telephone || !email) {
      return;
  }

  const dataForm = {query: 'form', datas:{
      nom: nom,
      prenom: prenom,
      structure: structure,
      lieu_travail: lieu_travail,
      telephone: telephone,
      email: email,
    }
  };

  console.log(dataForm);

  const responseForm = getDataFromServer(dataForm)

  console.log(responseForm);
  modal.remove();
  $('.modal-backdrop').remove();
}

async function getDataFromServer(data) {
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf_token,
      },
      body: JSON.stringify(data),
    });

    const dataJson = await response.json();
    return dataJson;
  } catch (error) {
    console.error('Erreur lors de la récupération des données :', error);
    throw error; // Rejeter l'erreur pour la gérer dans la fonction appelante
  }
}

async function showChart(keyRow, keyCol){
  var objetct  = $('#' + dataDashboard[keyRow][keyCol]['id']);
  objetct.find('.dropdown-menu').removeClass('show');
  objetct.find('.overflow-auto').remove();
  var loading = $('#spinner').clone();
  loading.show();

  objetct.append(loading);

  var chart = $('<canvas></canvas>');
  chart.attr('id', 'Item-' + dataDashboard[keyRow][keyCol]['id']);
  var ctx = chart[0].getContext('2d');

  
  if (periods.length !== 0){
    var data = { query: 'chart', datas: dataDashboard[keyRow][keyCol], filter: periods };
    console.log('Filtered');
  }else{
    var data = { query: 'chart', datas: dataDashboard[keyRow][keyCol]};
    console.log('Normal');
  }

  var chartData = await getDataFromServer(data);

  objetct.append($('<div class="container overflow-auto justify-content-center align-items-center" style="max-width: 580px; max-height: 300px; margin: 0px"></div>').append(chart));

  console.log(chartData);

  var chartItem = new Chart(ctx, {
        type: chartData.type,
        data: chartData,
        options: {
            scales: {
                x: {
                    beginAtZero: false,
                    grid: {
                        display: false // Enlève les grilles sur l'axe x
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        display: true // affiche les grilles sur l'axe y
                    }
                }
            },
            plugins: {
              labels: {
                render: 'value'
              },
                legend: {
                    display: true,
                    position: 'top'
                },
                annotation: {
                  annotations: [{
                    type: 'line',
                    mode: 'horizontal',
                    scaleID: 'y',
                    borderColor: 'black', // Couleur de la ligne
                    borderWidth: 1, // Largeur de la ligne
                    label: {
                      display: true,
                      color: 'black',
                      backgroundColor: 'transparent',
                      borderColor: 'transparent',
                      position: 'start',
                      yAdjust: -10,
                      yAdjust: -10,
                    }
                  }]
                },
            }
        }
    });
    
    if (curIdDashboard === "yyVWGbDnVho"){
      chartItem.options.scales.y.max = 150;
    };

    if (chartData.type === 'bar' && 'annotation' in chartData){
      chartItem.options.plugins.annotation.annotations[0].value = chartData.annotation[0].value; // La valeur cible que vous souhaitez représenter
      chartItem.options.plugins.annotation.annotations[0].label.content = chartData.annotation[0].label; // Libellé facultatif = 85; // La valeur cible que vous souhaitez représenter
    };

    chartItem.update();

    objetct.find('.spinner-border').remove();
    objetct.find('.dropdown-item').prop('disabled', false);

    $('#' + dataDashboard[keyRow][keyCol]['id']).parent('.col-md').remove(loading);

}

async function showTable(keyRow, keyCol){
  
  var objetct  = $('#' + dataDashboard[keyRow][keyCol]['id']);

  objetct.find('.overflow-auto').remove();
  var loading = $('#spinner').clone();
  loading.show();
  objetct.append(loading);

  var table = $('#monTableau').clone();
  table.attr('id', 'Item-' + dataDashboard[keyRow][keyCol]['id']);
  table.show();

  if (periods.length !== 0){
    var data = { query: 'reportTable', datas: dataDashboard[keyRow][keyCol], filter: periods };
    console.log('Filtered');
  }else{
    var data = { query: 'reportTable', datas: dataDashboard[keyRow][keyCol]};
    console.log('Normal');
  }

    var dataItem = await getDataFromServer(data);
    console.log('ShowTable : ' + dataDashboard[keyRow][keyCol] + objetct.html());
    console.log(data);
    console.log(dataItem);
    objetct.find('.overflow-auto').remove();
    objetct.append($('<div class="container overflow-auto justify-content-center align-items-center" style="max-width: 580px; max-height: 300px; margin: 0px"></div>').append(table));
    console.log(dataItem['data']);
    console.log(dataItem['columns']);

    table.DataTable({
      // columnDefs: [{ orderable: false, targets: 0 }],
      "data": dataItem['data'],
      "columns": dataItem['columns']
  });

    objetct.find('.spinner-border').remove();
    $('#' + dataDashboard[keyRow][keyCol]['id']).parent('.col-md').remove(loading);

}

async function getDashboardItem(idDashboardItem) {
  var overlay = $('<div class="d-flex justify-content-center align-items-center overlay position-absolute" style="z-index: 8;">\
    <div class="spinner-border text-primary" role="status" style="width: 7rem; height: 7rem;">\
      <span class="visually-hidden">Loading...</span>\
    </div>\
  </div>');
  $('.section').prepend(overlay);
  $('.menu-btn').removeClass('bg-primary fw-bold text-white');
  $('#' + idDashboardItem).addClass('bg-primary fw-bold text-white');


    $("#titleDashboardItem").text($('#' + idDashboardItem).text())

    if (periods.length !== 0){
      var data = { query: 'dashboardItem', datas: idDashboardItem, filter: periods };
      console.log('Filtered')
    }else{
      var data = { query: 'dashboardItem', datas: idDashboardItem };
      console.log('Normal')
    }

    console.log(data);

    dataDashboard = await getDataFromServer(data);

    container.children().html("");

    console.log(dataDashboard); //{0: Array(3), 1: Array(3), 2: Array(3), 3: Array(1)}
    for (rowKey in dataDashboard){
      // console.log(dataJson[rowKey]); // <= Array(3) trois colonnes par ligne
      var row = $('<div class="row"></div>');
      for (colKey in dataDashboard[rowKey]){ 
        // console.log(dataJson[rowKey][colKey]);
        
        var col = $('<div class="col-md bg-light text-dark m-1"><div id="' + dataDashboard[rowKey][colKey]['id'] + '"  class="container border rounded-3 bg-white justify-content-center align-items-center" style="max-width: 580px; min-height: 350px; padding: 0px; position: relative"></div></div>');
        
        // Ajouter le titre à gauche
        col.children('div').append($('<div class="container d-flex bg-light rounded-top-3 py-1"></div>')
        .append($('<div class="mr-auto text-truncate" style="display: inline-block; text-align: left; max-width: 80%;" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-custom-class="custom-tooltip" title="' + dataDashboard[rowKey][colKey]['name'] + '"> <b>' + dataDashboard[rowKey][colKey]['name'] + '</b></div>')));
        
        // Ajouter le bouton dropdown à droite
        var dropdown = $('#option-btn').clone();

        // Ajouter un nouvel attribut onclick aux éléments de la classe dropdown-item
        dropdown.find('#reportTable').attr('onclick', 'showTable(' + rowKey + ', ' + colKey + ')');
        dropdown.find('#chart').attr('onclick', 'showChart(' + rowKey + ', ' + colKey + ')');
        dropdown.find('#map').attr('onclick', 'showMap(' + rowKey + ', ' + colKey + ')');

        dropdown.show();
        dropdown.css('margin: 0 5px'); // Apparaitre et Ajuster la marge
        col.children('div').children('.container').append(dropdown);
          
        // Ajouter le conteneur au gd-container
        $('#gd-container').append(container);

        row.append(col);
      }
      container.append(row);
      content.children('h3').text($('#' + idDashboardItem).text());
    }

    overlay.remove();
    for (rowKey in dataDashboard){
      for (colKey in dataDashboard[rowKey]){
        console.log()
        if (dataDashboard[rowKey][colKey]['type'] === "VISUALIZATION"){
          showChart(rowKey, colKey);
        } else if (dataDashboard[rowKey][colKey]['type'] === "pivot_table") {
          showTable(rowKey, colKey);
        } else if(dataDashboard[rowKey][colKey]['type'] === "MAP") {
          showMap(rowKey, colKey);
        }
      }
    }

}

function showElement() {
  $('button.menu-btn').on('click', function () {
    curIdDashboard = $(this).attr('id');

    getDashboardItem(curIdDashboard)

    // Afficher le contenu dans la div avec la classe 'content'
    

    // Utiliser la syntaxe async/await pour gérer les appels asynchrones de fetch
    
  });
}

async function showMap(keyRow, keyCol){
  
  var objetct  = $('#' + dataDashboard[keyRow][keyCol]['id']);

  objetct.find('.overflow-auto').remove();
  var loading = $('#spinner').clone();
  loading.show();
  objetct.append(loading);

  var map_ = $('<div></div>');

  map_.attr('id', 'Item-' + dataDashboard[keyRow][keyCol]['id']);
  map_.css('width','575px')
  map_.css('height','300px')

  if (periods.length !== 0){
    var data = { query: 'map', datas: dataDashboard[keyRow][keyCol], filter: periods };
    console.log('Filtered');
  }else{
    var data = { query: 'map', datas: dataDashboard[keyRow][keyCol]};
    console.log('Normal');
  }

    var statesData = await getDataFromServer(data);
    console.log('ShowMap : ' + dataDashboard[keyRow][keyCol] + objetct.html());
    console.log(data);
    console.log(statesData);
    objetct.append($('<div class="container overflow-auto justify-content-center align-items-center" style="max-width: 580px; max-height: 300px; margin: auto; padding:0px"></div>').append(map_));

  /*===================================================
                        OSM  LAYER               
  ===================================================*/

  console.log(statesData.center);
  var map = L.map(map_.attr('id')).setView(statesData.center, 6);
  var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  });
  osm.addTo(map);

  /*===================================================
                       TILE LAYER               
  ===================================================*/
  
  var CartoDB_DarkMatter = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
  subdomains: 'abcd',
    maxZoom: 19
  });
  CartoDB_DarkMatter.addTo(map);
  
  // Google Map Layer
  
  googleStreets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',{
      maxZoom: 20,
      subdomains:['mt0','mt1','mt2','mt3']
   });
   googleStreets.addTo(map);
  
   // Satelite Layer
  googleSat = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{
     maxZoom: 20,
     subdomains:['mt0','mt1','mt2','mt3']
   });
  googleSat.addTo(map);
  
  var Stamen_Watercolor = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.{ext}', {
   attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  subdomains: 'abcd',
  minZoom: 1,
  maxZoom: 16,
  ext: 'jpg'
  });
  Stamen_Watercolor.addTo(map);

  /*===================================================
                        LAYER CONTROL               
  ===================================================*/
  
  var baseLayers = {
      "Satellite":googleSat,
      "Google Map":googleStreets,
      "Water Color":Stamen_Watercolor,
      "OpenStreetMap": osm,
  };
  
  L.control.layers(baseLayers).addTo(map);
  
  /*===================================================
                        Choropleth Map               
  ===================================================*/
  
  L.geoJSON(statesData).addTo(map);
  
  
  function getColor(d) {
      return d > 100 ? '#800026' :
             d > 96.2  ? '#BD0026' :
             d > 92.4  ? '#E31A1C' :
             d > 88.6  ? '#FC4E2A' :
             d > 84.8   ? '#FEB24C' :
             d > 81   ? '#FED976' :
                        '#FFEDA0';
  }
  
  function style(feature) {
      return {
          fillColor: getColor(feature.properties.density),
          weight: 2,
          opacity: 1,
          color: 'white',
          dashArray: '3',
          fillOpacity: 0.7
      };
  }
  
  L.geoJson(statesData, {style: style}).addTo(map);
  
  function highlightFeature(e) {
      var layer = e.target;
  
      layer.setStyle({
          weight: 3,
          color: '#777',
          dashArray: '',
          fillOpacity: 0.7
      });
  
      // if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
      //     layer.bringToFront();
      // }
  
      info.update(layer.feature.properties);
  }
  
  function resetHighlight(e) {
      geojson.resetStyle(e.target);
      info.update();
  }
  
  var geojson;
  // ... our listeners
  geojson = L.geoJson(statesData);
  
  function zoomToFeature(e) {
      map.fitBounds(e.target.getBounds());
  }
  
  function onEachFeature(feature, layer) {
      layer.on({
          mouseover: highlightFeature,
          mouseout: resetHighlight,
          click: zoomToFeature
      });
  }
  
  geojson = L.geoJson(statesData, {
      style: style,
      onEachFeature: onEachFeature
  }).addTo(map);
  
  var info = L.control();
  
  info.onAdd = function (map) {
      this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
      this.update();
      return this._div;
  };
  
  // method that we will use to update the control based on feature properties passed
  info.update = function (props) {
      this._div.innerHTML = (props ?
          '<b>' + props.name + '</b><br/>' + props.density
          : 'Survoler la zone');
  };
  
  info.addTo(map);
  
  var legend = L.control({position: 'bottomright'});
  
  legend.onAdd = function (map) {
  
      var div = L.DomUtil.create('div', 'info legend'),
          grades = [81, 84.8, 88.6, 92.4, 96.2, 100],
          labels = [];
  
      // loop through our density intervals and generate a label with a colored square for each interval
      for (var i = 0; i < grades.length; i++) {
          div.innerHTML +=
              '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
              grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
      }
  
      return div;
  };
  
  legend.addTo(map);

  objetct.find('.spinner-border').remove();
  
    $('#' + dataDashboard[keyRow][keyCol]['id']).parent('.col-md').remove(loading);
}