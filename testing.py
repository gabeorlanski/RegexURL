
import functions
import sys
import json

of = open("clusters.json", "w")
of.write(json.dumps(functions.groupstofile(str(sys.argv[1]) + ".csv", None,None), indent=2))
of.close()



