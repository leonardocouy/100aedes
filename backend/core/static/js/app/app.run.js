(function () {
    'use strict';
    angular
        .module('app')
        .run(runApp);

    runApp.$inject = ['$http', 'JWT_TOKEN'];

    function runApp($http, JWT_TOKEN) {
        $http.defaults.headers.common['Authorization'] = 'JWT ' + JWT_TOKEN;
    }

})();

