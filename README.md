# PILA dashboard

[Conceptual mapping of Karel indicators](https://docs.google.com/drawings/d/1A8KhKQJ4ryChVazJKYhgPlTaB-iFcCZ8VmQ-XreGiOM/edit)


The diagram below presents a high-level overview of the proposed **Dashboard**. A loosely coupled architecture ensures system reliability in case of failures along the pipeline. The system is composed of three components:
 - a **Data Processing** service that i) pulls data from KnowLearning (or from another database, e.g. Firestore), ii) processes it and iii) stores the results in a bucket;
 - a **Storage** service where final results could be stored;
 - a **Dashboard** that presents the final results;

The working assumption is that there is no need to display real-time data, albeit this could be changed further than down the line thanks to the modular architecture. In fact, building the system around microservices makes the architecture modular, loosely coupled and thus more resilient to breaks.

![](./images/pila_dashboard_high.png)

This system could be implemented on Google Cloud Platform as shown in the diagram below. The **Data Processing** service could be configured as a *Cloud Function* with either an event-driven or a pub/sub trigger (e.g. hourly updates). Google *Cloud Storage* buckets could provide the storage service and the **Dashboard** (developed in Flask) could be hosted on a *Compute Engine* instance.

![](./images/pila_dashboard_gcp.png)


