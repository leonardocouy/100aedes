(function () {
    'use strict';
    angular
        .module('app')
        .run(runApp);

    runApp.$inject = ['$http', 'ENV_VARS'];

    function runApp($http, ENV_VARS) {
        $http.defaults.headers.common['Authorization'] = 'JWT ' + ENV_VARS.apiToken;
    }

})();

