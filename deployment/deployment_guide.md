# Deployment Guide

## Overview
This guide provides instructions for deploying the E-Commerce Churn Prediction application. The application consists of a machine learning model exposed via a Streamlit web interface.

## Prerequisites
- Docker
- Docker Compose
- Minimum 2GB RAM available

## Local Deployment (Docker Compose)
The easiest way to run the application is using the provided `docker-compose.yml`.

1. **Clone the repository** (or navigate to the project root).
2. **Build and start the container:**
   ```bash
   docker-compose up --build -d
   ```
3. **Access the application:**
   Open a web browser and navigate to: `http://localhost:8501`
4. **Stop the application:**
   ```bash
    docker-compose down
   ```

## Local Deployment (Standard Python)
If you prefer not to use Docker, you can run it directly:

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Streamlit app:**
   ```bash
   streamlit run app/streamlit_app.py
   ```

## Cloud Deployment (e.g., AWS EC2 / DigitalOcean)
Given the Docker setup, this can be easily deployed to any Virtual Machine:

1. Provision an Ubuntu VM (e.g., AWS t3.small).
2. Install Docker and Docker Compose on the server.
3. SSH into the server and git clone this project.
4. Run `docker-compose up -d`.
5. Ensure port 8501 is open in the server's firewall/security group.

## File Structure Requirements for Deployment
Ensure the following directories are present and populated before building:
- `models/`: Must contain `xgboost.pkl`, `scaler.pkl`.
- `data/processed/`: Must contain `feature_names.json`.
- `app/`: Contains the python scripts for inference and the UI.
