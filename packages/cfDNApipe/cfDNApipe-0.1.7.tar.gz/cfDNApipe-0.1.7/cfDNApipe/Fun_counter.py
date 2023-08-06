# -*- coding: utf-8 -*-
"""
Created on Wed Apr 8 12:51:24 2020

@author: Jiaqi Huang
"""

from .StepBase import StepBase
from .cfDNA_utils import commonError, maxCore
import os
import math
from .Configure import Configure

__metaclass__ = type


class runCounter(StepBase):
    def __init__(
        self,
        fileInput=None,
        outputdir=None,
        filetype=None,
        binlen=None,
        threads=1,
        stepNum=None,
        upstream=None,
        verbose=True,
        **kwargs
    ):
        """
        This function is used for transforming fasta files or bam files into wig files.
        Note: this function is calling gcCounter or readCounter.

        runCounter(fileInput=None, outputdir=None, filetype=None, stepNum=None, upstream=None)
        {P}arameters:
            fileInput: list, paths of input files waiting to be transformed.
            outputdir: str, output result folder, None means the same folder as input files.
            filetype: int, 0 for GC counter (which indicates fasta input), 1 for read counter (which indicates bam inputs).
            binlen: int, length of the dividing bins of the wig file.
            threads: int, how many thread to use.
            stepNum: Step number for folder name.
            upstream: Not used parameter, do not set this parameter.
            verbose: bool, True means print all stdout, but will be slow; False means black stdout verbose, much faster.
        """

        super(runCounter, self).__init__(stepNum, upstream)

        # set fileInput
        if (upstream is None) or (upstream is True):
            if filetype == 1:
                self.setInput("fileInput", fileInput)
                self.setParam("countertype", "reads")
            elif filetype == 0:
                if fileInput is None:
                    self.setInput("fileInput", [Configure.getConfig("genome.seq")])
                else:
                    self.setInput("fileInput", fileInput)
                self.setParam("countertype", "gc")
            else:
                raise commonError("Parameter filetype is invalid.")
        else:
            Configure.configureCheck()
            upstream.checkFilePath()
            if upstream.__class__.__name__ in "bamsort" or "rmduplicate":
                self.setInput("fileInput", upstream.getOutput("bamOutput"))
            else:
                raise commonError(
                    "Parameter upstream must from bamsort or rmduplicate."
                )

            self.setParam("countertype", "reads")

        self.checkInputFilePath()

        # set threads
        if upstream is None:
            self.setParam("threads", threads)
        else:
            self.setParam("threads", Configure.getThreads())

        # set outputdir
        if upstream is None:
            if outputdir is None:
                self.setOutput(
                    "outputdir",
                    os.path.dirname(os.path.abspath(self.getInput("fileInput")[0])),
                )
            else:
                self.setOutput("outputdir", outputdir)
        else:
            self.setOutput("outputdir", self.getStepFolderPath())

        # set binlen
        if binlen is not None:
            self.setParam("binlen", binlen)
        else:
            self.setParam("binlen", 100000)

        if self.getParam("countertype") == "gc":
            self.setOutput(
                "wigOutput",
                [
                    os.path.join(
                        self.getOutput("outputdir"), self.getMaxFileNamePrefixV2(x)
                    )
                    + ".gc.wig"
                    for x in self.getInput("fileInput")
                ],
            )
        elif self.getParam("countertype") == "reads":
            self.setOutput(
                "wigOutput",
                [
                    os.path.join(
                        self.getOutput("outputdir"), self.getMaxFileNamePrefixV2(x)
                    )
                    + ".read.wig"
                    for x in self.getInput("fileInput")
                ],
            )
        else:
            commonError("parameter countertype is invalid!")

        finishFlag = self.stepInit(upstream)

        multi_run_len = len(self.getInput("fileInput"))
        all_cmd = []
        for i in range(multi_run_len):
            if self.getParam("countertype") == "gc":
                if not os.path.exists(self.getOutput("wigOutput")[i]):
                    tmp_cmd = self.cmdCreate(
                        [
                            "gcCounter",
                            "-w",
                            self.getParam("binlen"),
                            self.getInput("fileInput")[i],
                            ">",
                            self.getOutput("wigOutput")[i],
                        ]
                    )
                    all_cmd.append(tmp_cmd)
            elif self.getParam("countertype") == "reads":
                if not os.path.exists(self.getOutput("wigOutput")[i]):
                    tmp_cmd = self.cmdCreate(
                        [
                            "readCounter",
                            "-w",
                            self.getParam("binlen"),
                            self.getInput("fileInput")[i],
                            ">",
                            self.getOutput("wigOutput")[i],
                        ]
                    )
                    all_cmd.append(tmp_cmd)

        if not finishFlag:
            if verbose:
                self.run(all_cmd)
            else:
                self.multiRun(
                    args=all_cmd,
                    func=None,
                    nCore=maxCore(math.ceil(self.getParam("threads") / 4)),
                )

        self.stepInfoRec(cmds=[all_cmd], finishFlag=finishFlag)
