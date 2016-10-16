(function () {
    'use strict';
    angular
        .module('app')
        .config(config);

    function config($interpolateProvider) {
       $interpolateProvider.startSymbol('{_');
       $interpolateProvider.endSymbol('_}');
    }
})();
