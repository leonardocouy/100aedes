(function () {
    'use strict';
    angular
        .module('app')
        .run(runApp);

    runApp.$inject = ['$http'];

    function runApp($http) {
        $http.defaults.headers.common['Authorization'] = 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRva2VuIiwiZW1haWwiOiIiLCJleHAiOjE0NzY2Njk4ODIsInVzZXJfaWQiOjE0NX0.c0TrLDKPm0qCHqG39_hQtDIwOjdlDz4ggC5Q-llfuMs  ';
    }

})();

