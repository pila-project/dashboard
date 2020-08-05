
#$1 /Users/bonaventurapacileo/google-cloud-sdk/
#$2 xxxx-277913
#gcloud path
source $1/completion.bash.inc
source $1/path.bash.inc


#from cwd
docker build -t flaskdash:latest .


docker tag flaskdash gcr.io/$2/flaskdash:latest

#once per session
#gcloud auth login

#then
docker push gcr.io/$2/flaskdash:latest


#create gce instance from container and run as privileged

#once deployed, app available at External IP:5000

#--image-family ubuntu-minimal-1804-lts --image-project cost-stable \

gcloud compute instances create-with-container flaskdash-pila-v2 \
--zone europe-west4-a \
--tags http-server,https-server \
--container-image=gcr.io/$2/flaskdash \
 --container-privileged

#only once
# cmd /
# gcloud compute firewall-rules create default-allow-http-5000 \
#    --allow tcp:5000 \
#    --source-ranges 0.0.0.0/0 \
#    --target-tags http-server \
#    --description "Allow port 5000 access to http-server"


