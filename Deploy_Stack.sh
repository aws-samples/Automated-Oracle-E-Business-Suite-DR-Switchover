cdk synth --app "python app.py" --all

if [ $? -eq 0 ]; then
    echo "Success:Stack Synth Successfully."
else
    echo "Error: Stack Synth Failed. Fix the error and restart this script."
    exit 1
fi

cdk deploy IamResStack --no-confirm

if [ $? -eq 0 ]; then
    echo "Success:Stack IamResStack Deployed Successfully."
else
    echo "Error: Stack IamResStack Deploy Failed. Fix the error and restart this script."
    exit 1
fi

cdk deploy AtsObjectStack --no-confirm

if [ $? -eq 0 ]; then
    echo "Success:Stack AtsObjectStack Deployed Successfully."
else
    echo "Error: Stack AtsObjectStack Deploy Failed. Fix the error and restart this script."
    exit 1
fi
