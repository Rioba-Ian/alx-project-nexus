# Cloud Database Setup for Jobs Board Application

This guide explains how to set up and connect your Jobs Board application to an external cloud-based PostgreSQL database instead of using the Docker container database.

## 1. Create a Cloud PostgreSQL Database

You have several options for cloud PostgreSQL providers:

### Option A: AWS RDS
1. Log in to the AWS Management Console
2. Navigate to RDS service
3. Click "Create database"
4. Select PostgreSQL as the engine
5. Choose your preferred settings (storage, instance class, etc.)
6. Set up security groups to allow connections from your application

### Option B: DigitalOcean Managed Database
1. Log in to DigitalOcean
2. Navigate to "Databases" in the left menu
3. Click "Create Database Cluster"
4. Select PostgreSQL as the engine
5. Choose your preferred settings (region, size, etc.)

### Option C: Render PostgreSQL
1. Create an account on Render.com
2. Navigate to "New+" and select "PostgreSQL"
3. Configure your database settings

## 2. Get Your Database Connection Information

After creating your database, collect the following information:
- Database hostname/endpoint
- Port (typically 5432 for PostgreSQL)
- Database name
- Username
- Password

## 3. Update Your Environment Variables

Update your `.env` and `.env.prod` files with the cloud database connection information:

```
# External Database settings
DATABASE_URL=postgres://your_username:your_password@your_hostname:5432/your_database
```

## 4. Security Recommendations

1. **Use SSL Connections**: Ensure your `DATABASE_URL` uses SSL by adding `?sslmode=require` at the end:
   ```
   DATABASE_URL=postgres://username:password@hostname:5432/database?sslmode=require
   ```

2. **Restrict Network Access**: Configure your database to only accept connections from your application's IP address.

3. **Use Strong Passwords**: Use a strong, unique password for your database user.

4. **Least Privilege**: Create a database user with only the permissions needed by your application.

## 5. Database Migration

If you're migrating from a local database to cloud:

1. Create a backup of your local database:
   ```bash
   pg_dump -U postgres -d your_local_db > backup.sql
   ```

2. Restore to your cloud database:
   ```bash
   psql -h your_cloud_host -U your_username -d your_database < backup.sql
   ```

## 6. Testing the Connection

Test your connection from your local machine:

```bash
psql -h your_cloud_host -U your_username -d your_database
```

You should see a PostgreSQL prompt if successful.

## 7. Environment-Specific Configuration

For different environments (development, staging, production), maintain separate `.env` files with the appropriate database connection strings.

## 8. Troubleshooting

If you encounter connection issues:

1. Check network connectivity (ping the database host)
2. Verify firewall rules allow traffic on port 5432
3. Confirm your connection string format is correct
4. Check that your database user has appropriate permissions

For more detailed PostgreSQL connection troubleshooting, refer to the [official PostgreSQL documentation](https://www.postgresql.org/docs/).
