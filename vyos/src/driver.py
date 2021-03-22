#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from cloudshell.shell.core.driver_context import InitCommandContext, ResourceCommandContext, AutoLoadDetails
from cloudshell.shell.core.driver_utils import GlobalLock
from cloudshell.shell.core.interfaces.save_restore import OrchestrationSaveResult
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.flows.connectivity.models.connectivity_result import ConnectivitySuccessResponse
from cloudshell.shell.flows.connectivity.simple_flow import apply_connectivity_changes
from cloudshell.shell.standards.networking.driver_interface import NetworkingResourceDriverInterface
from cloudshell.shell.core.session.logging_session import LoggingSessionContext
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext
from cloudshell.shell.core.driver_context import AutoLoadCommandContext
#from cloudshell.snmp.quali_snmp import QualiSnmp, QualiMibTable
from cloudshell.cli.session.ssh_session import SSHSession
from cloudshell.cli.service.cli import CLI
from cloudshell.cli.service.command_mode import CommandMode

from data_model import *  # run 'shellfoundry generate' to generate data model classes
from cloudshell.snmp.cloudshell_snmp import Snmp
from cloudshell.snmp.core.domain.snmp_oid import SnmpMibObject
from cloudshell.snmp.snmp_parameters import SNMPWriteParameters


class VyosDriver(ResourceDriverInterface, NetworkingResourceDriverInterface, GlobalLock):

    """
    ResourceDriverInterface - describe all functionality/methods which should be implemented
                              for base abstract resource
    NetworkingResourceDriverInterface - describe all functionality/methods which should be implemented
                                        for network resource based on Networking Standard

    In case of building driver based on Quali Standards and using Quali packages you can simplify your work
    by importing functionality from cloudshell-shell-standards package:
    from cloudshell.shell.standards.networking.resource_config import NetworkingResourceConfig

    and organize working with network resource configuration as with object:
    resource_config = NetworkingResourceConfig.from_context(shell_name=self.SHELL_NAME,
                                                            supported_os=self.SUPPORTED_OS,
                                                            context=context)


    """
    def __init__(self):
        """ Constructor must be without arguments, it is created with reflection at run time """

        pass

    def initialize(self, context):
        """
        Initialize the driver session, this function is called everytime a new instance of the driver is created
        This is a good place to load and cache the driver configuration, initiate sessions etc.
        :param InitCommandContext context: the context the command runs on
        """
        pass

    # <editor-fold desc="Networking Standard Commands">
    def restore(self, context, cancellation_context, path, configuration_type, restore_method, vrf_management_name):
        """
        Restores a configuration file
        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        :param str path: The path to the configuration file, including the configuration file name.
        :param str restore_method: Determines whether the restore should append or override the current configuration.
        :param str configuration_type: Specify whether the file should update the startup or running config.
        :param str vrf_management_name: Optional. Virtual routing and Forwarding management name
        """
        pass

    def save(self, context, cancellation_context, folder_path, configuration_type, vrf_management_name):
        """
        Creates a configuration file and saves it to the provided destination
        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        :param str configuration_type: Specify whether the file should update the startup or running config. Value can one
        :param str folder_path: The path to the folder in which the configuration file will be saved.
        :param str vrf_management_name: Optional. Virtual routing and Forwarding management name
        :return The configuration file name.
        :rtype: str
        """
        pass

    def load_firmware(self, context, cancellation_context, path, vrf_management_name):
        """
        Upload and updates firmware on the resource
        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param str path: path to tftp server where firmware file is stored
        :param str vrf_management_name: Optional. Virtual routing and Forwarding management name
        """
        pass

    def run_custom_command(self, context, cancellation_context, custom_command):
        """
        Executes a custom command on the device
        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        :param str custom_command: The command to run. Note that commands that require a response are not supported.
        :return: the command result text
        :rtype: str
        """
        pass

    def run_custom_config_command(self, context, cancellation_context, custom_command):
        """
        Executes a custom command on the device in configuration mode
        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        :param str custom_command: The command to run. Note that commands that require a response are not supported.
        :return: the command result text
        :rtype: str
        """
        pass

    def shutdown(self, context, cancellation_context):
        """
        Sends a graceful shutdown to the device
        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        """
        pass

    # </editor-fold>

    # <editor-fold desc="Orchestration Save and Restore Standard">
    def orchestration_save(self, context, cancellation_context, mode, custom_params):
        """
        Saves the Shell state and returns a description of the saved artifacts and information
        This command is intended for API use only by sandbox orchestration scripts to implement
        a save and restore workflow
        :param ResourceCommandContext context: the context object containing resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        :param str mode: Snapshot save mode, can be one of two values 'shallow' (default) or 'deep'
        :param str custom_params: Set of custom parameters for the save operation
        :return: SavedResults serialized as JSON
        :rtype: OrchestrationSaveResult
        """

        # See below an example implementation, here we use jsonpickle for serialization,
        # to use this sample, you'll need to add jsonpickle to your requirements.txt file
        # The JSON schema is defined at: https://github.com/QualiSystems/sandbox_orchestration_standard/blob/master/save%20%26%20restore/saved_artifact_info.schema.json
        # You can find more information and examples examples in the spec document at https://github.com/QualiSystems/sandbox_orchestration_standard/blob/master/save%20%26%20restore/save%20%26%20restore%20standard.md

        '''
        # By convention, all dates should be UTC
        created_date = datetime.datetime.utcnow()

        # This can be any unique identifier which can later be used to retrieve the artifact
        # such as filepath etc.

        # By convention, all dates should be UTC
        created_date = datetime.datetime.utcnow()

        # This can be any unique identifier which can later be used to retrieve the artifact
        # such as filepath etc.
        identifier = created_date.strftime('%y_%m_%d %H_%M_%S_%f')

        orchestration_saved_artifact = OrchestrationSavedArtifact('REPLACE_WITH_ARTIFACT_TYPE', identifier)

        saved_artifacts_info = OrchestrationSavedArtifactInfo(
            resource_name="some_resource",
            created_date=created_date,
            restore_rules=OrchestrationRestoreRules(requires_same_resource=True),
            saved_artifact=orchestration_saved_artifact)

        return OrchestrationSaveResult(saved_artifacts_info)
        '''
        pass

    def orchestration_restore(self, context, cancellation_context, saved_artifact_info, custom_params):
        """
        Restores a saved artifact previously saved by this Shell driver using the orchestration_save function
        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        :param str saved_artifact_info: A JSON string representing the state to restore including saved artifacts and info
        :param str custom_params: Set of custom parameters for the restore operation
        :return: None
        """
        '''
        # The saved_details JSON will be defined according to the JSON Schema and is the same object returned via the
        # orchestration save function.
        # Example input:
        # {
        #     "saved_artifact": {
        #      "artifact_type": "REPLACE_WITH_ARTIFACT_TYPE",
        #      "identifier": "16_08_09 11_21_35_657000"
        #     },
        #     "resource_name": "some_resource",
        #     "restore_rules": {
        #      "requires_same_resource": true
        #     },
        #     "created_date": "2016-08-09T11:21:35.657000"
        #    }

        # The example code below just parses and prints the saved artifact identifier
        saved_details_object = json.loads(saved_details)
        return saved_details_object[u'saved_artifact'][u'identifier']
        '''
        pass

    # </editor-fold>

    # <editor-fold desc="Connectivity Provider Interface (Optional)">

    # The ApplyConnectivityChanges function is intended to be used for using switches as connectivity providers
    # for other devices. If the Switch shell is intended to be used a DUT only there is no need to implement it

    def ApplyConnectivityChanges(self, context, request):
        """
        Configures VLANs on multiple ports or port-channels
        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param str request: A JSON object with the list of requested connectivity changes
        :return: a json object with the list of connectivity changes which were carried out by the switch
        :rtype: str
        """

        return apply_connectivity_changes(request=request,
                                          add_vlan_action=lambda x: ConnectivitySuccessResponse(x,'Success'),
                                          remove_vlan_action=lambda x: ConnectivitySuccessResponse(x,'Success'))

    # </editor-fold>

    # <editor-fold desc="Discovery">

    def get_inventory(self, context):
        """
        Discovers the resource structure and attributes.
        :param AutoLoadCommandContext context: the context the command runs on
        :return Attribute and sub-resource information for the Shell resource you can return an AutoLoadDetails object
        :rtype: AutoLoadDetails
        """

        # See below some example code demonstrating how to return the resource structure and attributes
        # In real life, this code will be preceded by SNMP/other calls to the resource details and will not be static
        # run 'shellfoundry generate' in order to create classes that represent your data model

        # logger = LoggingSessionContext.get_logger_for_context(context)
        with LoggingSessionContext(context) as logger:
            logger.info("started")
            api = CloudShellSessionContext(context).get_api()
            # api = CloudShellAPISession(host=context.connectivity.server_address,
            #                            token_id=context.connectivity.admin_auth_token,
            #                            domain="Global")

            snmp_community_enc = context.resource.attributes['Vyos.SNMP Read Community']
            logger.info(snmp_community_enc)
            snmp_community_dec = api.DecryptPassword(snmp_community_enc).Value
            logger.info(snmp_community_dec)
            try:
                snmp_params = SNMPWriteParameters(context.resource.address, snmp_community_dec, "v2")
                snmp_handler = Snmp()

                with snmp_handler.get_snmp_service(snmp_parameters=snmp_params, logger=logger) as snmp_service:
                    # response = snmp_service.get_table(SnmpMibObject('IF-MIB', 'ifTable'))
                    # Retruns empty SnmpResponse in case get command failed to retrieve data
                    resource = Vyos.create_from_context(context)
                    # resource.vendor = 'Vyos'
                    # resource.model = 'Vyos'

                    chassis1 = GenericChassis('Chassis 1')
                    chassis1.serial_number = ''
                    resource.add_sub_resource('1', chassis1)
                    logger.info(chassis1.name)

                    response = snmp_service.get_table(SnmpMibObject('IF-MIB', 'ifXTable'))
                    port_idx = 0
                    for interface in response.values():
                        if 'ifName' in interface:
                            port_idx += 1
                            port_name = interface['ifName'].safe_value
                            port = GenericPort(port_name)
                            # port.mac_address = ''
                            # port.ipv4_address = ''
                            chassis1.add_sub_resource(str(port_idx), port)
                            logger.info(port_name)
            except Exception as e:
                logger.error(str(e))
                raise

            result = resource.create_autoload_details()
            logger.info('return object: {} {}'.format(str(result), 'is None' if result is None else 'is not None'))
            return result

    # </editor-fold>

    # <editor-fold desc="Health Check">

    def health_check(self,cancellation_context):
        """
        Checks if the device is up and connectable
        :return: str: Success or fail message
        """
        pass

    def show_interfaces(self, context):
        """
        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :return: response
        :rtype: str
        """
        logger = LoggingSessionContext.get_logger_with_thread_id(context)
        api = CloudShellSessionContext(context).get_api()
        host = context.resource.address
        username = context.resource.attributes['Vyos.User']
        password = api.DecryptPassword(context.resource.attributes['Vyos.Password']).Value
        logger.info('{} : {} , {}'.format(host, username, password))
        session = SSHSession(host=host, username=username, password=password)
        mode = CommandMode(r'.*$')
        cli = CLI()
        with cli.get_session([session], mode) as cli_service:
           out = cli_service.send_command('show interfaces')
           return out


    def cleanup(self):
        """
        Destroy the driver session, this function is called everytime a driver instance is destroyed
        This is a good place to close any open sessions, finish writing to log files
        """
        pass

if __name__ == "__main__":
    from unittest import mock
    from cloudshell.shell.core.driver_context import CancellationContext
    from cloudshell.api.cloudshell_api import CloudShellAPISession
    server = "localhost"
    username = "admin"
    password = "admin"
    resource_name = "vyos-dev4"
    address = "192.168.51.126"
    model = "Vyos"
    api = CloudShellAPISession(server, username, password, "Global")
    enc_password = api.GetAttributeValue(resource_name, "{}.Password".format(model)).Value
    # api_token = api.token_id
    # shell_name = "Vyos"

    cancellation_context = mock.create_autospec(CancellationContext)
    context = mock.create_autospec(AutoLoadCommandContext)
    context.resource = mock.MagicMock()
    context.reservation = mock.MagicMock()
    context.connectivity = mock.MagicMock()
    context.connectivity.serverAddress = server
    context.connectivity.server_address = server
    context.connectivity.cloudshell_api_port = "8029"
    context.connectivity.cloudshell_api_scheme = "http"
    # context.connectivity.admin_auth_token = api_token
    # context.reservation.reservation_id = "<RESERVATION_ID>"
    # context.reservation.domain="Global"
    context.resource.address = address
    context.resource.name = resource_name

    context.resource.attributes = dict()
    snmp_community = api.GetAttributeValue(resource_name, "{}.SNMP Read Community".format(model)).Value
    context.resource.attributes["{}.SNMP Read Community".format("Vyos")] = snmp_community
    context.resource.attributes["{}.Password".format("Vyos")] = enc_password
    context.resource.attributes["{}.User".format("Vyos")] = "vyos"

    driver = VyosDriver()
    driver.initialize(context)
    driver.get_inventory(context)

    print("done")