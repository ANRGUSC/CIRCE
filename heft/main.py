import heft_dup
import cpop

"""
This module is a test module. You should take three steps:
1. Instantiating a HEFT/CPOP objects.
2. Calling run() method.
3. Calling display_result() method.
"""
heft_scheduler = heft_dup.HEFT('input_0.tgff')
heft_scheduler.run()
heft_scheduler.output_file()
heft_scheduler.display_result()


"""
cpop_scheduler = cpop.CPOP('../dag/input_0.tgff')
cpop_scheduler.run()
cpop_scheduler.display_result()
"""
