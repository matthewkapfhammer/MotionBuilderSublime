# MotionBuilderSublime
### A Sublime Text 2/3 plugin based on MayaSublime by Justin Isreal (https://github.com/justinfx/MayaSublime).

Send selected Python code snippets or whole files from SublimeText to MotionBuilder via telnet.

----------

### Installation

**Easy Install**

You can install this plugin directly from Sublime Package Control:

https://packagecontrol.io/packages/MotionBuilderSublime

**Manual install**

1. clone this repo into the `SublimeText2/3 -> Preference -> Browse Packages` directory:  
`git clone git://github.com/matthewkapfhammer/MotionBuilderSublime.git`

2. Edit the `MotionBuilderSublime.sublime-settings` file, setting the port to match the commandPorts you have configured in MotionBuilder.

3. Optionally edit the keymap file to change the default hotkey from `ctrl+return` to something else.

Note - Ideally you would make your custom changes to the user settings and not the default settings, so that they do not get overwritten when the plugin is updated.

### Usage

To send a snippet, simply select some code in a mel or python script, and hit `ctrl+return`, or right click and choose "Send To MotionBuilder".
A socket conncetion will be made to a running MotionBuilder instance on the configured port matching mel or python, and the code will be 
run in MotionBuilder's environment.

As an example, if you want to open a connection on port 4242 for Python (the default port in the config), you can do the following:

```python
# PLACEHOLDER
```
