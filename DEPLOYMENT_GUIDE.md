# Django Backend Deployment Guide - Vercel + MongoDB

## Overview
This Django backend supports both PostgreSQL and MongoDB databases with flexible configuration. It's optimized for deployment on Vercel.

## Database Configuration

### Option 1: MongoDB (Recommended for Vercel)
Set these environment variables in Vercel:

```bash
USE_MONGODB=true
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_NAME=portfolio_db
MONGODB_USERNAME=your-username
MONGODB_PASSWORD=your-password
MONGODB_AUTH_SOURCE=admin
```

### Option 2: PostgreSQL (Current setup)
Keep these environment variables:

```bash
USE_MONGODB=false
DATABASE_URL=postgresql://user:password@host:port/database
```

## Vercel Deployment Steps

### 1. Connect Repository
- Go to [Vercel Dashboard](https://vercel.com/dashboard)
- Click "New Project"
- Import your GitHub repository

### 2. Configure Environment Variables
Add these required variables in Vercel Project Settings → Environment Variables:

**Required for all setups:**
```bash
DEBUG=false
DJANGO_SECRETE_KEY=your-super-secret-key-here
CLOUDINARY_CLOUD_NAME=your-cloudinary-name
CLOUDINARY_API_KEY=your-cloudinary-key
CLOUDINARY_API_SECRET=your-cloudinary-secret
```

**For MongoDB setup (recommended):**
```bash
USE_MONGODB=true
MONGODB_URI=your-mongodb-connection-string
MONGODB_NAME=portfolio_db
MONGODB_USERNAME=your-username
MONGODB_PASSWORD=your-password
```

**For PostgreSQL setup:**
```bash
USE_MONGODB=false
DATABASE_URL=your-postgresql-connection-string
```

### 3. Set Build Settings
- **Framework Preset:** Other
- **Build Command:** `bash build_files.sh`
- **Output Directory:** `staticfiles_build`
- **Install Command:** `pip install -r requirements.txt`

### 4. Deploy
Click "Deploy" and wait for the build to complete.

## MongoDB Setup (MongoDB Atlas - Recommended)

### 1. Create MongoDB Atlas Account
- Go to [MongoDB Atlas](https://cloud.mongodb.com/)
- Create a free account and cluster

### 2. Database Configuration
- Create a database named `portfolio_db`
- Create a user with read/write permissions
- Whitelist Vercel IPs (or use 0.0.0.0/0 for all IPs)

### 3. Get Connection String
- Go to Cluster → Connect → Connect your application
- Copy the connection string
- Replace `<password>` with your actual password

## Local Development

### Environment Variables
Create a `.env` file in your project root:

```bash
DEBUG=true
DJANGO_SECRETE_KEY=your-local-secret-key
USE_MONGODB=false  # Use SQLite locally for development
CLOUDINARY_CLOUD_NAME=your-cloudinary-name
CLOUDINARY_API_KEY=your-cloudinary-key
CLOUDINARY_API_SECRET=your-cloudinary-secret
```

### Run Locally
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Key Features

### Flexible Database Support
- **MongoDB**: Primary choice for cloud deployment
- **PostgreSQL**: Production-ready relational database
- **SQLite**: Local development fallback

### Static Files
- **Cloudinary**: Media files (images, videos)
- **Vercel**: Static assets (CSS, JS)

### API Endpoints
- `/api/auth/` - Authentication endpoints
- `/api/resume/` - Resume CRUD operations
- `/api/blogs/` - Blog management
- Check `api/urls.py` for complete endpoint list

## Troubleshooting

### Common Issues

1. **Build Fails**
   - Check if all environment variables are set
   - Verify `requirements.txt` has all dependencies

2. **Database Connection Issues**
   - For MongoDB: Check connection string and credentials
   - For PostgreSQL: Verify DATABASE_URL format

3. **Static Files Not Loading**
   - Ensure CLOUDINARY settings are correct
   - Check `build_files.sh` runs successfully

### MongoDB Migration from PostgreSQL

If you're migrating from PostgreSQL:
1. Export your data from PostgreSQL
2. Set `USE_MONGODB=true` in environment variables
3. Redeploy the application
4. Import data to MongoDB using Django management commands

## Support

For issues related to:
- **Vercel Deployment**: Check Vercel documentation
- **MongoDB**: Refer to MongoDB Atlas documentation
- **Django**: Check Django documentation

## File Structure
```
├── api/                    # Main application
├── backend/               # Django settings
├── build_files.sh        # Vercel build script
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
└── DEPLOYMENT_GUIDE.md   # This file
``` 