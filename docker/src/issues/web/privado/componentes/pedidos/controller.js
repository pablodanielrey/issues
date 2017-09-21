
app.controller("PedidosCtrl", ["$scope", "$resource", "$location", '$state', '$http', function ($scope, $resource, $location, $state, $http) {

  //var Usuarios = $resource('http://127.0.0.1:5001/users/api/v1.0/usuarios/');

  $state.go('pedidos.seleccion');

  $scope.pedido = { };

  $scope.$parent.obtener_config().then(function(c) {
    $scope.config = c.data;
    console.log(c.data);

    var usuario = c.data['usuario']
    $scope.pedido = {
        usuario_id: usuario['sub'],
        nombre: usuario['given_name'],
        correo: usuario['email'],
        telefono: usuario['phone_number']
    }
  })

  $scope.registrarProblema = function() {
    var api = $scope.config.issues_api_url;
    $scope.pedido.estado_cliente = $state.$current.name;
    console.log($scope.pedido);
    $http({
            url: api + '/pedidos',
            dataType: 'json',
            method: 'POST',
            data: $scope.pedido,
            headers: {
                "Content-Type": "application/json"
            }
    }).then(
    function(response){
        console.log(response);
        $scope.pedido.numero = response.data.pedido;
        $state.go('pedidos.ok');
    },
    function(error){
        console.log(error);
        $state.go('pedidos.error');
    });
  }

}]);
