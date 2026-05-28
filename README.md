#Step-5 README**

Scalability & Reliability Considerations 

How would you schedule this pipeline to run automatically? 

I would schedule the pipeline using tools such as Apache Airflow, GitHub Actions, or a Linux cron-job. In production, Airflow or Cloud Scheduler would be preferred because they provide better retry handling, monitoring, and workflow management. 

How would you know if it failed? 

I would add logging and monitoring for every stage of the pipeline, including API requests, transformations, and BigQuery loads. Failure alerts could be sent through email or Slack notifications whenever a pipeline run fails or returns invalid data. 

What would you add or change if this pipeline needed to scale to 10x the data volume? 

To support larger data volumes, I would implement incremental data loading, table partitioning in BigQuery, and distributed processing tools such as Apache Spark or Google Dataflow. I would also add queue-based ingestion and containerized deployment for improved scalability and reliability.
