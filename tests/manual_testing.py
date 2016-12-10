"""Misc lines of code to be used for manual testing of this plugin.

MotionBuilderSublime's default shortcut to send code to 
MotionBuilder is `ctrl+shift+enter`.

To test sending individual lines: 
    - Select lines you want to send> `ctrl+shift+enter`
    - Check MotionBuilder to see if it executed as expected.

To test sending entire file:
    - Deselect all lines> `ctrl+shift+enter`
    - Check MotionBuilder to see if it executed as expected.
"""
# Test single line execution.
FBModelCube('TestSingle')

# Test multiple line execution.
for i in range(10):
    FBModelCube('TestMultiple{}'.format(i))
