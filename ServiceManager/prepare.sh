#!/bin/bash
base_url="52.43.222.42"
function downloadCurrentVersion {
    curl -H "Accept: application/json" -X GET "$base_url/downloadCurrentVersion"  > /home/ubuntu/run.sh
}

function getRepo {
    sudo apt-get install git
    curl -H "Accept: application/json" -X GET "$base_url/downloadRSA" > ~/home/ubuntu/id_rsa
    eval "$(ssh-agent -s)"
    ssh-add /home/ubuntu/.ssh/id_rsa
    mkdir /home/ubuntu/service
    git clone git@github.com:h3y4w/dissect-services.git ~/service 
}

    
downloadCurrentVersion
getRepo
bash run.sh





