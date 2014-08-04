pyxdevkit: xdevkit for python
============================

Why?
------
I am a linux and python user by choice and debugging on the xbox is essentially the opposite. One is bascially confined to windows and C# or C++. This project allows you to debug across all platforms that python is supported, and is in python, so it is much more usable for me. Also why not?

Note
--------
This is early in development and I wouldn't use it for anything real right now. I will remove this when it is more stable.

Installation
-----------

```bash
$ git clone https://github.com/Fire30/pyxdevkit.git
$ cd pyxdevkit
$ python setup.py install
```

Hopefully I will put it on pypi someday

Features
-------
 - Get Memory
 - Set Memory
 - Get Console Name
 - Reboot Console
 - Connect as Debugger
 - Set Breakpoints
 - Start Execution After Break
 - Execute Function on Notification
 - Get Registers

Hopefully this will slowly increase over time.

Examples
--------

### Initialization

```python
>>> import pyxdevkit

>>> con = pyxdevkit.Console('192.168.1.69')
```

### Getting Name

```python
>>> con.get_name()
'Jtag'
```

### Getting Memory
```python
>>> addr = 0x82000000
>>> length = 8
>>> mem = con.get_memory(addr,length)
>>> print mem.encode('hex')
4d5a900003000000
```

### Setting Memory
```python
>>> addr = 0x82000000
>>> value = 'FFFFFFFFFFFFFFFF'
>>> con.set_memory(addr,length)
>>> mem = con.get_memory(addr,len(value))
>>> print mem.encode('hex')
ffffffffffffffff
```
### Rebooting Console
```python
>>> con.reboot()
```

### Connecting As Debugger
```python
>>> con.connect_as_debugger()
>>> # You can now use the other debugger functions such as breakpoints
...
>>> # Accessed with con.debugger
```

### Setting Breakpoints
```python
>>> # Note that this starts a new thread that stops when the main thread exits
...
>>> con.debuger.set_breakpoint(0x8234A68)
```

### Executing Function on Break
```python
This also shows you how to get registers and restart execution

>>> def on_break(event_type,event_info):
...		# the event_type variable is a string with the type of event
...		# The most common is break
...     if event_type == 'break':
...		# get_registers returns a dict of all registers and their values
...             regs = event_info.thread.get_registers()
...				# Gpr5 is the same as r5
...             print regs['Gpr5']
...		# Shows how to continue when execution is stopped
...     if event_info.is_stopped:
...             event_info.thread.t_continue()
...             con.debugger.go()
...
>>> con.debugger.on_std_notify_func = on_break
```

Dependencies
--------
None as of right now!