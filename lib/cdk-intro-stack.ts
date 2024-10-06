import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { aws_dynamodb } from 'aws-cdk-lib';
import { aws_lambda } from 'aws-cdk-lib';
import { CfnOutput } from 'aws-cdk-lib';

export class CdkIntroStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const ddb_table = new aws_dynamodb.TableV2(this, "DDBTable", {
      partitionKey: {
        name: "id",
        type: aws_dynamodb.AttributeType.STRING,
      },
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const lambda_bedrock = new aws_lambda.Function(this, "LambdaBedrock", {
      code: aws_lambda.Code.fromAsset("./lambda/lambda_bedrock"),
      handler: "index.handler",
      runtime: aws_lambda.Runtime.PYTHON_3_12,
      environment: {
        "DDB_TABLE_NAME": ddb_table.tableName,
      }
    });

    new CfnOutput(this, "LambdaARN", {
      value: lambda_bedrock.functionArn,
      description: "ARN of lambda function",
    });
    
    new CfnOutput(this, "DDBName", {
      value: ddb_table.tableName,
      description: "Name of the DDB table",
    });

    new CfnOutput(this, "DDBArn", {
      value: ddb_table.tableArn,
      description: "ARN of the DDB Table",
    });
  }
}
