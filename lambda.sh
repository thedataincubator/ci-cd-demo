#!/bin/bash

if [[ $# != 2 ]]; then
    echo "Usage: $0 [create|delete] function-name"
    exit 1
fi

action=$1
functionname=$2
rolename="$2-role"

if [[ $action == 'create' ]]; then
    echo "Creating lambda function $functionname"

    set -e
    set -x

    roleres=$(aws iam create-role --role-name $rolename --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}')
    echo $roleres
    aws iam attach-role-policy --role-name $rolename --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

    rolearn=`echo $roleres | python -c "import sys; import json; print(json.loads(sys.stdin.read())['Role']['Arn'])"`

    sleep 10

    zip deployment.zip lambda_function.py
    aws lambda create-function --function-name $functionname --runtime python3.10 --zip-file fileb://deployment.zip --handler lambda_function.lambda_handler --role $rolearn
    aws lambda add-permission --function-name $functionname --statement-id AllowURLAccess --action lambda:InvokeFunctionUrl --principal '*' --function-url-auth-type NONE
    aws lambda create-function-url-config --function-name $functionname --auth-type NONE

    set +x
elif [[ $action == 'delete' ]]; then
    echo "Deleting lamdba function $functionname"
    
    set -x
    
    aws lambda delete-function --function-name $functionname
    aws iam detach-role-policy --role-name $rolename --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
    aws iam delete-role --role-name $rolename

    set +x
fi
