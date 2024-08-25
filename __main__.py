"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import ec2

sg = ec2.SecurityGroup('web-server-sg', description="security group for web servers")
allow_ssh = ec2.SecurityGroupRule("AllowSSH", type="ingress", from_port=22, to_port=22, protocol="tcp", cidr_blocks=["0.0.0.0/0"], security_group_id=sg.id)
allow_http = ec2.SecurityGroupRule("AllowHTTP", type="ingress", from_port=80, to_port=80, protocol="tcp", cidr_blocks=["0.0.0.0/0"], security_group_id=sg.id)
allow_egress = ec2.SecurityGroupRule("AllowAllEgress", type="egress", from_port=0, to_port=0, protocol="-1", cidr_blocks=["0.0.0.0/0"], security_group_id=sg.id)

ec2_instance = ec2.Instance('web-server',
                            ami="ami-0230bd60aa48260c6",
                            instance_type="t2.micro",
                            key_name="crossplane_key",
                            vpc_security_group_ids=[sg.id],
                            tags={
                                "Name":"web"
                            }
                            )

pulumi.export('public_ip', ec2_instance.public_ip)