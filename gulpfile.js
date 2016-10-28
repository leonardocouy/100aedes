var ENV = process.env.APP_ENV || 'development';

if (ENV === 'development') {
  require('dotenv').load();
}

var gulp = require('gulp');
var sass = require('gulp-sass');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var ngAnnotate = require('gulp-ng-annotate');
var ngConfig = require('gulp-ng-config');
var rename = require ('gulp-rename');
var fs = require('fs');
var config = require('./frontend/config.js');
var uglifyInline = require('gulp-uglify-inline');
var sourcemaps = require('gulp-sourcemaps');
var order = require("gulp-order");
var vendorPath = "assets/js/vendor/";


var concatOrderSources = [
  vendorPath + 'angular/*.js',
  vendorPath + 'angular-route/*.js',
  vendorPath + 'jquery/*.js',
  vendorPath + 'bootstrap/*.js',
  vendorPath + 'highcharts-ng/*.js',
  vendorPath + 'lodash/*.js',
  vendorPath + 'angular-simple-logger/*.js',
  vendorPath + 'angular-google-maps/*.js',
  'assets/js/app/app.module.js',
  'assets/js/app/app.constants.js',
  'assets/js/app/app.config.js',
  'assets/js/app/app.run.js',
  'assets/js/app/home/*.js'
];

gulp.task('default', ['sass', 'ng-config', 'scripts']);

gulp.task('sass', function() {
  return gulp.src('frontend/assets/src/sass/**/*.scss')
      .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
      .pipe(gulp.dest('frontend/assets/css'))
});


// ['assets/js/vendor/lodash/*.js', 'assets/js/vendor/jquery/*.js', 'assets/js/vendor/!(lodash, jquery)**/*.js', 'assets/js/app/*.js'
gulp.task('scripts', function() {
  return gulp.src(['frontend/assets/js/app/app.module.js', 'frontend/assets/js/app/!(app.module)*.js','frontend/assets/js/app/home/*.js'])
      .pipe(sourcemaps.init())
        .pipe(concat('app.min.js'))
        .pipe(ngAnnotate({add: true}))
        .pipe(uglify())
      .pipe(sourcemaps.write())
      .pipe(gulp.dest('frontend/assets/dist/'));
});


gulp.task('ng-config', function(){
  fs.writeFileSync('./frontend/config.json', JSON.stringify(config[ENV]));
  return gulp.src('./frontend/config.json')
      .pipe(ngConfig('app', {
        createModule: false,
        pretty: true,
        wrap: true
      }))
      .pipe(rename('app.constants.js'))
      .pipe(gulp.dest('frontend/assets/js/app/'))
});
