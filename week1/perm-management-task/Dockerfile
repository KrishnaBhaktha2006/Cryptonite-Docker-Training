# We start with a full Ubuntu, because we need its system tools like 'useradd' and 'apt'.
FROM ubuntu:22.04

# This ensures that when we run 'apt install', it doesn't stop and ask for user input.
ENV DEBIAN_FRONTEND=noninteractive

# Here, we create our non-root user named 'user'.
# -m creates its home directory (/home/user).
# -s /bin/bash gives it a nice, interactive shell by default.
RUN useradd -ms /bin/bash user

# We update our software lists and install 'socat', a powerful tool for creating listeners.
# We also clean up afterward to keep the image small.
RUN apt update && apt install -y socat bash && rm -rf /var/lib/apt/lists/*

# This is the "sandbox" for our user, as requested by the prompt.
# 1. We create the directory.
# 2. We give ownership of it to our new 'user'.
# 3. We put a test file in it.
RUN mkdir -p /home/editable && \
    chown user:user /home/editable && \
    echo "test" > /home/editable/info.txt

# We set the starting directory for anyone connecting to the shell.
WORKDIR /home/editable

# This is the command that starts the 'socat' server.
# It listens on port 9001 and, when a connection comes in, it gives that
# connection a 'bash' shell running as the unprivileged 'user'.
CMD ["socat", "TCP-LISTEN:9001,reuseaddr,fork", "EXEC:'su -s /bin/bash user',pty,stderr,setsid,sigint,sane"]
