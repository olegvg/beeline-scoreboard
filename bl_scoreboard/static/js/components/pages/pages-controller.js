/**
 * Created by ogaidukov on 25.06.14.
 */

define(['./pages'], function(pages) {
  'use strict';

  pages.controller('NavBarCtrl', [
    '$scope',
    '$location',
    function($scope, $location) {
      $scope.showScoreboard = function() {
        $location.url('/')
      };

      $scope.showGivePrize = function() {
        $location.url('/give_prize')
      };

      $scope.newGamerClick = function() {
        $location.url('/gamer')
      };

      $scope.searchClick = function() {
        var promoCode = $scope.searchPromo;
        if(promoCode) {
          $location.url('/gamer/' + promoCode);
        }
      }
    }
  ]);

  pages.controller('GamerDetailsCtrl', [
    '$scope',
    '$routeParams',
    '$location',
    '$http',
    'GameSelectionStore',
    'GameLogic',
    function($scope, $routeParams, $location, $http, GameSelectionStore, GameLogic) {

      $scope.gamer = {
        participate: 0,
        score: 0,
        photos: 0,
        best_time: '',
        most_pins: 0
      };

      if($routeParams.promoCode) {
        $scope.detailsMode = 'edit';
        $scope.personalAgreement = true;

        var params = {promo_code: $routeParams.promoCode};
        params.game_name = GameSelectionStore.getGameSelector();

        $http.get('../gamers/mangle_gamer', { params: params }).success(function(res) {
          $scope.gamer = res;
          $scope.gamer.game_name = params.game_name;
          updateGamesForm();
          if(res.prize_given) {
            $scope.alertPrizeGivenModal.show()
          }
        }).error(function() {
          $scope.detailsMode = 'new'
        })
      } else {
        $scope.detailsMode = 'new';
      }

      var games = {
        '': {
          showParticip: false,
          showWins: false,
          showPhotos: false,
          showTimes: false,
          showPins: false,
          participate: 0,
          score: 0,
          photos: 0
        }};
      GameLogic.getGameLogic().then(function(res) {
        for(var key in res) {
          if(res.hasOwnProperty(key)) {
            games[key] = res[key]
          }
        }
        $scope.gameNames = Object.keys(games);
      });

      $scope.gameSelectClick = function() {
        GameSelectionStore.setGameSelector($scope.gamer.game_name);
        $http.get('../gamers/mangle_gamer', {
          params: { promo_code: $routeParams.promoCode, game_name: $scope.gamer.game_name }
        }).success(function(res) {
          delete res['game_name'];
          for(var key in res) {
            if(res.hasOwnProperty(key)) {
              $scope.gamer[key] = res[key]
            }
          }
          updateGamesForm()
        });
      };

      var updateGamesForm = function() {
        var gameDescr = games[$scope.gamer.game_name];
        for(var key in gameDescr) {
          if (gameDescr.hasOwnProperty(key)) {
            if (key.indexOf('show') == 0) {     // touch fields which begin with 'show' e.g. 'showParticip'
              $scope[key] = gameDescr[key]
            }
          }
        }
      };

      $scope.participateClick = function() {
        if($scope.gamer.participate > 1) {
          $scope.gamer.participate = 0
        } else if($scope.gamer.participate == 0) {
          $scope.gamer.participate = games[$scope.gamer.game_name].participate;
        }
      };

      $scope.winClick = function() {
        if($scope.gamer.score > 0) {
          $scope.gamer.score = 0
        } else if($scope.gamer.score == 0) {
          $scope.gamer.score = games[$scope.gamer.game_name].score;
        }
      };

      $scope.photoClick = function() {
        if($scope.gamer.photos > 0) {
          $scope.gamer.photos = 0
        } else if($scope.gamer.photos == 0) {
          $scope.gamer.photos = games[$scope.gamer.game_name].photos;
        }
      };

      $scope.submitClick = function() {
        if($scope.detailsMode === 'edit') {
//          $scope.gamer.game_name = $scope.gamer.game_name.text;
          $http.put('../gamers/mangle_gamer', $scope.gamer).then(function(){
            $location.url('/')
          })
        } else if($scope.detailsMode === 'new') {
          $http.post('../gamers/mangle_gamer', $scope.gamer)
            .success(function(res) {
              $scope.promoCode = res.promo_code;
              $scope.gamersPromoCodeModal.show()
            })
            .error(function(d, status) { if(status == 409) { $scope.gamerAlreadyRegisteredModal.show() }})
        }
      };

      $scope.leaveGamersPromoCodeModalClick = function() {
        $scope.gamersPromoCodeModal.hide().then(function() { $location.url('/') })
      };

      $scope.leaveGamerDetailsClick = function() {
        $scope.gamerAlreadyRegisteredModal.hide().then(function() { $location.url('/') })
      }
    }
  ]);

  pages.controller('ScoreboardCtrl', [
    '$scope',
    '$route',
    '$http',
    function($scope, $route, $http) {
      $http.get('../gamers/get_scoreboard').success(function(res){
        $scope.scoreBoardMain = res['main'];
        $scope.scoreBoardDance = res['dance'];
        $scope.scoreBoardAutosim = res['autosim']
      });

      $scope.currentScoreboard = 'main';
      $scope.changeScoreboard = function (val) {
        $scope.currentScoreboard = val
      }
    }]);

  pages.controller('GivePrizeCtrl', [
    '$scope',
    '$route',
    '$location',
    '$http',
    function($scope, $route, $location, $http) {
      $scope.searchClick = function() {
        $http.get('../gamers/get_gamer_summary', {
          params: { promo_code: $scope.searchPromo }
        }).success(function(res) {
          $scope.gamer = res;
          $scope.promoFound = true;
          $scope.promoNotFound = false;
          if(res.prize_given) {
            $scope.alertPrizeGivenModal.show()
          }
        }).error(function() {
          $scope.promoFound = false;
          $scope.promoNotFound = true;
        })
      };

      $scope.prizeGivenClick = function() {
        $scope.prizeGivenModal.show();
      };
      $scope.prizeGivenAcceptClick = function() {

        $scope.prizeGivenModal.hide().then(function() {
          var params = {
            promo_code: $scope.gamer.promo_code,
            prize_given: true
          };
          $http.put('../gamers/mangle_gamer', params).then(function(){
            $location.url('/')
          })
        })
      };

    }]);

  pages.controller('TotalCtrl', [
    '$scope',
    '$interval',
    '$http',
    function($scope, $interval, $http) {
      var secsToRestart = 60;

      var updateFunc = function() {
        $http.get('../gamers/total').success(function(res) { $scope.totalGamers = res.total })
      };

      $scope.secsToRestart = secsToRestart;
      updateFunc();
      $interval(function() {
        $scope.secsToRestart = secsToRestart;
        updateFunc()
      }, secsToRestart * 1000);
      $interval(function() {
        $scope.secsToRestart -= 1;
      }, 1000)

    }]);


});