# AWS Control Tower Customizations

![Lacework](https://user-images.githubusercontent.com/6440106/152378397-90c862e9-19fb-4427-96d0-02ca6c87f4dd.png)

## Overview
This repository contains Control Tower Customizations. These are CloudFormation-based Service Catalog products that can executed during
AWS Control Tower account provisioning using Account Factory.

## List of Customizations

### Lacework Config Type Provisioning
This CloudFormation template provisions the Lacework Config Type account.

#### CloudFormation Parameters
The following CloudFormation parameters may be set via SSM parameters instead of specifying as input in the template.

- Your Lacework URL: _ssm:LaceworkURL_
- Lacework Admin Access Key ID: _ssm:LaceworkAccessKeyID_
- Lacework Admin Secret Key: _ssm:LaceworkSecretKey_

### Deploy the CloudFormation Template

1. Click on the following Launch Stack button to go to your CloudFormation console and launch the template.

   [![Launch](https://user-images.githubusercontent.com/6440106/153987820-e1f32423-1e69-416d-8bca-2ee3a1e85df1.png)](https://console.aws.amazon.com/cloudformation/home?#/stacks/create/review?templateURL=https://lacework-alliances.s3.us-west-2.amazonaws.com/lacework-aws-ct-customizations/templates/provision-lacework-config.template.yml)

   For most deployments, you only need the Basic Configuration parameters.
   ![basic_configuration](https://user-images.githubusercontent.com/6440106/198918292-24b2fc0c-4093-43f0-9a18-b855c0b095e0.png)
   Specify the following Basic Configuration parameters:
    * Enter a **Stack name** for the stack.
    * Enter **Your Lacework URL**.
    * Enter your **Lacework Admin Access Key ID** and **Lacework Admin Secret Key** that you copied from your API Keys file. See [here](https://docs.lacework.com/console/generate-api-access-keys-and-tokens).
3. Click **Next** through to your stack **Review**.
4. Accept the AWS CloudFormation terms and click **Create stack**.

