(function () {
    'use strict';
    angular
        .module('app')
        .run(runApp);

    runApp.$inject = ['$http'];

    function runApp($http) {
        $http.defaults.headers.common.Authorization = 'JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Imxlb0BsZW8uY29tIiwidXNlcm5hbWUiOiJsZW8iLCJ1c2VyX2lkIjoxLCJleHAiOjE0NzUyMzE5OTh9.Wpp_-ebxI2_aC2mmqSOwmpddo68NZ5T-RlgbCP9OAPY';
    }

})();

