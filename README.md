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

   BACKEND__ORIGINS='["http://172.24.0.4:3000","https://example.com"]'

   NUXT_CSR_API_BASE=https://example.com
   ```

   > You can find the rest of the environment variables and their default values in the `docker-compose.yml` file.

3. Run app

   ```bash
   docker compose up --build
   ```
