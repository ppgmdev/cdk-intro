# CDK Intro!

This project deploys a lambda function that talks to Bedrock Claude 3 Sonnet and saves the output into a DynamoDB table.

```bash
git clone https://github.com/ppgmdev/cdk-intro.git
cd cdk-intro
npm install
npx cdk deploy
```

Once the stack is deployed, you can change the lambda function name in the assistant.sh file in line 14.
```bash
FUNCTION_NAME="YOUR LAMBDA NAME"
```

Once done, you can call the assistant from your terminal. Make sure you are at `cdk-intro` in your terminal.
```bash
sh assistant.sh "Create a list of 10 pop songs"
```
Example output:
```
Response:
{"statusCode": 200, "body": "Here's a list of 10 popular pop songs:\n\n1. \"Blinding Lights\" by The Weeknd\n2. \"Levitating\" by Dua Lipa\n3. \"Watermelon Sugar\" by Harry Styles\n4. \"Savage\" by Beyoncé featuring Megan Thee Stallion\n5. \"Say So\" by Doja Cat\n6. \"Circles\" by Post Malone\n7. \"Rockstar\" by DaBaby featuring Roddy Ricch\n8. \"Rain on Me\" by Lady Gaga featuring Ariana Grande\n9. \"Toosie Slide\" by Drake\n10. \"Cardigan\" by Taylor Swift"}
```

## Useful CDK commands

* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
* `npx cdk deploy`  deploy this stack to your default AWS account/region
* `npx cdk diff`    compare deployed stack with current state
* `npx cdk synth`   emits the synthesized CloudFormation template
