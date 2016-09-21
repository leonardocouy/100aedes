var app = angular.module("aedesApp", ['ngRoute']);

app.config(function($routeProvider, $interpolateProvider){
   $routeProvider.when('/', {
      controller: "TestController",
      templateUrl: 'index.html'
   });

   $interpolateProvider.startSymbol('{_');
   $interpolateProvider.endSymbol('_}');
    // $resourceProvider.defaults.stripTrailingSlashes = false;
});

app.controller("TestController", function($scope){
   console.log("test console");
});