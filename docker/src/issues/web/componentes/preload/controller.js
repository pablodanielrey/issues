
app.controller("PreloadCtrl", ["$scope", "$http", '$location', function ($scope, $http, $location) {

  $scope.$parent.estado = 'EstadoPreload';

  $scope._inicializar = function() {
    if ($scope.$parent.config != null && $scope.$parent.config.usuario != null) {
      $location.path('/perfil/' + $scope.$parent.config.usuario['sub']);
    }
  }

  $scope.$on('config', $scope._inicializar);

  $scope._inicializar();

}]);
