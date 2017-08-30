app = angular.module('MainApp', ['ngRoute', 'ngResource','ngFileUpload', 'ngImgCrop'])

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider
    .when('/config_correo/:uid', {templateUrl: '/componentes/config_correo/index.html', controller:'ConfigCorreoCtrl'})
    .when('/config_clave/:uid', {templateUrl: '/componentes/cambio_clave/index.html', controller:'ConfigClaveCtrl'})
    .when('/reset_clave', {templateUrl: '/componentes/reseteo_clave/index.html', controller:'ReseteoClaveCtrl'})
    .when('/perfil/:uid', {templateUrl: '/componentes/perfil/index.html', controller:'PerfilCtrl'})
    .when('/preload', {templateUrl: '/componentes/preload/index.html', controller:'PreloadCtrl'})
    .otherwise({ redirectTo: '/preload' });

}]);

app.config(['$resourceProvider', function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);
