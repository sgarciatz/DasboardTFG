if [ $# -lt 3 ]; then
    printf "Se debe ejecutar este script con 3 parametros -> updateSharedFolder.sh <usuario> <contrasena> <urlRemoto> <excludeList>\n"
    exit
fi

shared_folder=${HOME}DashboardTFG/sharedFolder

if [ ! -d  $shared_folder ]; then
    mkdir $shared_folder
fi

printf "\n nextcloudcmd --silent --exclude $4 --user ${1} --password ${2} ${sharedFolder} ${3} \n"

nextcloudcmd --silent --exclude $4 --user $1 --password $2 $shared_folder $3

#/home/sgarciatz/anaconda3/bin/conda activate /home/sgarciatz/anaconda3/envs/prepararMongo

${HOME}anaconda3/envs/prepararMongo/bin/python3.10 ${HOME}DashboardTFG/cargarMongo.py
