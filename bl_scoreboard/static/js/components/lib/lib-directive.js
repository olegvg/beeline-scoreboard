/**
 * Created by ogaidukov on 30.06.14.
 */

define(['./lib'], function(lib) {
  'use strict';

  lib.directive('modalDialogToScopeAs', ['$q', '$window', function($q, $window) {
    return {
      restrict: 'A',
      link: function(scope, element, attr) {
        scope[attr.modalDialogToScopeAs] = {};
        scope[attr.modalDialogToScopeAs].show = function() {
          var shownDeferred = $q.defer();
          try {
            element.modal('show');
          }
          catch(msg) {
            $window.alert("Twitter Bootstrap or at least Modal Dialog add-on is not installed!");
          }
          element.on('shown.bs.modal', function() { shownDeferred.resolve() });
          return shownDeferred.promise
        };
        scope[attr.modalDialogToScopeAs].hide = function() {
          var hiddenDeferred = $q.defer();
          try {
            element.modal('hide');
          }
          catch(msg) {
            $window.alert("Twitter Bootstrap or at least Modal Dialog add-on is not installed!");
          }
          element.on('hidden.bs.modal', function() { hiddenDeferred.resolve() });
          return hiddenDeferred.promise
        }
      }
    }
  }]);

  lib.directive('maskedInput', ['$window', function($window) {
    return {
      restrict: 'A',
      link: function(scope, element, attr) {
        try {
          element.mask(attr.maskedInput);
        }
        catch(err) {
          $window.alert("jQuery Masked Input plugin is not installed!");
        }
      }
    }
  }]);
});