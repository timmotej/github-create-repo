#!/usr/bin/env python3

import subprocess as sp
import re
import sys
import os


class Admin:
    def __init__(self, quiet=False, show_output=True, log_file="/var/log/pyadmin.log"):
        self.process = None
        self.quiet = quiet
        self.show_output = show_output
        self.log_file = log_file

    def log(self, output):
        uid = os.getuid()
        if not os.path.isfile(self.log_file):
            os.system(f"sudo touch {self.log_file}; sudo chown {uid} {self.log_file}")
        if os.stat(self.log_file).st_uid != uid:
            os.system(f"sudo chown {uid} {self.log_file}")
        with open(self.log_file, "a") as f:
            f.write(output)

    def split_command(self, cmd):
        """
        split string to list for executing in self.start_process()
        return list
        """
        if isinstance(cmd, str):
            cmd = cmd.replace('"', "'")
            if "'" in cmd:
                cmd_list = [
                    c.split(" ") if i % 2 == 0 else [f"{c}"]
                    for i, c in zip(range(len(cmd.split("'"))), cmd.split("'"))
                ]
                cmd = [c for l in cmd_list for c in l]
            else:
                cmd = cmd.split()
        elif isinstance(cmd, (list, tuple)):
            cmd = list(cmd)
        else:
            raise RuntimeError("Not right type of cmd")
        return cmd

    def start_process(self, cmd, stdin=False, shell=False):
        """
        starts the process
        return dict {proc:cmd}
        """
        if not shell:
            cmd = self.split_command(cmd)
        if not self.quiet:
            print(" ".join(cmd) if not isinstance(cmd, str) else cmd)
        if stdin:
            proc = sp.Popen(
                cmd, stdout=sp.PIPE, stderr=sp.PIPE, stdin=stdin, shell=shell
            )
        else:
            proc = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, shell=shell)
        self.log(f"Started:\n{' '.join(cmd)}")
        return {proc: cmd}

    def get_output_proc(self, procs):
        """
        returns output from {proc: cmd} and print to console, if self.show_output=True (default)
        or won't print if self.show_output=False
        """
        dict_ret = {}
        for proc, cmd in procs.items():
            ret = "\n".join([i.decode("utf-8") for i in proc.communicate()])
            self.log(ret)
            if self.show_output:
                print(ret)
            if proc.returncode != 0 and not self.quiet:
                cont = input(
                    f"There was an error executing the command : {' '.join(cmd)}. Should we continue with executing? [Y/n]:\n"
                )
                if cont.lower() == "n":
                    raise RuntimeError("You have chosen to exit script...")
                else:
                    print("You have chosen to continue")
            dict_ret.update({" ".join(cmd): [ret, proc.returncode]})
        return dict_ret

    def execute_pipe(self, cmd, shell=False):
        if shell:
            if isinstance(cmd, (list, tuple)):
                cmd = " ".join(cmd)
            proc = self.start_process(cmd, stdin=False, shell=True)
            return self.get_output_proc(proc)
        if isinstance(cmd, str):
            commands = cmd.split("|")
            cmds = [self.split_command(c) for c in commands]
        elif isinstance(cmd, (list, tuple)):
            indices = [k for k in range(len(cmd)) if cmd[k] == "|"] + [len(cmd)]
            cmds = [cmd[(a + 1) : b] for a, b in zip([-1] + indices[:-1], indices)]
        for c in cmds:
            if c == cmds[0]:
                proc = self.start_process(c)
            else:
                pr = [p for p in proc][0]
                proc = self.start_process(c, stdin=pr.stdout)
            if c == cmds[-1]:
                return self.get_output_proc(proc)

    def execute(self, cmd, shell=False):
        procs = self.start_process(cmd, shell=shell)
        return self.get_output_proc(procs)
