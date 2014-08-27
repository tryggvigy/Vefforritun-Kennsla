/*jshint ignore: start*/

var paths = {
  base: 'kennsla_vefforritun',
  any: './**/*',
  verkefni1: 'verkefni1/',
  verkefni2: 'verkefni2/'
};

/*
  returns the path from project root to the file changed.
*/
function buildShortPath(pathComponents) {
  var shortPath = '';
  for (var i = pathComponents.length-1; i >= 0; i--) {
    if(pathComponents[i] === paths.base)
      return shortPath;

    if(shortPath === '')
      shortPath = pathComponents[i];
    else
      shortPath = pathComponents[i] + '/' + shortPath;
  }
}

// FIRES ON FILE CHANGE.
var changeEvent = function(evt) {
  var pathComponents = evt.path.split('/');
  var shortPath = buildShortPath(pathComponents);
  gutil.log('\n\nFile', gutil.colors.cyan(shortPath), 'was', gutil.colors.magenta(evt.type) + ', running tasks...\n');
};

var gulp = require('gulp');
var gutil = require('gulp-util');
var w3cHTML = require('gulp-w3cjs');
var w3cCSS = require('gulp-css-validator');

//#########################################
//################ TASKS ##################
//#########################################

//################## HTML ##############################
gulp.task('validate-html-v1', function () {
    gulp.src([paths.verkefni1 + '**/*.html', paths.verkefni1 + '**/*.htm'])
        .pipe(w3cHTML());
});

gulp.task('validate-html-v2', function () {
    gulp.src([paths.verkefni2 + '**/*.html', paths.verkefni2 + '**/*.htm'])
        .pipe(w3cHTML());
});

//################## CSS ################################
gulp.task('validate-css-v1', function () {
    gulp.src([paths.verkefni1 + '**/*.css'])
        .pipe(w3cCSS());
});

//---------------------------------------------------------------------------

// Watch
gulp.task('watch', function() {

  //VALIDATE SAVED HTML FILE
  gulp.watch([paths.any+'.html', paths.any+'.htm'], function(evt) {
    changeEvent(evt);
    gulp.src(evt.path)
        .pipe(w3cHTML());
  });

  //VALIDATE SAVED CSS FILE
  gulp.watch([paths.any+'.css'], function(evt) {
    changeEvent(evt);
    gulp.src(evt.path)
        .pipe(w3cCSS());
  });
});

// Default
gulp.task('default', ['watch']);
