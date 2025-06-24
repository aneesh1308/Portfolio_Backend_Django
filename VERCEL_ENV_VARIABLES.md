# Vercel Environment Variables for MongoDB Deployment

## Copy these exact values to Vercel Project Settings → Environment Variables:

### Django Core Settings
```
DEBUG=false
DJANGO_SECRETE_KEY=your-super-secret-django-key-here-min-50-characters-long-12345
```

### MongoDB Configuration (Recommended)
```
USE_MONGODB=true
MONGODB_URI=mongodb+srv://araneesh08:Anee%26H08@cluster0.9xqcy0k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
MONGODB_NAME=portfolio_db
MONGODB_USERNAME=araneesh08
MONGODB_PASSWORD=Anee&H08
MONGODB_AUTH_SOURCE=admin
```

### Cloudinary Settings (Media Storage)
```
CLOUDINARY_CLOUD_NAME=dgqkqvkkm
CLOUDINARY_API_KEY=856745949455318
CLOUDINARY_API_SECRET=q8caMXB0bFV1y3B_G9xxnX1Iwkc
```

## Important Notes:

1. **Replace `YOUR_PASSWORD_HERE`** in MONGODB_URI with your actual MongoDB password
2. **Replace `YOUR_ACTUAL_MONGODB_PASSWORD`** with the same password
3. The **DJANGO_SECRETE_KEY** should be at least 50 characters long
4. All other values can be used as-is

## After Deployment:

- **API Base URL**: `https://your-project.vercel.app/`
- **Resume ID for Frontend**: `8e26c392-d2e9-45a8-b8b3-36fb5a65e6cc`
- **Admin Login**: admin@portfolio.com / admin123

## Frontend Usage:

```javascript
const apiUrl = "https://your-project.vercel.app/";
const resumeId = "8e26c392-d2e9-45a8-b8b3-36fb5a65e6cc";

// Your existing code will work:
const response = await fetch(`${apiUrl}api/resumes/${resumeId}/`, {
  headers: {
    "Content-Type": "application/json",
  },
});
``` 