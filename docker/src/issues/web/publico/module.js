app = angular.module('MainApp', ['ui.router', 'ngResource', 'ngMaterial'])


app.config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default')
    .primaryPalette('blue')
    .warnPalette('red')
    .accentPalette('cyan');
});


app.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {

  $urlRouterProvider.otherwise("/pedido_ditesi");

  // --- preload ----

  $stateProvider
  .state('pedidoDitesi', {
    url:'/pedido_ditesi',
    templateUrl: 'componentes/pedido_ditesi/index.html',
    controller:'PedidoDitesiCtrl'
  })
  .state('pedidoDitesi.pedido', {
    url:'/pedido',
    templateUrl: 'componentes/pedido_ditesi/templates/pedido.html',
  })
  .state('pedidoDitesi.pedidoOk', {
    url:'/pedido_ok',
    templateUrl: 'componentes/pedido_ditesi/templates/pedido_registrado.html',
  })
  .state('pedidoDitesi.error', {
    url:'/error',
    templateUrl: 'componentes/pedido_ditesi/templates/error.html',
  })



}]);


app.config(['$resourceProvider', function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);
