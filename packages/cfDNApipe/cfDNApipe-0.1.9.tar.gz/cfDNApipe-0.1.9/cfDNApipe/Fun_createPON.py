# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 18:27:32 2019
Modify on Sun Apr 26 11:27:32 2020
@author: LY, Shuying He
"""

from .StepBase import StepBase
from .cfDNA_utils import commonError, maxCore
import os
from .Configure import Configure
import math

__metaclass__ = type


class createPON(StepBase):
    def __init__(
        self,
        createPONInput=None,  # db dir
        outputdir=None,
        genome=None,
        ref=None,  # str
        other_params={"--min-sample-count": 2},
        stepNum=None,
        upstream=None,
        threads=1,
        verbose=False,
        **kwargs
    ):
        """
        This function is using normal samples' mutation genomicsDB to create PON file. PON means Panel Of Normals, the output file is using for follow-up somatic filter.
        Note: This function is calling gatk CreateSomaticPanelOfNormals, please install gatk before using.

        createPON(createPONInput=None, outputdir=None,
            genome=None, ref=None, threads=1,
            stepNum=None, other_params={"--min-sample-count": 2},
            upstream=None, verbose=False, **kwargs)

        {P}arameters:
            createPONInput: db input dirname, or from dbImport.
            outputdir: str, output result folder, None means the same folder as input files.
            other_params: dict, other parameters for gatk mutect, default is {"--min-sample-count": 2},
            threads: int, how many thread to use.
            genome: str, human genome version, just support "hg19" and "hg38"
            ref: str, reference folderpath.
            stepNum: int or str, step flag for folder name.
            upstream: upstream output results, used for call snp pipeline, just can be dbimport. This parameter can be True, which means a new pipeline start.
            verbose: bool, True means print all stdout, but will be slow; False means black stdout verbose, much faster.
        """

        super(createPON, self).__init__(stepNum, upstream)
        if (upstream is None) or (upstream is True):
            # In this situation, input file and output path should be checked
            self.setInput("createPONInput", createPONInput)
        else:
            # check Configure for running pipeline
            Configure.configureCheck()
            upstream.checkFilePath()

            if upstream.__class__.__name__ == "dbimport":
                self.setInput("createPONInput", upstream.getOutput("dbimportOutput"))
            else:
                raise commonError("Parameter upstream must from dbimport.")

        self.checkInputFilePath()

        if upstream is None:
            self.setParam("ref", ref)
            self.setParam("genome", genome)
            self.setParam("threads", threads)
            if outputdir is None:
                self.setOutput("outputdir", os.path.dirname(self.getInput("createPONInput")[0]))
            else:
                self.setOutput("outputdir", outputdir)

        else:
            self.setOutput("outputdir", self.getStepFolderPath())
            self.setParam("ref", Configure.getRefDir())
            self.setParam("genome", Configure.getGenome())
            self.setParam("threads", Configure.getThreads())

        self.createPONcheck()
        self.setOutput(
            "createPONOutput",
            [
                os.path.join(self.getOutput("outputdir"), os.path.basename(x) + ".vcf.gz")
                for x in self.getInput("createPONInput")
            ],
        )

        if other_params is None:
            self.setParam("other_params", "")
        else:
            self.setParam("other_params", other_params)

        all_cmd = []
        for x in range(len(self.getInput("createPONInput"))):
            tmp_cmd = self.cmdCreate(
                [
                    "gatk",
                    "CreateSomaticPanelOfNormals",
                    "-R",
                    self.getParam("ref") + "/" + self.getParam("genome") + ".fa",
                    "-V gendb:///" + self.getInput("createPONInput")[x],
                    self.getParam("other_params"),
                    "-O",
                    self.getOutput("createPONOutput")[x],
                ]
            )
            all_cmd.append(tmp_cmd)

        finishFlag = self.stepInit(upstream)

        if not finishFlag:
            if verbose:
                self.run(all_cmd)
            else:
                self.multiRun(
                    args=all_cmd,
                    func=None,
                    nCore=maxCore(math.ceil(self.getParam("threads") / 4)),
                )

        self.stepInfoRec(cmds=all_cmd, finishFlag=finishFlag)

    def createPONcheck(
        self,
    ):
        fafile = os.path.join(self.getParam("ref"), self.getParam("genome") + ".fa")

        if not os.path.exists(fafile):
            raise commonError("file " + fafile + " don not exist!")
