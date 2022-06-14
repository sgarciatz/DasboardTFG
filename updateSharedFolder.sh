if [ $# -lt 3 ]; then
    printf "Se debe ejecutar este script con 3 parametros -> updateSharedFolder.sh <usuario> <contrasena> <urlRemoto>\n"
    exit
fi

shared_folder=$(pwd)/Documents/University/TFG/DashboardTFG/sharedFolder

printf "${shared_folder}\n"

if [ ! -d  $shared_folder ]; then
    mkdir $shared_folder
fi

printf "nextcloudcmd --silent --user ${1} --password ${2} ${sharedFolder} ${3}\n"

nextcloudcmd --user $1 --password $2 $shared_folder $3

/bin/python3.8 /home/santi/Documents/University/TFG/DashboardTFG/cargarMongo.py
