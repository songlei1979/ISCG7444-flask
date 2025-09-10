
# ISCG7444 Flask App – Docker Deployment on Claw.Cloud Run

This project demonstrates how to package a Flask application using Docker and deploy it to [Claw.Cloud Run](https://run.claw.cloud), a cloud platform for running containerized apps.

---

## 🧱 Step 1: Create Dockerfile

Create a `Dockerfile` in the root of your Flask project directory with the following content:

```Dockerfile
# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app source code
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Set environment variable for Flask
ENV FLASK_APP=app.py

# Start the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
```

### Explanation:
- `FROM python:3.10-slim`: Uses a lightweight official Python base image.
- `WORKDIR /app`: All files and commands will operate from `/app`.
- `COPY requirements.txt .` and `RUN pip install`: Install dependencies.
- `COPY . .`: Copies the entire project folder.
- `EXPOSE 5000`: Makes the container's port 5000 available.
- `CMD`: Starts the Flask server on 0.0.0.0:5000.

---

## 🔐 Step 2: Docker Hub Login

You need to **log in to Docker Hub** to push your image:

```bash
docker login
```

> 🔐 If you use **Google to sign into Docker Hub**, you must [generate an Access Token](https://hub.docker.com/settings/security) and use it as your password.

---

## 🛠️ Step 3: Build & Push Docker Image

Use Docker Buildx to build the image for the correct architecture and push it to Docker Hub.

```bash
# Create builder (only once)
docker buildx create --use

# Build and push the image
docker buildx build --platform linux/amd64   -t your_repository_name/iscg7444-flask:latest   --push .
```

Replace `your_repository_name` with your Docker Hub username.

---

## 🚀 Step 4: Deploy to Claw.Cloud Run

1. Visit: [https://run.claw.cloud](https://run.claw.cloud)
2. Click **Create App**
3. Choose **Deploy from Docker Image**
4. Enter your image URL:

   ```
   docker.io/your_repository_name/iscg7444-flask:latest
   ```

5. Set **Container Port** to:

   ```
   5000
   ```

6. Under **Resource Limits**, configure:

| Resource | Value   |
|----------|---------|
| CPU      | 0.1     |
| Memory   | 128Mi   |

7. Click **Deploy**

> 📝 It may take a minute or two to pull the image and start the container.

---

## 🌐 Step 5: Access Your App

Once deployed, Claw.Cloud Run will provide you with a public URL like:

```
https://your-app-name.run.claw.cloud
```

Visit it in your browser to confirm it's working.

---

## 🧪 Step 6: Run Locally (Optional)

To test locally before deploying:

```bash
docker run -p 5000:5000 your_repository_name/iscg7444-flask:latest
```

Then open: [http://localhost:5000](http://localhost:5000)

---

## 📁 Example Project Structure

```
iscg7444-flask/
├── app.py
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## ✅ Requirements

- Your `requirements.txt` must include `flask`.
- The main file should be `app.py`, or update the `FLASK_APP` env variable in Dockerfile.

---

## 👩‍🏫 Author

Lei Song  
Senior Lecturer – Cloud Application Development  
Unitec Institute of Technology  
