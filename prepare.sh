#!/bin/bash
export FILE='%s'

base_url="52.43.7.201"
function downloadCurrentVersion {
    curl -H "Accept: application/json" -X GET "$base_url/downloadCurrentVersion"  > /home/ubuntu/run.sh
}



function getRepo {
    curl -H "Accept: application/json" -X GET "$base_url/downloadRSA" > /home/ubuntu/.ssh/id_rsa
    eval "$(ssh-agent -s)"
    sudo ssh-add /home/ubuntu/.ssh/id_rsa
    cd /home/ubuntu/
    git clone git@github.com:h3y4w/dissect-workers.git
}





downloadCurrentVersion
getRepo
bash /home/ubuntu/run.sh




