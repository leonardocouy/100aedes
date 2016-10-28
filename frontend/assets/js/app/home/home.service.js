(function () {
    'use strict';

    angular
        .module('app')
        .factory('dataService', dataService);

    dataService.$inject = ['$http', 'ENV_VARS'];

    function dataService($http, ENV_VARS) {
        var service = {
            getReports: getReports,
            calculatePercentage: calculatePercentage
        };

        return service;

        ////////////////

        function getReports() {
            return $http.get(ENV_VARS.apiUrl)
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

