
//Controlador Indice
app.controller("IndexCtrl", ["$scope", "$http", function ($scope, $http) {

  $scope.config = {};

  $scope.obtener_config = function() {
    return $http.get('/config.json');
  };

  $scope.obtener_config().then(function(c) {
    $scope.config = c.data;
    $scope.$broadcast('config', null);
  });

}]);
