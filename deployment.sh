#/bin/bash

#Ask lambda details
read -r -p "Select an environment (d- for dev; p - for production)" envabv

echo "Define handler of this AWS Lambda (default: code.lambda_function.lambda_handler)"
read handler

if [[ "$envabv" =~ ^([dD])$ ]];
then
  env="dev"
elif [[ "$envabv" =~ ^([pP])$ ]];
then
  env="production"
else
  echo "Invalid environment"
  exit 1
fi

# Code filename
response="N" #Never create a new lambda with this script
datetime=$(date +"%Y-%m-%dT%H_%M_%S")
codefilename="code$datetime.zip"
layerfilename="python$datetime.zip"
tmpjsonlayerfilename="tmpjsonlayer.json"
codepath=deployments/code
dependenciespath=deployments/dependencies
codefolder=codefolder
lambdaname="vivanta-aggregated-parameters-$env"
layerdescription="$lambdaname-$env"
layername="$lambdaname-$env"
# Making code and dependencies folders
mkdir -p $codepath
mkdir -p $dependenciespath

# Zip for code deployment
find code/ -name '*.py' | cpio -pdm $codefolder
rm $codefolder/code/cmd_lambda_function.py
cd $codefolder
zip -r $codefilename code
cd ..
mv $codefolder/$codefilename $codepath
rm -r $codefolder

# Zip for dependencies
mkdir python
pipenv run pip freeze > requirements.txt
pipenv run pip3 install requests -r requirements.txt -t python
zip -r $layerfilename python/*
mv $layerfilename $dependenciespath
rm -r python

# Setting default handler
if [ -z "${handler}" ]; then
  handler="code.lambda_function.lambda_handler"
fi

# Variables
env_file=".env.$env"
cp $env_file .env.aws
sed -i ':a;N;$!ba;s/\n/,/g' .env.aws
env=$(cat .env.aws)
# Deploy layer
# echo "Deploying layer..."
# aws lambda publish-layer-version --layer-name $layername --description "$layerdescription" --license-info "MIT" --zip-file fileb://$dependenciespath/$layerfilename --compatible-runtimes python3.6 python3.7 python3.8 --compatible-architectures "arm64" "x86_64" > $tmpjsonlayerfilename

# Getting layer arn from file
# layerarn="$(grep -oP '(?<="LayerArn": ")[^"]*' $tmpjsonlayerfilename)"
# version="$(grep -oP '(?<="Version": )[^,]*' $tmpjsonlayerfilename)"
rm $tmpjsonlayerfilename
echo $layerarn:$version
# Deploy lambda
echo "Deploying lambda..."
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]];
then
  aws lambda create-function --function-name $lambdaname \
  --zip-file fileb://$codepath/$codefilename --handler $handler --runtime python3.10 \
  --role arn:aws:iam::036497184801:role/vivanta-lambda-stg \
  # --layers $layerarn:$version \
  --vpc-config SubnetIds=subnet-0deef7c7db1b35a70,subnet-08c72e4ac202b6198,SecurityGroupIds=sg-01e5b7c150d395d4d

  aws lambda update-function-configuration --function-name $lambdaname \
    --environment "Variables={$env}"
else
  aws lambda update-function-code --function-name $lambdaname \
  --zip-file fileb://$codepath/$codefilename

  aws lambda update-function-configuration --function-name $lambdaname \
    --environment "Variables={$env}" \
    --vpc-config SubnetIds=subnet-0deef7c7db1b35a70,subnet-08c72e4ac202b6198,SecurityGroupIds=sg-01e5b7c150d395d4d
fi
