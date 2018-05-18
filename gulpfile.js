const gulp = require('gulp');

gulp.task('css', function () {
  var postcss    = require('gulp-postcss');
  var sourcemaps = require('gulp-sourcemaps');

  return gulp.src([
    'static/src/investment-report.css',
    'static/src/investment-report-last-page.css'
  ])
    .pipe( sourcemaps.init() )
    .pipe( postcss() )
    .pipe( sourcemaps.write('.') )
    .pipe( gulp.dest('investment_report/static/build/') );
});


gulp.task('watch', function() {
    gulp.watch('static/src/**/*.css', ['css']);
});
