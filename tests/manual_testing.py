"""Misc lines of code to be used for manual testing of this plugin.
"""
# Test single line execution.
FBModelCube('TestSingle')

# Test multiple line execution.
for i in range(10):
    FBModelCube('TestMultiple{}'.format(i))
