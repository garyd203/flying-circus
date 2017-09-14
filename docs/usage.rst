Usage Patterns
==============

Disclaimer
----------
Flying Circus is still very much a work in progress. These examples form part of our interface-first
approach to development. As such, they indicate how we see the tool being used, but don't necessarily
reflect the current implementation level. :-)

Create YAML From Command line
-----------------------------

Bash:

python my_stack.py # outputs to my_stack.yaml
python my_stack.py --format=yaml # outputs to my_stack.yaml
python my_stack.py --format=json # outputs to my_stack.json


Maintain Stack From Command Line
--------------------------------

Bash:

python my_stack.py --maintain-stack # Connects to AWS with your current credentials, and blocks until the stack has been created/updated