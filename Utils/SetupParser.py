"""
Provides a SetupParse class that can, well, parse a setup path_to_file

Initialize with my_parser = SetupParser(<setup_file_path>) and the options
will be stored in my_parser.settings (which is a dict)

If you want to set custom default values, you can pass them in as a dict
in the second argument of the constructor
"""

import json

# helper to parse the json into ascii instead of unicode
def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('ascii') if isinstance(x, unicode) else x 
    return dict(map(ascii_encode, pair) for pair in data.items())

class SetupParser:

	def __init__(self, path_to_file, defaults=None):
		self.settings = self.parse_setup_file(path_to_file, defaults)


	def parse_setup_file(self, path_to_file, defaults):
		file_contents = open(path_to_file).read()
		file_json = json.loads(file_contents, object_hook=ascii_encode_dict)
		if not defaults:
			return file_json

		for key in defaults:
			if key not in file_json:
				file_json[key] = defaults[key]

		# now we do the ones that depend on the other values
		file_json["his_program"] = "/c/cs323/Hwk{}/{}".format(file_json["number"], file_json["name"])
		file_json["folder_path"] = file_json["testfile_base_path"] + file_json["folder"] + "/"

		return file_json