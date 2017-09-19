
app.controller("PedidoDitesiCtrl", ["$scope", "$http", "$state", function ($scope, $http, $state) {

  //var Usuarios = $resource('http://127.0.0.1:5001/users/api/v1.0/usuarios/');

  $scope.pedido = {
      dni: '',
      nombre: '',
      apellido: '',
      correo: ''
  };

  $scope.obtenerInfoUsuario = function(uid) {
    var api = $scope.config.users_api_url;

    $http.get(api + '/usuarios/' + uid).then(
    function(data){
        var usuario = data.data;
        console.log(usuario);
        $scope.pedido = {
            'dni': usuario.dni,
            'nombre': usuario.nombre,
            'apellido': usuario.apellido
        }
        $state.go('pedidoDitesi.pedido');
    },
    function(error){
        console.log(error);
        $state.go('pedidoDitesi.error');
    });

  }

  $scope.$parent.obtener_config().then(function(c) {
    $scope.config = c.data;
    console.log(c.data);

    var uuid = c.data['usuario']['sub'];
    $scope.obtenerInfoUsuario(uuid);

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
            url: api + '/publico/pedidos_ditesi',
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
