#!/bin/bash
# This script will render the project css files.

# put the path of library scss files we want to incluide
libraries="\
	--load-path node_modules/govuk_frontend_toolkit/stylesheets \
	--load-path node_modules/govuk-elements-sass/public/sass \
"

# put the path of source code files we want to include, and where we want them
# to be exported to e.g., input.scss:output.css
input_output_map="\
"

prod_command="sass --sourcemap=none --style compressed"

eval 'rm enrolment/static/*.css'
eval $prod_command$libraries$input_output_map
