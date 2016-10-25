(function () {
    'use strict';
    angular
        .module('app')
        .run(runApp);

    runApp.$inject = ['$http'];

    function runApp($http) {
        $http.defaults.headers.common['Authorization'] = 'JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRva2VuIiwiZXhwIjoxNDc3NDMzNTI4LCJlbWFpbCI6ImNvbnRhdG9AMTAwYWVkZXMuY29tLmJyIiwidXNlcl9pZCI6NH0.L6VlbFORhdAFK5vBYXMVe52TIeWmd4pwHm7y4UFIHZg';
    }

})();

