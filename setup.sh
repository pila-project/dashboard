
#$1 /Users/bonaventurapacileo/google-cloud-sdk/
#gcloud path
source $1/completion.bash.inc
source $1/path.bash.inc


#from cwd
docker build -t helloworld:latest .


docker tag helloworld gcr.io/lexical-archery-252114/helloworld:latest

#once per session
#gcloud auth login

#then
docker push gcr.io/lexical-archery-252114/helloworld:latest


#create gce instance from container and run as privileged

#once deployed, app available at External IP:5000

#--image-family ubuntu-minimal-1804-lts --image-project cost-stable \

gcloud compute instances create-with-container flask-pilatest88 \
--zone europe-west4-a \
--tags http-server,https-server \
--container-image=gcr.io/lexical-archery-252114/helloworld \
 --container-privileged

#only once
# gcloud compute firewall-rules create default-allow-http-5000 \
 #   --allow tcp:5000 \
  #  --source-ranges 0.0.0.0/0 \
   # --target-tags http-server \
    #--description "Allow port 5000 access to http-server"


