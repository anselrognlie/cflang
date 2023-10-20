from cflang.io.file_binary_reader import FileBinaryReader
from cflang.cfsm.stack_machine import StackMachine

r = FileBinaryReader('sample_data/cfsm/bin/sum_to_5')
sm = StackMachine(r)
exit_code = sm.run()

print(exit_code)
