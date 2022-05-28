import json
import sys

from virtual_machine import VirtualMachine

obj = None
with open(sys.argv[1], encoding='utf-8') as file:
    read_data = file.read()
    obj = json.loads(read_data)

vm = VirtualMachine()
vm.execute(obj)
