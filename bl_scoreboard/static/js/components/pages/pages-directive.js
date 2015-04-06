/**
 * Created by ogaidukov on 25.06.14.
 */

define(['./pages', 'require'], function(pages, require) {
  'use strict';

  pages.directive('navBar', function() {
    return {
      restrict: "E",
      templateUrl: require.toUrl('./main-navigation-bar.html'),
      controller: 'NavBarCtrl'
    }
  });
});