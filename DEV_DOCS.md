---------------------------------------
Install docker
---------------------------------------
    https://docs.docker.com/install

---------------------------------------
run local:  
---------------------------------------
docker image build -t paws-data-pipeline .
docker container run --publish 5000:5555 --name pdp -d paws-data-pipeline

---------------------------------------
API:  
---------------------------------------
Run http GET request like:    
- http://localhost:5555/listFiles
- http://localhost:5555/file/{fileName}
- http://localhost:5555/execute/{scriptName}
- http://localhost:5555/allFiles 

---------------------------------------  
Using Private Network with Production:
---------------------------------------
Private IP (can use after added to ZeroTier):    
Replace http://localhost with - http://10.147.20.146:5000/

If you signed the confidentiality agreement document and want access to the server, please download zeroTier software (https://www.zerotier.com/), create an account online, sign in, and then let Uri know on Slack. He’ll send you the id of the network and then you need to send him your node ID; then you can use the api in the private server

---------------------------------------
Deploy:
---------------------------------------
From local machine:
1. zip project folder: `tar -czvf src.tar.gz src`
2. scp project to server: `scp src.tar.gz [usrmname]@paws-data-pipeline.team-machine.phl.io:/home/[usrmname]/paws-data-pipeline`
3. ssh to server: `ssh [usrmname]@paws-data-pipeline.team-machine.phl.io`

In server:
1. `cd paws-data-pipeline`
2. run `sh run.sh`