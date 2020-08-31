
if [ $1 == "prod" ]; then

  echo "$1 environment, $2 project"   #$2 xxxx-277913

  source /Users/bonaventurapacileo/google-cloud-sdk/completion.bash.inc
  source /Users/bonaventurapacileo/google-cloud-sdk/path.bash.inc

  #once per session
  #gcloud auth login

  #ensure you are in the correct wd
  docker build -t flaskdash:latest .
  docker tag flaskdash gcr.io/$2/flaskdash:latest
  docker push gcr.io/$2/flaskdash:latest

  #create gce instance from container and run as privileged
  gcloud compute instances create-with-container flaskdash-pila-v4 \
  --zone europe-west4-a \
  --tags http-server,https-server \
  --container-image=gcr.io/$2/flaskdash \
   --container-privileged

  #once deployed, app available at External IP:5000 if FIREWALL RULES shell has been run in the project.

elif [ $1 == "dev" ]; then

    echo "$1 environment"

    pip install -r requirements.txt

    export FLASK_APP=app.py

    python -m flask run

fi
