(function () {
  'use strict';

  angular
      .module('app')
      .controller('HomeController', HomeController);

  HomeController.$inject = ['dataService', '$timeout', 'uiGmapGoogleMapApi', 'uiGmapIsReady'];

  function HomeController(dataService,  $timeout, uiGmapGoogleMapApi, uiGmapIsReady) {
    var vm = this;
    
    vm.title = 'HomeController';
    vm.reports = {
      'sentReports': [],
      'notResolvedReports': [],
      'resolvedReports': []
    };
    //     styles:    [{
    //   textColor: 'white',
    //   url: 'http://s15.postimg.org/fuaqrrot3/rsz_cluster_resize.png',
    //   height: 40,
    //   width: 40,
    //   textSize: 11,
    //   fontWeight: 'normal'
    // }]
    vm.map = {
      center: {latitude: -19.73639, longitude: -45.25222},
      zoom: 14,
      options: {
        mapTypeControl: false,
        mapScaleControl: false,
        streetViewControl: false,
        maxZoom: 15,
        minZoom: 14,
        scrollwheel: false
      },
      showHeat: false,
      heatLayerCallback: function (layer) {
        var mockHeatLayer = new MockHeatLayer(layer);
      }
    };

    vm.reportsChartConfig = {
      options: {
        chart: {
          type: 'pie'
        },

        tooltip: {
          pointFormat: "{series.name}: <b> {point.num_reports} </b> " +
          "<br/><b>{point.percentage:.2f}%</b> "
        },

        plotOptions: {
          pie: {
            cursor: 'pointer',
            dataLabels: {
              enabled: true,
              format: '<b>{point.name}</b>: {point.percentage:.2f} %',
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
      return getReports().then(function (_) {
        calculatePercentage();
      })
    }

    function getReports() {
      return dataService.getReports()
          .then(function (data) {
            angular.forEach(data, function (report) {
              switch (report.status) {
                // Enviadas
                case 1:
                  vm.reports.sentReports.push({
                    location: new google.maps.LatLng(report.latitude, report.longitude),
                    weight: 40
                  });
                  break;
                // Em análise
                case 2:
                  vm.reports.notResolvedReports.push({
                    location: new google.maps.LatLng(report.latitude, report.longitude),
                    weight: 100
                  });
                  break;
                // Foco tratado ou não encontrado
                case 3:
                case 4:
                  vm.reports.resolvedReports.push({location: new google.maps.LatLng(report.latitude, report.longitude)});
                  break;

              }
            });
            return data;
          });

    }

    function calculatePercentage() {
      var totalReports = vm.reports.notResolvedReports.length + vm.reports.resolvedReports.length +
          vm.reports.sentReports.length;

      var results = dataService.calculatePercentage(
          [vm.reports.sentReports.length, vm.reports.notResolvedReports.length,
            vm.reports.resolvedReports.length], totalReports
      );

      vm.reportsChartConfig.series[0].data = [{
        name: 'Enviadas',
        num_reports: vm.reports.sentReports.length,
        y: results[0],
        color: '#EEEEEE'
      }, {
        name: 'Em análise',
        num_reports: vm.reports.notResolvedReports.length,
        y: results[1],
        color: '#7F2B11'
      }, {
        name: 'Resolvidas',
        num_reports: vm.reports.resolvedReports.length,
        y: results[2],
        color: '#FF5722'
      }];
    }

    uiGmapGoogleMapApi.then(function(maps) {
      vm.map.showHeat = true;
    });

    function MockHeatLayer(heatLayer) {
      // Apenas denúncias que foram enviadas e as queestão em analise
      var data = vm.reports.sentReports.concat(vm.reports.notResolvedReports);
      var gradient = [
        'rgba(229, 153, 0, 0)',
        'rgba(231, 140, 0, 1)',
        'rgba(233, 128, 1, 1)',
        'rgba(235, 116, 2, 1)',
        'rgba(237, 103, 3, 1)',
        'rgba(239, 91, 4, 1)',
        'rgba(242, 79, 5, 1)',
        'rgba(244, 66, 5, 1)',
        'rgba(246, 54, 6, 1)',
        'rgba(248, 42, 7, 1)',
        'rgba(127, 57, 51, 1)',
        'rgba(252, 17, 9, 1)',
        'rgba(255, 5, 10, 1)',
        'rgba(255, 0, 0, 1)'
      ];
      heatLayer.set('gradient', heatLayer.get('gradient') ? null : gradient);
      heatLayer.set('radius', 20);
      heatLayer.set('opacity', 1);
      // $timeout(function () {
      uiGmapIsReady.promise().then(function(instances){
        var maps = instances[0].map;
        var pointArray = new google.maps.MVCArray(data);
        heatLayer.setData(pointArray)
      });


      // }, 1000);
    }
  }

})();

