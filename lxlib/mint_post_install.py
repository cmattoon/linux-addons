"""
Functions for bin/mint-post-install

"""
class Config:
    _rawData = None
    data = None

    @staticmethod
    def get(key, default=None, message=None):
        """Gets input from:
           - A stored value
           - User input
        """
        result = None

        try:
            ## First, see if we have a value.
            result = Config.data[str(key)]
            
        except KeyError:
            ## Ask the user
            result = Config.getInput(key, default, message)
            
        except TypeError:
            ## `key` is bad.
            raise
        except:
            pass
        finally:
            Config.data[str(key)] = result


    @staticmethod
    def getInput(key, default=None, message=None, empty=True):
        """
        key (string) used for default message
        default (mixed|None)
        message (string|None)
        empty (bool|False) Allow '' value?
        """
        if message is None:
            message = "Enter value for '%s'"
        
        while True:
            result = raw_input("%s >>>" % (str(message)))

            if empty or result:
                return result

    @staticmethod
    def loadDefaults(something):
        self.data = {}
        self.data = {
            'update_apt': True,
            'upgrade_apt': True,
            'install': [
                'lamp',
                'dev',
                'python'
                ]
            }

class PN:
    """Privacy/Permission Notice
    
    Prints a description of permissions the user is about to grant.
    """
    cmd = None
    user = None
    
    def show(**kwargs):
        PN.run = kwargs.get('run', None)
        PN.user = kwargs.get('user', None)
        ## Set user to 
        msg = []
        if PN.run:
            msg.append("Run: %s" % PN.run)

        if PN.user:
            msg.append("As user: %s" % PN.run)
