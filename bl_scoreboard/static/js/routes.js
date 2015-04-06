/**
 * Created by ogaidukov on 25.06.14.
 */

define(['./app'], function (app) {
     'use strict';

     return app.config(['$routeProvider', function ($routeProvider) {

         $routeProvider.when('/gamer/:promoCode', {
           templateUrl: 'js/components/pages/gamer-details.html',
           controller: 'GamerDetailsCtrl'
         });

         $routeProvider.when('/gamer', {
           templateUrl: 'js/components/pages/gamer-details.html',
           controller: 'GamerDetailsCtrl'
         });

         $routeProvider.when('/give_prize', {
           templateUrl: 'js/components/pages/give-prize.html',
           controller: 'GivePrizeCtrl'
         });

         $routeProvider.when('/total', {
           templateUrl: 'js/components/pages/total.html',
           controller: 'TotalCtrl'
         });

         $routeProvider.when('/', {
           templateUrl: 'js/components/pages/scoreboard.html',
           controller: 'ScoreboardCtrl'
         });

     }]);
});