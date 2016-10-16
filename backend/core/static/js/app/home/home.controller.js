(function () {
  'use strict';

  angular
      .module('app')
      .controller('HomeController', HomeController);

  HomeController.$inject = ['dataService', 'uiGmapGoogleMapApi', '$scope'];

  function HomeController(dataService, uiGmapGoogleMapApi, $scope) {
    var vm = this;
    var clusterStyles = [{}];
    vm.reportss = []
    clusterStyles = [
      {'sentReports':
        {
          url: 'https://raw.githubusercontent.com/googlemaps/v3-utility-library/master/markerclustererplus/images/m1.png',
          height: 27,
          width: 30,
          anchor: [3, 0],
          offsetX: 40,
          offsetY: 40
        }
      },
      {'notResolvedReports':
        {
          url: 'https://raw.githubusercontent.com/googlemaps/v3-utility-library/master/markerclustererplus/images/m2.png',
          height: 36,
          width: 40,
          anchor: [6, 0],
          offsetX: 40,
          offsetY: 40
        }
      },
      {'resolvedReports':
        {
          url: 'https://raw.githubusercontent.com/googlemaps/v3-utility-library/master/markerclustererplus/images/m3.png',
          width: 50,
          height: 45,
          anchor: [9, 0],
          offsetX: 40,
          offsetY: 40
        }
      }
    ];
        var clusterStyless = [
        {
            url: 'https://raw.githubusercontent.com/googlemaps/v3-utility-library/master/markerclustererplus/images/m1.png',
            height: 27,
            width: 30,
            anchor: [3, 0],
            textColor: '#11ffbb',
            textSize: 10,
            offsetX: 20,
            offsetY: 20
          }, {
            url: 'https://raw.githubusercontent.com/googlemaps/v3-utility-library/master/markerclustererplus/images/m2.png',
            height: 36,
            width: 40,
            anchor: [6, 0],
            textColor: '#ff0000',
            textSize: 11,
            offsetX: 20,
            offsetY: 20
          }, {
            url: 'https://raw.githubusercontent.com/googlemaps/v3-utility-library/master/markerclustererplus/images/m3.png',
            width: 50,
            height: 45,
            anchor: [8, 0],
            textSize: 12,
            offsetX: 20,
            offsetY: 20
          }
        ];
    vm.title = 'HomeController';
    vm.reports = {
      'sentReports': [],
      'notResolvedReports': [],
      'resolvedReports': []
    };
    vm.map = {
      center: {latitude: -19.73639, longitude: -45.25222},
      zoom: 14,
      sentReportsMCOpt: {
        gridSize: 20,
        styles: clusterStyless,
        maxZoom: 14,
        minimumClusterSize: 2
      },
      notResolvedReportsMCOpt: {
        gridSize: 20,
        styles: clusterStyless,
        maxZoom: 14,
        minimumClusterSize: 2
      },
      resolvedReportsMCOpt: {
        gridSize: 20,
        styles: clusterStyless,
        maxZoom: 14,
        minimumClusterSize: 2
      },
      clusterOpt: {
        gridSize: 40, ignoreHidden: true, minimumClusterSize: 4, minZoom: 14, maxZoom: 14,
        styles:    [{
          textColor: 'white',
          url: 'http://s15.postimg.org/fuaqrrot3/rsz_cluster_resize.png',
          height: 40,
          width: 40,
          textSize: 11,
          fontWeight: 'normal'
        }]
      },

      circleOpt: {
        id: 1,
        center: {latitude: -19.73639, longitude: -45.25222},
        radius: 100,
        stroke: {
          color: '#08B21F',
          weight: 2,
          opacity: 1
        },
        fill: {
          color: '#08B21F',
          opacity: 0.5
        },
        geodesic: false,
        draggable: false,
        clickable: false,
        editable: false,
        visible: true
      },

      options: {
        mapTypeControl: false,
        mapScaleControl: false,
        streetViewControl: false,
        maxZoom: 15,
        minZoom: 14,
        scrollwheel: false
      },
      showHeat: true,
      heatLayerCallback: function (layer) {
          var mockHeatLayer = new MockHeatLayer(layer);
      },

    };
            var opt = {
                "legend": {
                    "Fatal" : "#FF0066",
                    "Very serious injuries" : "#FF9933",
                    "Serious injuries" : "#FFFF00" ,
                    "Minor injuries" : "#99FF99",
                    "No injuries" : "#66CCFF",
                    "Not recorded" : "#A5A5A5"
                }
            };

    vm.reportsChartConfig = {
      options: {
        chart: {
          type: 'pie'
        },

        tooltip: {
          pointFormat: "{series.name}: <b> {point.percentage:.2f}%</b>"
        },

        plotOptions: {
          pie: {
            cursor: 'pointer',
            dataLabels: {
              enabled: false
            },
            allowPointSelect: false,
            showInLegend: true,
            point: {
              events: {
                legendItemClick: function (e) {
                  e.preventDefault();
                }
              }
            }
          }
        }
      },

      series: [{
        name: 'Nº de Denúncias',
        colorByPoint: true,
        data: []
      }],

      title: {
        text: 'Histórico Atual de Denúncias de Criadouros do Aedes Aegypti da Cidade Bom Despacho'
      }


    };

    activate();

    ////////////////

    function activate() {
      console.log('Hello HomeController');

      return getReports().then(function (_) {
        calculatePercentage();

        // getCenterMarkers();
      })
    }

    function getReports() {
      return dataService.getReports()
          .then(function(data) {

            angular.forEach(data, function (report){

              switch(report.status){
                case 1:

                  // vm.reportss.push({'id': report.id, 'title': 'Leo', 'latitude': report.latitude, 'longitude': report.longitude, 'name': 'Enviadas'})
                  vm.reportss.push({location: new google.maps.LatLng(report.latitude, report.longitude), weight: 500})
                  vm.reports.sentReports.push(report);
                  // var marker1 = new google.maps.Marker({
                  //   position: new google.maps.LatLng(report.latitude, report.longitude),
                  //   title: "Perigo"
                  // });
                  //   vm.reportss.push(marker1)
                  break;
                case 2:
                  vm.reportss.push({location: new google.maps.LatLng(report.latitude, report.longitude), weight: 1000})
                  // vm.reportss.push({'id': report.id, 'title': 'Carmen', 'latitude': report.latitude, 'longitude': report.longitude, 'name': 'Não resolvidas'})
                  vm.reports.notResolvedReports.push(report);
                  // var marker2 = new google.maps.Marker({
                  //   position: new google.maps.LatLng(report.latitude, report.longitude),
                  //   title: "Pau quebra"
                  // });
                  // vm.reportss.push(marker2)
                  break;
                case 3:
                case 4:
                  // vm.reportss.push({location: new google.maps.LatLng(report.latitude, report.longitude), weight: 5000})
                  // vm.reportss.push({'id': report.id, 'title': 'Lucas','latitude': report.latitude, 'longitude': report.longitude, 'name': 'Resolvido'})

                  vm.reports.resolvedReports.push(report);
                  // var marker = new google.maps.Marker({
                  //   position: new google.maps.LatLng(report.latitude, report.longitude),
                  //   title: "Jones"
                  // });
                  // vm.reportss.push(marker)
                  break;

              }
            });
                // uiGmapGoogleMapApi.then(function(maps) {
                //   google.load("visualization", "1", {packages: ["corechart"]});
                //   google.setOnLoadCallback(initialize);
                // });

              // $scope.$on('mapInitialized', function(event, args) {
              //   var map = args[0]
              //   console.log(map)
              //  var markerCluster = new MarkerClusterer(map, vm.reportss, opt)

              // });

            // angular.forEach(data, function (report){
            //   switch(report.status){
            //     case 1:
            //       vm.reports.sentReports.push(report);
            //       break;
            //     case 2:
            //       vm.reports.notResolvedReports.push(report);
            //       break;
            //     case 3:
            //     case 4:
            //       vm.reports.resolvedReports.push(report);
            //       break;
            //   }
            // });
            return data;
          });

    }

    // function getCenterMarkers(){
    //   uiGmapGoogleMapApi.then(function(maps) {
    //      var bounds = new maps.LatLngBounds();
    //      for (var i = 0; i < vm.reports.length; i++) {
    //         bounds.extend(new maps.LatLng(vm.reports[i].latitude, vm.reports[i].longitude));
    //     }
    //     vm.map.bounds = bounds;
    //     console.log(bounds)
    //   });
    // }

    function calculatePercentage() {
      var totalReports = vm.reports.notResolvedReports.length + vm.reports.resolvedReports.length +
          vm.reports.sentReports.length;

      var results = dataService.calculatePercentage(
          [vm.reports.sentReports.length, vm.reports.notResolvedReports.length,
            vm.reports.resolvedReports.length], totalReports
      );

      vm.reportsChartConfig.series[0].data = [{
        name: 'Enviadas',
        y: results[0],
        color: '#EEEEEE'
      }, {
        name: 'Em análise',
        y: results[1],
        color: '#7F2B11'
      }, {
        name: 'Resolvidas',
        y: results[2],
        color: '#FF5722'
      }];
    }


    function MockHeatLayer(heatLayer) {
      heatLayer.set('radius', 20)
      heatLayer.set('opacity', 0.75)
      var pointArray = new google.maps.MVCArray(vm.reportss);
      heatLayer.setData(pointArray)

    }
  }

})();

