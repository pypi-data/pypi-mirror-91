from FreeTAKServer.controllers.configuration.MainConfig import MainConfig

class FederationServerServiceVariables:
    def __init__(self):
        # TODO: change to default ''
        self.FederationServerServiceStatus = ''
        self.FederationServerServicePort = MainConfig.FederationPort
        self.FederationServerServiceIP = "0.0.0.0"