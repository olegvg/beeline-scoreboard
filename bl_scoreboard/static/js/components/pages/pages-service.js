/**
 * Created by ogaidukov on 02.07.14.
 */

define(['./pages'], function(pages) {
  'use strict';

  pages.factory('GameSelectionStore', function() {
    var gameSelector = '';
    return {
      setGameSelector: function(val) { gameSelector = val },
      getGameSelector: function() { return gameSelector }
    }
  });

  pages.service('GameLogic', ['$http', '$q', function($http, $q) {
    var gameLogicDeferred = $q.defer();
    $http.get('./game_logic.json').success(function(res) { gameLogicDeferred.resolve(res) });
    this.getGameLogic = function() { return gameLogicDeferred.promise };
  }])
});