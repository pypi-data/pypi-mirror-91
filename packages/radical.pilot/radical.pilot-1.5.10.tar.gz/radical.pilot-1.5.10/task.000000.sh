#!/bin/sh


# Environment variables
export RADICAL_BASE="<Mock id='140375126306288'>"
export RP_SESSION_ID="sid0"
export RP_PILOT_ID="pid0"
export RP_AGENT_ID="aid0"
export RP_SPAWNER_ID="<Mock id='140375126306192'>"
export RP_TASK_ID="task.000000"
export RP_TASK_NAME="None"
export RP_GTOD="<Mock id='140375126306240'>"
export RP_TMP="<Mock id='140375126306480'>"
export RP_PILOT_SANDBOX="<Mock id='140375126306288'>"
export RP_PILOT_STAGING="<Mock id='140375126306288'>/staging_area"
export RP_PROF=".//task.000000.prof"

prof(){
    if test -z "$RP_PROF"
    then
        return
    fi
    event=$1
    msg=$2
    now=$($RP_GTOD)
    echo "$now,$event,task_script,MainThread,$RP_TASK_ID,AGENT_EXECUTING,$msg" >> $RP_PROF
}
export OMP_NUM_THREADS="0"

prof cu_start

# Change to task sandbox
cd ./

# Pre-exec commands
prof cu_pre_start
n ||  (echo "pre_exec failed"; false) || exit
u ||  (echo "pre_exec failed"; false) || exit
l ||  (echo "pre_exec failed"; false) || exit
l ||  (echo "pre_exec failed"; false) || exit
prof cu_pre_stop

# The command to run
prof cu_exec_start
mpiexec echo hello
RETVAL=$?
prof cu_exec_stop

# Post-exec commands
prof cu_post_start
n ||  (echo "post_exec failed"; false) || exit
u ||  (echo "post_exec failed"; false) || exit
l ||  (echo "post_exec failed"; false) || exit
l ||  (echo "post_exec failed"; false) || exit

prof cu_post_stop "$ret=RETVAL"

# Exit the script with the return code from the command
prof cu_stop
exit $RETVAL
