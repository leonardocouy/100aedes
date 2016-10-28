(function () {
    'use strict';

    angular
        .module('app')
        .config(config);

    function config($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'base.html',
                controller: 'HomeController',
                controllerAs: 'vm'
            });
    }

})();
