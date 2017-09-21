
app.controller("PedidosCtrl", ["$scope", "$resource", "$location", '$state', function ($scope, $resource, $location, $state) {

  //var Usuarios = $resource('http://127.0.0.1:5001/users/api/v1.0/usuarios/');

  $state.go('pedidos.seleccion');


}]);
