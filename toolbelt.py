"""

    Used for information gather about objects to build reports

"""
from pyVmomi import vmodl, vim
from time import strftime, localtime


class Report:
    # Class to generate useful information about the environment
    def __init__(self, service_manager, view_manager):
        self.content = service_manager.content
        self.view_manager = view_manager
        self.hosts = {}
        self.report_heading = """<html>
        <head>
        <title>VEMS Report</title>
        </head>
        <body>
        <center><H2>VEMS Report</h2></center>      
        <hr>
        """
        self.report_body = """"""
        self.report_end = """</body></html>"""

    def create_report(self):
        print("GENERATING REPORTS")
        print("Finding disconnected hosts...")
        self.report_hosts_disconnected()
        print("Finding hosts not resonding...")
        self.report_hosts_not_responding()

        report = self.report_heading + str(self.report_body) + self.report_end
        report_time = localtime()
        report_time = strftime("%Y_%m_%d_%I:%M%p")
        report_file = open("generated_reports/Report_" + report_time + ".html", "w")
        report_file.write(report)
        report_file.close()

    def tool_get_host_connection_states(self):
        allhosts = self.view_manager.get_all_obj(vim.HostSystem)
        host_connection_states = {}
        if len(allhosts) > 0:
            for host in allhosts:
                host_connection_states[host.name] = host.runtime.connectionState
            return host_connection_states
        else:
            return f"Could not get host connection states"

    def tool_gather_host_information(self):
        allhosts = self.view_manager.get_all_obj(vim.HostSystem)
        for host in allhosts:
            self.hosts[host.name] = Host(self.content, self.view_manager, host)
        pass

    def tool_host_with_connection_state(self, state_check):
        host_states = self.tool_get_host_connection_states()
        hosts_with_state = []
        for host, state in host_states.items():
            if state == state_check:
                hosts_with_state.append(host)
        return hosts_with_state

    def report_hosts_disconnected(self):
        # Add hosts with a disconnected state to the report
        self.report_body += r"<br><h2>HOSTS - DISCONNECTED</h2><br>"
        hosts_disconnected = self.tool_host_with_connection_state("disconnected")
        if len(hosts_disconnected) > 0:
            for host_disconnected in hosts_disconnected:
                self.report_body += host_disconnected+"<br>"
        else:
            self.report_body += r"<i>No hosts disconnected</i>"

    def report_hosts_not_responding(self):
        # Add hosts with a not responding state to the report
        self.report_body += r"<br><h2>HOSTS - NOT RESPONDING</h2><br>"
        hosts_not_responding = self.tool_host_with_connection_state("notResponding")
        if len(hosts_not_responding) > 0:
            for host_not_responding in hosts_not_responding:
                self.report_body += host_not_responding+"<br>"
        else:
            self.report_body += r"<i>No hosts not responding</i>"


class Host:
    def __init__(self, content, view_manager, host_object):
        self.content = content
        self.view_manager = view_manager
        self.host_object = host_object
        self.name = host_object.name
        self.connection_state = host_object.runtime.connectionState
        self.certificate_expiration_date = host_object.configManager.certificateManager.certificateInfo.notAfter


