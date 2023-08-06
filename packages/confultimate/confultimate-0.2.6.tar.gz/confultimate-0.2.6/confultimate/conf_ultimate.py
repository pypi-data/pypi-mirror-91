"""
Main class of the confultimate module
"""

import json
from jsonmerge import merge

class ConfUltimate( ):
    """A config Manager"""
    __instance = None

    def __init__( self, json_data ):
        """Initialize"""
        self.__json_data = json_data

    @staticmethod
    def load( json_path_list ):
        """Load a config contained in a list of JSON file"""
        jsonmerged = None

        if len(json_path_list) < 1 :
            raise Exception('Any configuration file specified')

        for json_path in json_path_list:
            with open( json_path, 'r' ) as fson_fp:
                jsonmerged = merge(jsonmerged, json.load(fson_fp))
        ConfUltimate.__instance = ConfUltimate(jsonmerged)

    @staticmethod
    def get_instance( ):
        """Get ConfUltimate instance"""
        if ConfUltimate.__instance is None:
            raise Exception('ConfUltimate not initalized')
        return ConfUltimate.__instance

    @staticmethod
    def clean( ):
        """Clean the ConfUltimate instance"""
        ConfUltimate.__instance = None

    def get_config( self ):
        """
        Return config string
        """
        return self.__json_data
