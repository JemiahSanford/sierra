#!usr/bin/env python3

import argparse
import json
import sys

from trosposphere import Parameter, Ref, Template
from troposphere.ecs import (Cluster, Service, TaskDefinition,     
                             ContainerDefinition, NetworkConfiguration,     
                             AwsvpcConfiguration, PortMapping )


template = Template()
template.add_version('2010-09-09')  


#define Metadata
template.add_metadata({
    'AWS::CloudFormation::Init':{
        'config': config({
            'commands':[            
                '01_add_instance_to_cluster':[
                    'command': '!Sub echo ECS_CLUSTER=${Cluster} > /etc/ecs/ecs.config'
                ]
            ]
            'files':[
                '/etc/cfn/cfn-hup.conf':[
                    'mode': 000400,
                    'owner': 'root',
                    'group': 'root',
                    'content': '!Sub |'
                        '[main]'
                        'stack=${AWS::StackId}'
                        'region=${AWS::Region}'
                ],
                '/etc/cfn/hooks.d/cfn-auto-reloader.conf':[
                    'content': '!Sub |'
                        '[cfn-auto-reloader-hook]'
                        'triggers=post.update'
                        'path=Resources.ContainerInstances.Metadata.AWS::CloudFormation::Init'
                        'action=/opt/aws/bin/cfn-init -v --region ${AWS::Region} --stack ${AWS::StackName} --resource LaunchConfiguration'
                ]
            ]
            'services':[
                'sysvinit':[
                    'cfn-hup': [
                        'enabled': 'true',
                        'ensureRunning': 'true'
                        'files': [
                            '/etc/cfn/cfn-hup.conf',
                            '/etc/cfn/hooks.d/cfn-auto-reloader.conf'
                        ]
                    ]
                ]
            ]
        }),
    }                
})


#define Outputs 
template.add_outputs(Outputs(
    'ClusterName':
        'Value': '!Ref Cluster'
))



#define Parameters
template.add_parameter(Parameter(
    'ImageId',
    Type = 'AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>',
    Default = '/aws/service/ecs/optimized-ami/amazon-linux/recommended/image_id',
    Description = '> An SSM parameter that resolves to a valid AMI ID. This is the AMI that will be used to create ECS hosts. The default value is the currently recommended ECS-optimized AMI.'
))

template.add_parameter(Parameter(
    'InstanceType',
    Type = 'String',
    Default = "t2.micro"
))

template.add_parameter(Parameter(
    'ClusterSize',
    Type = 'Number'
    Default = 2
))

template.add_parameter(Parameter(
    'KeyName',
    Type = 'AWS::EC2::KeyPair::KeyName'
))

template.add_parameter(Parameter(
    'SourceSecurityGroup',
    Type = 'AWS::EC2::KeyPair::KeyName'
))

template.add_parameter(Parameter(
    'Subnets',
    Type = 'List<AWS::EC2::Subnet::Id>'
))

template.add_parameter(Parameter(
    'VPC',
    Type = 'AWS::EC2::VPC::Id'
))


EcsHostRole = template.add_resource(IAM(
    Type = 'AWS::IAM::Role'
    'Properties':       
    'Path: /       
    AssumeRolePolicyDocument:
    
    




))






