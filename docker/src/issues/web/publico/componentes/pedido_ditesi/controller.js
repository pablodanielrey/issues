
app.controller("PedidoDitesiCtrl", ["$scope", "$http", "$state", function ($scope, $http, $state) {

  //var Usuarios = $resource('http://127.0.0.1:5001/users/api/v1.0/usuarios/');

  $scope.$parent.obtener_config().then(function(c) {
    $scope.config = c.data;
    $state.go('pedidoDitesi.pedido');
  })

  $scope.registrarProblema = function() {
    var api = $scope.config.issues_api_url;

    var data = {
      nombre: 'algo',
      apellido: 'algo2',
      correo: 'e@econo',
      telefono: '221-15-8358',
      problema: 'algo muy largo que describe el problema'
    };

    $http({
            url: api + '/publico/pedidos_ditesi',
            dataType: 'json',
            method: 'POST',
            data: data,
            headers: {
                "Content-Type": "application/json"
            }
    }).then(
    function(response){
        console.log(response);
        $state.go('pedidoDitesi.pedidoOk');
    },
    function(error){
        console.log(error);
        $state.go('pedidoDitesi.error');
    });


  }



}]);
