cdk destroy --app "python app.py" --all --require-approval never

if [ $? -eq 0 ]; then
	  echo "Success:Stack Destroyed Successfully."
    else
          echo "Error: Stack Destroy Failed."
	  exit 1
fi

