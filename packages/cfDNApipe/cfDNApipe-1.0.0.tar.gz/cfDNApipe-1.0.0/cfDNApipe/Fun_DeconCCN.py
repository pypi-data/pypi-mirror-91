# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 15:17:42 2020

@author: Jiaqi Huang
"""

from .StepBase import StepBase
from .cfDNA_utils import commonError, DeconCCN, preDeconCCN, DeconCCNplot
from .Configure import Configure
import os
import pandas as pd

__metaclass__ = type


class runDeconCCN(StepBase):
    def __init__(
        self,
        mixInput=None,
        refInput=None,
        outputdir=None,
        threads=1,
        stepNum=None,
        upstream=None,
        **kwargs
    ):
        """
        This function is used for methylation signal deconvolution.

        runDeconCCN(mixInput=None, refInput=None, outputdir=None, threads=1, stepNum=None, upstream=None,)
        {P}arameters:
            mixInput: Input samples need to be deconvoluted.
            refInput: reference files. Default from https://www.pnas.org/content/112/40/E5503.
            outputdir: str, output result folder, None means the same folder as input files.
            threads: int, how many thread to use. In this function, this number is set to 1.
            upstream: upstream output results, used for pipeline, must from calculate_methyl.
            stepNum: int or str, step flag for folder name.
        """
        super(runDeconCCN, self).__init__(stepNum, upstream)

        # set input
        if (upstream is None) or (upstream is True):
            self.setInput("mixInput", mixInput)
            if refInput is None:
                self.setInput("refInput", Configure.getConfig("PlasmaMarker"))
            else:
                self.setInput("refInput", refInput)
        else:
            Configure.configureCheck()
            upstream.checkFilePath()
            if upstream.__class__.__name__ == "calculate_methyl":
                self.setInput("mixInput", upstream.getOutput("txtOutput"))
            else:
                raise commonError("Parameter upstream must from calculate_methyl.")

            if refInput is None:
                self.setInput("refInput", Configure.getConfig("PlasmaMarker"))
            else:
                self.setInput("refInput", refInput)

        self.checkInputFilePath()

        # set outputdir
        if upstream is None:
            if outputdir is None:
                self.setOutput(
                    "outputdir",
                    os.path.dirname(os.path.abspath(self.getInput("mixInput"))),
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

        self.setOutput(
            "txtOutput", os.path.join(self.getOutput("outputdir"), "result.txt")
        )
        self.setOutput(
            "plotOutput", os.path.join(self.getOutput("outputdir"), "bar_chart.png")
        )

        finishFlag = self.stepInit(upstream)

        if not finishFlag:
            mix, ref, celltypes = preDeconCCN(
                self.getInput("mixInput"), self.getInput("refInput")
            )
            result = DeconCCN(ref, mix)
            res_df = pd.DataFrame(
                result,
                index=celltypes,
                columns=[
                    self.getMaxFileNamePrefixV2(x).split(".")[0]
                    for x in self.getInput("mixInput")
                ],
            )
            res_df.to_csv(self.getOutput("txtOutput"), sep="\t", index=True)
            DeconCCNplot(res_df, self.getOutput("plotOutput"))

        self.stepInfoRec(cmds=[], finishFlag=finishFlag)
