# CARE is a app dedicated to global well-being,education,training promotion mainly for children education and well-being.
This app is so global opinions,advice forums app
Global development ideas sharing and talking app.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Deployment on Tencent Cloud

This application is ready to be deployed as a containerized application on Tencent Cloud. Here are the steps to deploy it.

### Prerequisites

* A Tencent Cloud account.
* Docker installed on your local machine.
* `tcli`, the Tencent Cloud CLI, installed and configured on your local machine.

### 1. Build the Docker Image

First, build the Docker image for the application:

```bash
docker build -t care-app .
```

### 2. Set up Tencent Container Registry (TCR)

1.  **Create a TCR instance:** In the Tencent Cloud console, navigate to the Tencent Container Registry (TCR) service and create a new registry instance if you don't have one already.
2.  **Create a namespace:** Within your TCR instance, create a new namespace (e.g., `care-app-repo`).
3.  **Create a repository:** In the namespace, create a new repository for the application image (e.g., `care-app`).
4.  **Log in to TCR:** Use the `tcli` or the Docker client to log in to your TCR instance. You will find the login command in the TCR console.

    ```bash
    docker login <your-tcr-instance-name>.tencentcloudcr.com -u <your-username> -p <your-password>
    ```

5.  **Tag and push the image:** Tag your local Docker image with the TCR repository URL and push it:

    ```bash
    docker tag care-app:latest <your-tcr-instance-name>.tencentcloudcr.com/<your-namespace>/care-app:latest
    docker push <your-tcr-instance-name>.tencentcloudcr.com/<your-namespace>/care-app:latest
    ```

### 3. Set up a Production Database

This application uses a SQLite database by default, which is not suitable for production. You should set up a production-ready database, such as **TencentDB for PostgreSQL**.

1.  **Create a database instance:** In the Tencent Cloud console, create a new TencentDB for PostgreSQL instance.
2.  **Configure the database:** Create a new database and a user for the application.
3.  **Get the database URL:** The database URL will be in the following format:

    ```
    postgresql://<user>:<password>@<host>:<port>/<dbname>
    ```

### 4. Deploy the Application

You can deploy the application on either **Tencent Kubernetes Engine (TKE)** or **Cloud Run**.

#### Option A: Deploy on Tencent Kubernetes Engine (TKE)

1.  **Create a TKE cluster:** If you don't have one, create a new TKE cluster in the Tencent Cloud console.
2.  **Create a deployment:** Create a new deployment in your TKE cluster.
    *   **Image:** Use the TCR image URL from the previous step.
    *   **Port:** Expose port 5000.
    *   **Environment Variables:** Set the following environment variables:
        *   `SECRET_KEY`: A long, random string for signing session cookies.
        *   `DATABASE_URL`: The URL of your production database.

3.  **Create a service:** Create a service of type `LoadBalancer` to expose the deployment to the internet.

#### Option B: Deploy on Cloud Run

1.  **Create a Cloud Run service:** In the Tencent Cloud console, navigate to the Cloud Run service and create a new service.
2.  **Configure the service:**
    *   **Image:** Select the TCR image you pushed earlier.
    *   **Port:** Set the container port to 5000.
    *   **Environment Variables:** Set the `SECRET_KEY` and `DATABASE_URL` environment variables as described above.
3.  **Deploy:** Deploy the service. Cloud Run will provide you with a public URL for your application.

### 5. Using EdgeOne (Optional)

After your application is deployed and running, you can use **Tencent Cloud EdgeOne** to put a CDN in front of your application. This can help to improve performance, security, and reliability.

1.  **Create an EdgeOne zone:** In the EdgeOne console, create a new zone for your application's domain.
2.  **Configure the origin:** Set the origin to the public URL of your TKE service or Cloud Run service.
3.  **Configure DNS:** Update your domain's DNS records to point to the EdgeOne nameservers.
