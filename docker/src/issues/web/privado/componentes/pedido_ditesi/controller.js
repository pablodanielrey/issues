
app.controller("PedidoDitesiCtrl", ["$scope", "$http", "$state", function ($scope, $http, $state) {

  //var Usuarios = $resource('http://127.0.0.1:5001/users/api/v1.0/usuarios/');

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

    $state.go('pedidoDitesi.pedido');
  })

  $scope.registrarProblema = function() {
    var api = $scope.config.issues_api_url;

    console.log($scope.pedido);
    // var data = {
    //   dni: '12345678',
    //   nombre: 'algo',
    //   apellido: 'algo2',
    //   correo: 'e@econo',
    //   telefono: '221-15-8358',
    //   problema: 'algo muy largo que describe el problema'
    // };

    $http({
            url: api + '/pedidos_ditesi',
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
        $state.go('pedidoDitesi.pedidoOk');
    },
    function(error){
        console.log(error);
        $state.go('pedidoDitesi.error');
    });


  }



}]);
