# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 19:44:37 2019

@author: zhang
"""

from .StepBase import StepBase
from .cfDNA_utils import commonError
import os
from .Configure import Configure

__metaclass__ = type


class identifyAdapter(StepBase):
    def __init__(
        self,
        fqInput1=None,
        fqInput2=None,
        outputdir=None,
        threads=1,
        other_params=None,
        stepNum=None,
        upstream=None,
        verbose=True,
        **kwargs
    ):
        """
        This function is used for detecting adapters in paired end fastq files.
        Note: this function is calling AdapterRemoval and only works for paired end data.

        identifyAdapter(fqInput1=None, fqInput2=None, outputdir=None, threads=1, other_params=None,
                        stepNum=None, upstream=None, verbose=True)
        {P}arameters:
            fqInput1: list, fastq 1 files.
            fqInput2: list, fastq 2 files.
            outputdir: str, output result folder, None means the same folder as input files.
            threads: int, how many thread to use.
            other_params: dict, other parameters passing to command "AdapterRemoval --identify-adapters".
                          "-parameter": True means "-parameter" in command line.
                          "-parameter": 1 means "-parameter 1" in command line.
            stepNum: int or str, step flag for folder name.
            upstream: upstream output results, used for pipeline.
            verbose: bool, True means print all stdout, but will be slow; False means black stdout verbose, much faster.
        """

        super(identifyAdapter, self).__init__(stepNum, upstream)

        # set fastq input and fastq output (output actually not changed)
        if (upstream is None) or (upstream is True):
            self.setInput("fq1", fqInput1)
            self.setInput("fq2", fqInput2)
            self.setOutput("fq1", fqInput1)
            self.setOutput("fq2", fqInput2)
        else:
            Configure.configureCheck()
            upstream.checkFilePath()
            self.setInput("fq1", upstream.getOutput("fq1"))
            self.setInput("fq2", upstream.getOutput("fq2"))
            self.setOutput("fq1", upstream.getOutput("fq1"))
            self.setOutput("fq2", upstream.getOutput("fq2"))

        self.checkInputFilePath()

        # set outputdir
        if upstream is None:
            if outputdir is None:
                self.setOutput(
                    "outputdir",
                    os.path.dirname(os.path.abspath(self.getInput("fq1")[0])),
                )
            else:
                self.setOutput("outputdir", outputdir)
        else:
            self.setOutput("outputdir", self.getStepFolderPath())

        # set threads
        if upstream is None:
            self.setParam("threads", threads)
        else:
            self.setParam("threads", Configure.getThreads())

        # set other_params
        if other_params is None:
            self.setParam("other_params", "")
        else:
            self.setParam("other_params", other_params)

        if len(self.getOutput("fq1")) == len(self.getOutput("fq2")):
            multi_run_len = len(self.getOutput("fq1"))
        else:
            raise commonError("Paired end Input files are not consistent.")

        all_cmd = []

        for i in range(multi_run_len):
            tmp_fq1, tmp_fq2 = self.getInput("fq1")[i], self.getInput("fq2")[i]
            tmp_basename = self.getMaxFileNamePrefix(tmp_fq1, tmp_fq2)
            self.setOutput(
                tmp_basename + "-adapterFile",
                os.path.join(
                    self.getOutput("outputdir"), tmp_basename + "-adapters.log"
                ),
            )

            tmp_cmd = self.cmdCreate(
                [
                    "AdapterRemoval --identify-adapters",
                    "--threads",
                    self.getParam("threads"),
                    "--file1",
                    tmp_fq1,
                    "--file2",
                    tmp_fq2,
                    self.getParam("other_params"),
                    ">",
                    self.getOutput(tmp_basename + "-adapterFile"),
                ]
            )
            all_cmd.append(tmp_cmd)

        finishFlag = self.stepInit(upstream)

        if not finishFlag:
            if verbose:
                self.run(all_cmd)
            else:
                self.multiRun(args=all_cmd, func=None, nCore=1)

        self.stepInfoRec(cmds=[all_cmd], finishFlag=finishFlag)
