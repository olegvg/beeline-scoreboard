module.exports = function(grunt) {
  grunt.initConfig({

    // !! This is the name of the task 'requirejs' (grunt-contrib-requirejs module)
    requirejs: {
      dist: {
        // !! You can drop your app.build.js config wholesale into 'options'
        options: {
          appDir: "bl_scoreboard/static",
          baseUrl: "js",
          dir: "bl_scoreboard/dist",
          keepBuildDir: true, // cleanup of 'dist' is supposed to be done by 'purge:dist' task
          mainConfigFile: "bl_scoreboard/static/js/main.js",
          name: "main", // points to 'static/js/main.js'
          optimize: 'uglify2',
          uglify2: {
            compress: {}
          },
          skipDirOptimize: true,
          preserveLicenseComments: false,
          findNestedDependencies: false,
          removeCombined: true,
          inlineText: true,
          optimizeCss: 'standard',
          logLevel: 0,
          fileExclusionRegExp: /^\./
        }
      }
    },

    compress: {
      dist: {
        options: {
          mode: 'gzip',
          level: 9
        },
        files: [
          {expand: true, src: [
            'bl_scoreboard/dist/js/**/*.js',
            'bl_scoreboard/dist/lib/requirejs/require.js'
          ], ext: '.js.gz'}
        ]
      }
    },

    uglify: {
      rjs_dist: {
        options: { },
        files: {
          'bl_scoreboard/dist/lib/requirejs/require.js': ['bl_scoreboard/dist/lib/requirejs/require.js']
        }
      }
    },

    // !! This is the name of the task 'clean' (grunt-contrib-clean module) after renaming to 'purge'
    purge: {
      dist: {
        src: [
          'bl_scoreboard/dist/*', '!bl_scoreboard/dist/.gitignore'
        ]
      },
      dev: {
        src: [
          'bl_scoreboard/static/lib/*', '!bl_scoreboard/static/lib/.gitignore',
        ]
      }
    },

    // !! Bower's 'install' task
    bower: {
      dev: {
        options: {
//          targetDir: "bl_scoreboard/static/lib",
//          layout: "byComponent",
          verbose: true
        }
      }
    },

    bower_rjs: {
      all: {
        rjsConfig: "bl_scoreboard/static/js/main.js"
      }
    }
  });

  // This loads the requirejs plugin into grunt
  grunt.loadNpmTasks('grunt-contrib-requirejs');

  grunt.loadNpmTasks('grunt-contrib-compress');
  grunt.loadNpmTasks('grunt-contrib-uglify');

  // Must be renamed because 'clean' is very common name
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.renameTask('clean', 'purge'); // because 'clean' is very common name

  // Must be renamed because of task name conflict between 'grunt-bower-requirejs' and 'grunt-bower-task'.
  // They both are use 'bower' task name.
  // Also, 'bower-requirejs' npm module can be used. See '.bowerrc.inactive' at the root directory for some details.
  grunt.loadNpmTasks('grunt-bower-requirejs');
  grunt.renameTask('bower', 'bower_rjs');

  grunt.loadNpmTasks('grunt-bower-task');

  // Register tasks
  grunt.registerTask('clean', ['purge:dist', 'purge:dev']);
  grunt.registerTask('clean-dist', ['purge:dist']);
  grunt.registerTask('clean-dev', ['purge:dev']);
  grunt.registerTask('build-dev', ['clean-dev', 'bower:dev', 'bower_rjs']);
  grunt.registerTask('build-dist', ['clean-dist', 'requirejs:dist', 'uglify:rjs_dist', 'compress:dist']);
};
