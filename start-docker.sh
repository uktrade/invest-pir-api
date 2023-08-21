cf_cli_not_found(){
echo "#######################################################\n\n \
Cloud Foundry CLI could not be found. Please install to continue. \n\n\
#######################################################\n\n"
exit 1 
}

cloud_foundry_signin () {
echo "#######################################################\n\n \
Lets get you signed into Cloud Foundry. \n\n\
#######################################################\n\n"

make cf-signin ${user_email}

echo "#######################################################\n\n \
Installing cf conduit... \n\n\
#######################################################\n\n"
make install-cf-conduit
}


cloud_foundry_signin_sso () {
echo "#######################################################\n\n \
Lets get you signed into Cloud Foundry. \n\n\
#######################################################\n\n"

make cf-signin-sso ${user_email}

echo "#######################################################\n\n \
Installing cf conduit... \n\n\
#######################################################\n\n"
make install-cf-conduit
}

echo "#######################################################\n\n \
Lets get started \n\n\
#######################################################\n\n"

echo "Enter Your Email: "
read user_email

echo "\n#######################################################\n\n \
Welcome ${user_email}! \n\n\
#######################################################\n\n"

echo "#######################################################\n\n \
Checking for Cloud Foundry CLI... \n\n\
#######################################################\n\n"
cf logout || cf_cli_not_found
cloud_foundry_signin_sso


clone_invest_pir_api (){
echo "#######################################################\n\n \
Attempting directory-api database clone. This can take a few minutes...\n\n\
#######################################################\n\n"
cf conduit -o dit-staging -s directory-dev invest-pir-api-dev-db -- pg_dump -cOx | docker exec --interactive postgres psql -U debug invest_pir_api_debug
}

pg_dump_not_found (){
echo "#######################################################\n\n \
pg_dump could not be found. Please check PATH variables. \n\n\
#######################################################\n\n"
exit 1
}


read -e -p "Would you like to add hosts to /etc/hosts? [Y/n] " YN

if [[ $YN != "n" && $YN != "N" && $YN != "" ]]; then
    echo "Adding to /etc/hosts...\n"
    echo "127.0.0.1       greatcms.trade.great" >> /etc/hosts
    echo "127.0.0.1       buyer.trade.great" >> /etc/hosts
    echo "127.0.0.1       supplier.trade.great" >> /etc/hosts
    echo "127.0.0.1       sso.trade.great" >> /etc/hosts
    echo "127.0.0.1       sso.proxy.trade.great" >> /etc/hosts
    echo "127.0.0.1       api.trade.great" >> /etc/hosts
    echo "127.0.0.1       profile.trade.great" >> /etc/hosts
    echo "127.0.0.1       exred.trade.great" >> /etc/hosts
    echo "127.0.0.1       forms.trade.great" >> /etc/hosts
    echo "127.0.0.1       international.trade.great" >> /etc/hosts
    echo "127.0.0.1       cms.trade.great" >> /etc/hosts
    echo "127.0.0.1       components.trade.great" >> /etc/hosts
fi


echo "#######################################################\n\n \
Creating secrets... \n\n\
#######################################################\n\n"

if [ ! -f ./.env ]; \
    then echo "#!/usr/bin/env bash\nexport EMAIL='${user_email}'" > .env \
        && echo "Created .env"; \
    else echo ".env already exists."; \
fi
if [ ! -f ./docker/.env ]; \
    then sed -e 's/#DO NOT ADD SECRETS TO THIS FILE//g' local_docker_env_template > docker/.env \
        && echo "Created docker/.env"; \
    else echo "docker/.env already exists. Delete it first to recreate it."; \
fi


echo "Starting docker build...\n"
docker-compose -f docker-compose.yml -f docker-compose-test.yml rm -f && docker-compose -f docker-compose.yml -f docker-compose-test.yml pull
python ./docker/env_writer.py ./docker/env.json ./docker/env.test.json
docker-compose up -d --build

read -e -p "Would you like to clone databases? [Y/n] " YN

if [[ $YN != "n" && $YN != "N" && $YN != "" ]]; then
    echo "#######################################################\n\n \
    Checking for pg_dump in PATH... \n\n\
    #######################################################\n\n"
    pg_dump --version || pg_dump_not_found

    clone_invest_pir_api

fi

echo "#######################################################\n\n \
Logout of Cloud Foundry \n\n\
#######################################################\n\n"
cf logout

echo "#######################################################\n\n \
*** Congratulations *** \n\n\
Everything should now be up and running \n\n\
#######################################################\n\n"
exit 1


