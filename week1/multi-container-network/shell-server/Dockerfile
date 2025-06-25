# Start with a minimal base image that has our tools
FROM alpine:latest

# We don't need to install anything because 'alpine' already has 'nc' (netcat).
# The command to run when the container starts.
# This starts a listening server on port 1234.
# When a client connects, it gives them a shell (/bin/sh).
CMD ["nc", "-l", "-p", "1234", "-e", "/bin/sh"]
