
import group_class
import sys
import json

of = open("45-35-20.json", "w")
of.write(json.dumps(group_class.groups_to_file(str(sys.argv[1]) + ".csv", None, None), indent=2))
of.close()



