
app.controller("HeaderCtrl", ["$scope", "$location", "$routeParams", "$resource", "$timeout", "$window", function ($scope, $location, $routeParams, $resource, $tiemout, $window) {

  $scope.view = {
    logo: '/img/usersico.gif',
    usuario: null
  };

  $scope.salir = function() {
    $window.location.href = '/logout';
  }

  $scope.$on('config', function(c) {
    $scope.view.usuario = $scope.$parent.config.usuario;
  });

}]);
