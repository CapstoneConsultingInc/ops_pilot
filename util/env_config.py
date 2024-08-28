
import os

# The workspace root points to the root of the directory structure where the ops automation exists
# that will be used to carry out the requested tasks.
workspace_root= os.environ.get('OPS_WORKSPACE_ROOT', '/home/stwall/dev')

# The bastion host is where the ops-core scripts are run. ops_pilot executes the scripts on
# the bastion host.
bastion_host = os.environ.get('OPS_BASTION_HOST', 'localhost')
