# WML

## How to setup and run

1. Clone git project

   ```bash
   git clone git@github.com:Limbend/wml.git
   ```

2. Create `.env` file

   ```bash
   cd ./wml
   nano .env
   ```

   `.env` example:

   ```.env
   BACKEND__DB__PASSWORD=your_db_password
   BACKEND__DB__ECHO=false

   BACKEND__S3__ACCESS_KEY=your_s3_access_key
   BACKEND__S3__SECRET_KEY=your_s3_secret_key
   BACKEND__S3__ENDPOINT_URL=https://s3.example.com

   BACKEND__ORIGINS='["http://172.24.0.4:3000","https://example.com"]'

   MINIO__USER=your_minio_user
   MINIO__PASSWORD=your_minio_password
   MINIO__LOCAL__PATH="./backend/.np.s3_data"
   MINIO__LOCAL__UIDGID="1024:1024"

   NUXT_CSR_API_BASE=https://example.com
   ```

   > You can find the rest of the environment variables and their default values in the `docker-compose.yml` file.

   > Access and secret keys from S3 you will receive after MinIO configuration.

3. Run only MinIO for initial setup

   ```bash
   docker compose up wml_s3
   ```

   1. Open the web interface of MinIO. Default address: http://localhost:9401

   2. Generate keys in the `Access Keys` tab

   3. Create Bucket

   4. Add read-only permissions for the anonymous user.

      In the Bucket settings, `Anonymous` tab. When creating a rule, specify Prefix - `/`

4. Run app

   ```bash
   docker compose up --build
   ```
