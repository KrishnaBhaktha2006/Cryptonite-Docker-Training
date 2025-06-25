# Start with the same minimal base image
FROM alpine:latest

# This is a common trick to make a container run forever without doing anything.
# It simply "tails" a special file that never ends, so the container
# doesn't exit immediately after starting.
CMD ["tail", "-f", "/dev/null"]
