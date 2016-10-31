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
var order = require("gulp-order");
var sourcemaps = require('gulp-sourcemaps');
var vendor = require('gulp-concat-vendor');
var mainBowerFiles = require('main-bower-files');
var print = require('gulp-print');
var addsrc = require('gulp-add-src');


gulp.task('default', ['sass', 'config-env', 'dist']);

gulp.task('sass', function() {
  return gulp.src('frontend/assets/src/sass/**/*.scss')
      .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
      .pipe(gulp.dest('frontend/assets/dist/'))
});

gulp.task('config-env', function(){
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

gulp.task('dist', function() {
    return gulp.src(mainBowerFiles({
      paths: {
        bowerDirectory: 'frontend/assets/js/bower_components',
        bowerJson: 'frontend/assets/js/bower.json'
      }
    }))
    .pipe(addsrc.append(['frontend/assets/js/app/app.module.js', 'frontend/assets/js/app/!(app.module)*.js','frontend/assets/js/app/home/*.js']))
    .pipe(print())
    .pipe(concat('bundle.min.js'))
    .pipe(ngAnnotate())
    .pipe(uglify())
    .pipe(gulp.dest('frontend/assets/dist/'));
});


