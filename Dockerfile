###########################
#### FOR RASA ACTIONS #####

# Extend the official Rasa SDK image
FROM rasa/rasa-sdk:2.6.0

# Use subdirectory as working directory
WORKDIR /app

# Copy any additional custom requirements, if necessary (uncomment next line)
# COPY actions/requirements-actions.txt ./
COPY actions/. /app/actions

# Change back to root user to install dependencies
USER root

# Install extra requirements for actions code, if necessary (uncomment next line)
# RUN pip install --no-cache-dir -r requirements-actions.txt

# Copy actions folder to working directory
COPY ./actions /app/actions

# By best practices, don't run the code with root user
USER 1001



################################
##### FOR RASA OPEN SOURCE #####

# FROM python:3.7.11

# RUN python -m pip install rasa

# WORKDIR /app
# COPY . .

# # rasa train 
# RUN rasa train

# # set user to run, don't run as root
# USER 1001

# # set entrypoint for interactive shells
# ENTRYPOINT [ "rasa" ]

# # command to run when container is called to run
# CMD [ "run", "--enable-api", "--port", "8080" ]
