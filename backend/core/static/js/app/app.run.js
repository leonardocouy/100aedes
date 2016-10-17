(function () {
    'use strict';
    angular
        .module('app')
        .run(runApp);

    runApp.$inject = ['$http'];

    function runApp($http) {
        $http.defaults.headers.common.Authorization = 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNDUsImV4cCI6MTQ3NjY2ODUwOCwidXNlcm5hbWUiOiJ0b2tlbiIsImVtYWlsIjoiIn0.UhpOkxzMZFa6weXgzVcw1rg1Eu5-weiKogu1sfrP8UE';
    }

})();

