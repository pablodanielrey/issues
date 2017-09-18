app = angular.module('MainApp', ['ui.router', 'ngResource', 'ngMaterial'])


app.config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default')
    .primaryPalette('blue')
    .warnPalette('red')
    .accentPalette('cyan');
});


app.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {

  $urlRouterProvider.otherwise("/preload");

  // --- preload ----

  $stateProvider
  .state('preload', {
    url:'/preload',
    templateUrl: 'componentes/preload/index.html',
    controller:'PreloadCtrl'
  })
  .state('preload.bienvenido', {
    url:'/bienvenido',
    templateUrl: 'componentes/preload/templates/bienvenido.html',
  })
  .state('preload.error', {
    url:'/error',
    templateUrl: 'componentes/preload/templates/error.html',
  })



}]);


app.config(['$resourceProvider', function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);
