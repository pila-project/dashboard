
#from cwd
docker build -t helloworld:latest .


docker tag helloworld gcr.io/lexical-archery-252114/helloworld:latest

#then
docker push gcr.io/lexical-archery-252114/helloworld:latest


#create gce instance from container and run as privileged

#once deployed, app available at External IP:5000

#--image-family ubuntu-minimal-1804-lts --image-project cost-stable \


gcloud compute instances create-with-container flask-pila5 \
--zone europe-west4-a \
--tags http-server,https-server \
--container-image=gcr.io/lexical-archery-252114/helloworld \
 --container-privileged


