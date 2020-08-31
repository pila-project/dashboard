#only once
# cmd /
 gcloud compute firewall-rules create default-allow-http-5000 \
    --allow tcp:5000 \
    --source-ranges 0.0.0.0/0 \
    --target-tags http-server \
    --description "Allow port 5000 access to http-server"