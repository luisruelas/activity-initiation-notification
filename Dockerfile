FROM public.ecr.aws/lambda/python:3.12

# Copy function code
ADD . ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip3 install --no-cache-dir -r ./requirements.txt

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "code.lambda_function.lambda_handler" ]
