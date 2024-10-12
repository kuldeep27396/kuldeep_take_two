# Weather Data ETL Pipeline

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Components](#components)
4. [Data Flow](#data-flow)
5. [Scalability and Reliability](#scalability-and-reliability)
6. [Failure Handling](#failure-handling)
7. [Cost Optimization](#cost-optimization)
8. [Setup and Configuration](#setup-and-configuration)
9. [Monitoring and Maintenance](#monitoring-and-maintenance)

## Overview

This project implements an ETL (Extract, Transform, Load) pipeline for processing weather data from the OpenWeatherMap API. The pipeline is designed to run on Google Cloud Platform (GCP), leveraging various cloud services to ensure scalability, reliability, and cost-effectiveness.

## Architecture

![ETL Pipeline Architecture](Architecture/Part%202%20Architecture.png)

The architecture diagram above illustrates the high-level design of our ETL pipeline. It showcases the flow of data from the OpenWeatherMap API through various GCP services, ultimately landing in BigQuery for analysis.

## Components

### 1. Astronomer Airflow
- **Purpose**: Orchestration and scheduling of the ETL workflow
- **Key Features**:
  - DAG (Directed Acyclic Graph) management
  - Task scheduling and retries
  - Monitoring and alerting

### 2. Dataproc
- **Purpose**: Data processing and transformation
- **Technologies**:
  - Apache Spark for large-scale data processing
  - Pandas for smaller datasets and data science tasks
- **Key Features**:
  - Scalable cluster management
  - Integration with GCS and BigQuery

### 3. Google Cloud Storage (GCS)
- **Purpose**: Data lake for storing raw and processed data
- **Data Format**: Parquet
- **Key Features**:
  - High durability and availability
  - Lifecycle management
  - Integration with Dataproc and BigQuery

### 4. BigQuery
- **Purpose**: Data warehousing and analytics
- **Key Features**:
  - Serverless architecture
  - Fast query performance on large datasets
  - Integration with BI tools

## Data Flow

1. **Extraction**: 
   - Airflow triggers the extraction process
   - Dataproc job fetches data from OpenWeatherMap API
   - Raw data is stored in GCS in Parquet format

2. **Transformation**:
   - Airflow initiates the transformation job
   - Dataproc processes the raw data using Spark or Pandas
   - Transformed data is stored back in GCS

3. **Loading**:
   - Airflow triggers the loading process
   - Transformed data is loaded into BigQuery tables
   - Data is now ready for analysis and reporting

## Scalability and Reliability

- **Dataproc**: Clusters can be dynamically scaled based on workload
- **GCS**: Automatically scales to handle increasing data volumes
- **BigQuery**: Serverless architecture allows for automatic scaling
- **Airflow**: Can be scaled horizontally to manage complex workflows

Reliability is ensured through:
- Managed services reducing operational overhead
- Built-in redundancy in GCS and BigQuery
- Airflow's task retry mechanisms

## Failure Handling

1. **API Rate Limits**: 
   - Implement exponential backoff in Airflow tasks
   - Use Airflow sensors to pace API calls

2. **Long-running Processes**:
   - Leverage Dataproc's ability to handle long Spark jobs
   - Use Airflow SLAs and timeouts for monitoring

3. **Data Quality Issues**:
   - Implement data validation tasks in Airflow DAGs
   - Use Spark for data cleansing and error handling

4. **Network Failures**:
   - Utilize GCP's global network for reliable connectivity
   - Implement retry logic in tasks and jobs

## Cost Optimization

1. **Dataproc**:
   - Use preemptible VMs for batch processing
   - Implement autoscaling
   - Utilize job-specific clusters

2. **Storage**:
   - Use Parquet format for efficient storage and processing
   - Implement data partitioning and lifecycle policies

3. **BigQuery**:
   - Use partitioned and clustered tables
   - Implement cost controls and quotas

4. **General**:
   - Use data sampling for development and testing
   - Consider BigQuery flat-rate pricing for high query volumes
   - Leverage GCP committed use discounts

## Setup and Configuration

(Include steps for setting up the pipeline, such as creating GCP resources, configuring Airflow, etc.)

## Monitoring and Maintenance

- Use Cloud Monitoring for observing pipeline performance
- Set up alerts for job failures and SLA breaches
- Regularly review and optimize BigQuery queries
- Monitor costs and usage across all components

---

This README provides an overview of the ETL pipeline architecture and its key components. For detailed implementation instructions, please refer to the individual component documentation.