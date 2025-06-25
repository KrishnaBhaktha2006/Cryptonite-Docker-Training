# Step A: Start with a base image that already has Python
FROM python:3.11-slim

# Step B: Set the "current folder" inside the container
WORKDIR /app

# STEP 3: Create a dedicated, non-root user for our app.
# -r creates a system user (no home directory by default).
# -s /bin/false means this user cannot get an interactive shell.
# 'appuser' is the name we are giving our new user.
RUN useradd -r -s /bin/false appuser

# Step C: Copy ONLY the requirements file first and install packages
# This is a clever optimization. If our requirements don't change,
# Docker can reuse a cached layer, making future builds much faster.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Step D: Now, copy the rest of your application code into the container
COPY . .

# STEP 6: Change ownership of the app directory to our new user.
# This gives our 'appuser' permission to read/write files in /app.
# The -R flag means "recursive" (change all files and subdirectories).
RUN chown -R appuser:appuser /app

# STEP 7: Switch from the 'root' user to our new 'appuser'.
# All subsequent commands will be run as 'appuser'.
USER appuser

# Step F: Open a "window" on the container at port 5000
EXPOSE 5000

# Step G: The final command to run when the container starts
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]