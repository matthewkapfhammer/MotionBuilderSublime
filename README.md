# MotionBuilderSublime
### A Sublime Text 2/3 plugin.

Send selected Python code snippets or whole files from SublimeText to MotionBuilder via telnet.

----------

### Installation

**Easy Install**

You can install this plugin directly from Sublime Package Control:

https://packagecontrol.io/packages/MotionBuilderSublime

**Manual Install**

1. clone this repo into the `SublimeText2/3 -> Preference -> Browse Packages` directory:  
`git clone git://github.com/matthewkapfhammer/MotionBuilderSublime.git`

2. Edit the `MotionBuilderSublime.sublime-settings` file, setting the port to match the commandPorts you have configured in MotionBuilder.

3. Optionally edit the keymap file to change the default hotkey from `ctrl+return` to something else.

Note - Ideally you would make your custom changes to the user settings and not the default settings, so that they do not get overwritten when the plugin is updated.

### Usage

To send a snippet, simply select some code in a Python script, and hit `ctrl+alt+return`, or right click and choose "Send To MotionBuilder".
A telnet connection will be made to a running MotionBuilder instance on the configured port matching Python, and the code will be run in MotionBuilder's environment.

### Beyond The Plugin

The context manager class that sends Python command to MotionBuilder can also be used in any external application. 

See the docstring for ```MotionBuilderSublime.py``` -> ```MBPipe```

### Credits

MotionBuilderSublime is inspired by and primarily based on [MayaSublime] (https://github.com/justinfx/MayaSublime) by [Justin Israel] (https://github.com/justinfx).

Additional credit belongs to [Chris Evans] (https://github.com/chrisevans3d) for sharing how to handle a telnet connection to MotionBuilder in his blog post, [Creating Interactive MotionBuilder User Interface Tools] (http://www.chrisevans3d.com/pub_blog/creating-interactive-motionbuilder-user-interface-tools/).
