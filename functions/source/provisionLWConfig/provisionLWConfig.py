#
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json
import logging
import os
import random
import string

import urllib3
from crhelper import CfnResource

from aws import send_cfn_fail, send_cfn_success
from honeycomb import send_honeycomb_event
from lacework import setup_initial_access_token, get_lacework_environment_variables, get_account_from_url

from functions.source.common.aws import create_lw_config_cross_account_access_role, \
    delete_lw_config_cross_account_access_role
from functions.source.common.lacework import add_lw_cloud_account_for_cfg

HONEY_API_KEY = "$HONEY_KEY"
DATASET = "$DATASET"
BUILD_VERSION = "$BUILD"

CONFIG_NAME_PREFIX = "Lacework-Control-Tower-Config-Member-"

http = urllib3.PoolManager()

LOGLEVEL = os.environ.get('LOGLEVEL', logging.INFO)
logger = logging.getLogger()
logger.setLevel(LOGLEVEL)

helper = CfnResource(json_logging=False, log_level="INFO", boto_level="CRITICAL", sleep_on_delete=15)


def lambda_handler(event, context):
    logger.info("move.lambda_handler called.")
    logger.info(json.dumps(event))
    try:
        if "RequestType" in event: helper(event, context)
    except Exception as e:
        helper.init_failure(e)


@helper.create
@helper.update
def create(event, context):
    logger.info("provisionLWConfig.create called.")
    logger.info(json.dumps(event))

    aws_account_id = context.invoked_function_arn.split(":")[4]
    lacework_url = os.environ['lacework_url']
    lacework_account_name = get_account_from_url(lacework_url)
    access_key_id = os.environ['access_key_id']
    secret_key = os.environ['secret_key']
    lacework_account = os.environ['lacework_account']
    send_honeycomb_event(HONEY_API_KEY, DATASET, BUILD_VERSION, lacework_account_name, "add started",
                         "", get_lacework_environment_variables())

    logger.info(
        "Lacework URL: {}, Lacework account: {}".format(
            lacework_url,
            lacework_account_name))

    try:
        lw_account_name = get_account_from_url(lacework_url)
        external_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=7))
        role_arn = create_lw_config_cross_account_access_role(lw_account_name, external_id)
        if role_arn is not None:
            access_token = setup_initial_access_token(lacework_url, access_key_id, secret_key)
            if not add_lw_cloud_account_for_cfg(CONFIG_NAME_PREFIX + aws_account_id, lacework_url, lacework_account,
                                                access_token,
                                                external_id,
                                                role_arn, aws_account_id):
                send_cfn_fail(event, context, "add_lw_cloud_account_for_cfg failed {}.".format(aws_account_id))

    except Exception as provision_exception:
        send_cfn_fail(event, context, "Provision failed {}.".format(provision_exception))
        return None

    send_honeycomb_event(HONEY_API_KEY, DATASET, BUILD_VERSION, lacework_account_name, "provision completed", "")
    send_cfn_success(event, context)
    return None


@helper.delete
def delete(event, context):
    logger.info("provisionLWConfig.delete called.")
    lacework_url = os.environ['lacework_url']
    lacework_account_name = get_account_from_url(lacework_url)
    aws_account_id = context.invoked_function_arn.split(":")[4]

    send_honeycomb_event(HONEY_API_KEY, DATASET, BUILD_VERSION, lacework_account_name, "delete started", "")
    delete_lw_config_cross_account_access_role(lacework_account_name,aws_account_id)
    send_honeycomb_event(HONEY_API_KEY, DATASET, BUILD_VERSION, lacework_account_name, "delete completed", "")
    send_cfn_success(event, context)
    return None
