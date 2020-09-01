const gulp = require('gulp');

gulp.task('css', function () {
  var sass = require('gulp-sass');
  var sourcemaps = require('gulp-sourcemaps');

  sass.compiler = require('sass');

  return gulp.src([
    'static/src/investment-report2.scss',
    'static/src/investment-report-last-page2.scss'
  ])
    .pipe( sourcemaps.init() )
    .pipe( sass().on('error', sass.logError) )
    .pipe( sourcemaps.write('.') )
    .pipe( gulp.dest('investment_report/static/build/') );
});


gulp.task('watch', function() {
    gulp.watch('static/src/**/*.css', ['css']);
});
