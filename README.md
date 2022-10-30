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

- LaceworkURL: _ssm:LaceworkURL_
- LaceworkAccessKeyID: _ssm:LaceworkAccessKeyID_
- LaceworkSecretKey: _ssm:LaceworkSecretKey_


