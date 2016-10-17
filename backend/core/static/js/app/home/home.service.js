(function () {
    'use strict';

    angular
        .module('app')
        .factory('dataService', dataService);

    dataService.$inject = ['$http'];

    function dataService($http) {
        var API_URL = 'http://staging.100aedes.com.br/api/v1/reports/';

        var service = {
            getReports: getReports,
            calculatePercentage: calculatePercentage
        };

        return service;

        ////////////////

        function getReports() {
            return $http.get(API_URL)
                .then(getReportsComplete)
                .catch(getReportsFailed);


            function getReportsComplete(response) {
                return response.data;
            }

            function getReportsFailed(error) {
                console.log(error)
            }
        }

        function calculatePercentage(data, total){
            var new_data = [];
            angular.forEach(data, function(value){
                var result = ((value/total) * 100);
                new_data.push(result)
            });
            return new_data;
        }


    }

})();

