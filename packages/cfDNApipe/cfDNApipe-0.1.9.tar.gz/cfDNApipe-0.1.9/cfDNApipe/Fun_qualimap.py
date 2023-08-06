# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 18:27:32 2019
Modify on Sun Apr 26 11:27:32 2020
@author: Shuying He
"""

from .StepBase import StepBase
from .cfDNA_utils import commonError
import os
from .Configure import Configure


__metaclass__ = type


class qualimap(StepBase):
    def __init__(
        self,
        bamInput=None,
        outputdir=None,
        memSize="8G",
        threads=1,
        other_params=None,
        stepNum=None,
        upstream=None,
        verbose=True,
        **kwargs
    ):
        """
        This function is for bam file statistics, generating the coverage, depth, map ratio in each chromosome, some figures and so on.
        Note: this function is calling qualimap, please install qualimap before using.

        qualimap(bamInput=None, outputdir=None, memSize="8G",
            stepNum=None, upstream=None, threads=1,
            verbose=False, other_params=None, **kwargs)

        {P}arameters:
            bamInput: list, Input bam files.
            outputdir: str, output result folder, None means the same folder as input files.
            memSize: str, mem size for java, default is 8G.
            stepNum: int or str, step flag for folder name.
            upstream: upstream output results, used for pipeline. This parameter can be True, which means a new pipeline start.
            other_params: dict or str, other_params for qualimap, eg: for panel data, you can set {"--gff":'xx.bed'} for target region analysis.
            threads: int, how many threads used?
            verbose: bool, True means print all stdout, but will be slow; False means black stdout verbose, much faster.
        """

        super(qualimap, self).__init__(stepNum, upstream)
        if (upstream is None) or (upstream is True):
            self.setInput("bamInput", bamInput)
        else:
            Configure.configureCheck()
            upstream.checkFilePath()

            if upstream.__class__.__name__ in [
                "bamsort",
                "rmduplicate",
                "addRG",
                "BQSR",
            ]:
                self.setInput("bamInput", upstream.getOutput("bamOutput"))
            else:
                raise commonError("Parameter upstream must from bamsort, rmduplicate, addRG or BQSR.")
        self.checkInputFilePath()

        if upstream is None:
            if outputdir is None:
                self.setOutput(
                    "outputdir",
                    os.path.dirname(os.path.abspath(self.getInput("bamInput")[0])),
                )
            else:
                self.setOutput("outputdir", outputdir)
            self.setParam("threads", threads)
        else:
            self.setOutput("outputdir", self.getStepFolderPath())
            self.setParam("threads", Configure.getThreads())

        self.setParam(
            "prefix",
            [self.getMaxFileNamePrefixV2(x) for x in self.getInput("bamInput")],
        )

        self.setOutput(
            "outdir",
            [os.path.join(self.getOutput("outputdir"), x) for x in self.getParam("prefix")],
        )

        self.setOutput(
            "pdfOutput",
            [os.path.join(x, "report.pdf") for x in self.getOutput("outdir")],
        )

        self.setOutput(
            "htmlOutput",
            [os.path.join(x, "qualimapReport.html") for x in self.getOutput("outdir")],
        )

        self.setParam("memSize", memSize)

        if other_params is None:
            self.setParam("other_params", "")
        else:
            self.setParam("other_params", other_params)

        multi_run_len = len(self.getInput("bamInput"))

        all_cmd = []

        for i in range(multi_run_len):
            tmp_cmd = self.cmdCreate(
                [
                    "qualimap",
                    "bamqc",
                    "--java-mem-size=" + self.getParam("memSize"),
                    "-nt",
                    self.getParam("threads"),
                    "-bam",
                    self.getInput("bamInput")[i],
                    "-outdir",
                    self.getOutput("outdir")[i],
                    "-outformat",
                    "PDF:HTML",
                    self.getParam("other_params"),
                ]
            )
            all_cmd.append(tmp_cmd)

        finishFlag = self.stepInit(upstream)

        if not finishFlag:
            if verbose:
                self.run(all_cmd)
            else:
                self.multiRun(args=all_cmd, func=None, nCore=1)

        self.stepInfoRec(cmds=all_cmd, finishFlag=finishFlag)
