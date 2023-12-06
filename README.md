# URL Shortener

URL Shortener is a simple Flask application that allows you to shorten long URLs with specified expiry time.

## Setup Instructions

To run the application locally, follow these setup instructions:

### Prerequisites

Make sure you have Docker and Docker Compose installed on your machine.

- [Docker](https://www.docker.com/get-started)

### Getting Started

1. Clone the repository:

    ```bash
    git clone https://github.com/jenishayadav/url-shortener.git
    cd url_shortener
    ```
2. Create an empty directory `database-data`

    ```bash 
    mkdir database-data
    ```

2. Start the Database Service:

    ```bash
    docker compose up -d database
    ```

   This command starts the database service in the background. Ensure that the database service is up and running before proceeding to the next step.

3. Start the URL Shortener Service:

    ```bash
    docker compose up -d url_shortner
    ```

   This command starts the URL Shortener service in the background. The application APIs should now be accessible at [http://localhost:5000](http://localhost:5000).


    **Note:** separate steps are required only for the first time. After that, you can directly run the following to start both the services.

    ```bash
    docker compose up -d
    ```

## API Signatures

1. Sign Up

    ```bash
    curl --request POST \
        --url http://localhost:5000/sign-up/ \
        --header 'Content-Type: application/json' \
        --data '{
            "name": "test",
            "email": "test@gmail.com",
            "password": "1234567"
        }'
    ```

2. Sign In

    ```bash
    curl --request POST \
        --url http://localhost:5000/sign-in/ \
        --header 'Content-Type: application/json' \
        --data '{
            "email": "jenisha12@gmail.com",
            "password": "1234567"
        }'
    ```

2. Create Short URL

    **NOTE:** Either you can specify `absolute_expiry` or `relative_expiry`.

    ```bash
    curl --request POST \
        --url http://localhost:5000/create-short-url/ \
        --header 'Authorization: Bearer <AUTH-TOKEN>' \
        --header 'Content-Type: application/json' \
        --data '{
            "long_url": "https://serverfault.com/questions/981002/how-to-remove-and-rebuild-a-docker-container",
            "absolute_expiry": "2024-01-03T16:25:36.254878"
        }'
            
    ```

    ```bash
    curl --request POST \
        --url http://localhost:5000/create-short-url/ \
        --header 'Authorization: Bearer <AUTH-TOKEN>' \
        --header 'Content-Type: application/json' \
        --data '{
            "long_url": "https://serverfault.com/questions/981002/how-to-remove-and-rebuild-a-docker-container",
            "relative_expiry": {
                "days": 1,
                "hours": 1,
                "minutes": 2,
                "seconds": 1
            }
        }'
            
    ```



2. Get URLs list

    ```bash
    curl --request GET \
        --url http://localhost:5000/get-urls/ \
        --header 'Authorization: Bearer <AUTH_TOKEN>' \
    ```

2. Access Short URL

    ```bash
    curl -L http://localhost:5000/u/z57qa89o
    ```
    This will follow the redirects and render the long URL. To get only HTTP 302 response, remove `-L`.
