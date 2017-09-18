
app.controller("PreloadCtrl", ["$scope", "$http", '$timeout', '$state', function ($scope, $http, $timeout, $state) {

  $scope.view = {
    usuario: $scope.$parent.config.usuario,
    progreso: 0
  };

  $scope.chequear_precondiciones = function() {
    $scope.view.progreso = 0;
    var api = $scope.config.users_api_url;

    // chequeo la clave
    $scope.view.progreso = 30;
    $http.get(api + '/usuarios/' + $scope.config.usuario.sub + '/precondiciones')
    .then(function(d) {
        $scope.view.progreso = 60;
        if (d.data.clave.debe_cambiarla) {
          $state.go('cambio_clave_temporal');
          return;
        }

        $scope.view.progreso = 80;
        if (!d.data.correos.tiene_alternativo) {
          $state.go('config_correo_alternativo');
          return;
        }

        // voy al perfil
        $scope.view.progreso = 100;
        var uid = $scope.config.usuario['sub'];
        $state.go('perfil', {uid: uid});

      }
    ).catch(function(err) {
      console.log(err);
    });

  }

  $scope._inicializar = function() {
    $state.go('preload.bienvenido');

    $scope.$parent.obtener_config().then(
      function(c) {
        $scope.config = c.data;
        $scope.chequear_precondiciones();
      },
      function(err) {
        console.log(err);
      }
    );
  }

  $scope.$on('config', $scope._inicializar);

  $scope._inicializar();

}]);
