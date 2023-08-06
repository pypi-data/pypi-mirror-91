# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 15:54:49 2019
@author: Jiaqi Huang
"""

from yattag import Doc, indent
from .Configure import Configure
import datetime
import os
import shutil
import bz2
import pkg_resources
import glob
from .cfDNA_utils import getMaxFileNamePrefix, rmEndString, commonError


def report_generator(
    report_name=None,
    fastqcRes=None,
    identifyAdapterRes=None,
    bismarkRes=None,
    qualimapRes=None,
    deduplicateRes=None,
    rmduplicateRes=None,
    fraglenplotRes=None,
    CNVplotRes=None,
    CNVheatmapRes=None,
    CNV_GCcorrectRes=None,
    fragprof_GCcorrectRes=None,
    DeconCCNRes=None,
    outputdir=None,
):

    if outputdir is None:
        outputdir = Configure.getRepDir()

    # copy html elements
    htmlE_folder = os.path.join(outputdir, "HTML_Elements")
    if not os.path.exists(htmlE_folder):
        os.makedirs(htmlE_folder)
    shutil.copy(
        pkg_resources.resource_filename("cfDNApipe", "data/header_blue.png"), htmlE_folder,
    )
    shutil.copy(pkg_resources.resource_filename("cfDNApipe", "data/icon_1.png"), htmlE_folder)
    shutil.copy(pkg_resources.resource_filename("cfDNApipe", "data/icon_2.png"), htmlE_folder)
    shutil.copy(pkg_resources.resource_filename("cfDNApipe", "data/logo_1.png"), htmlE_folder)

    doc, tag, text, line = Doc().ttl()
    write_head(report_name, doc, tag, text, line)
    write_body(
        report_name,
        doc,
        tag,
        text,
        line,
        fastqcRes,
        identifyAdapterRes,
        bismarkRes,
        qualimapRes,
        deduplicateRes,
        rmduplicateRes,
        fraglenplotRes,
        CNVplotRes,
        CNVheatmapRes,
        CNV_GCcorrectRes,
        fragprof_GCcorrectRes,
        DeconCCNRes,
        outputdir,
    )
    html_name = report_name + ".html"
    fout = open(os.path.join(outputdir, html_name), "w")
    fout.write(indent(doc.getvalue()))
    fout.close()


def write_head(report_name, doc, tag, text, line):
    # read the header bz2 file
    href_file = pkg_resources.resource_filename("cfDNApipe", "data/src_href.bz2")
    with bz2.open(href_file, "rt") as fscript:
        textscript = fscript.read()
    srch = textscript.split("\n")

    # write the html head
    doc.asis("<!DOCTYPE html>")

    with tag("html", xmlns="http://www.w3.org/1999/xhtml"):
        with tag("head"):
            doc.stag("meta", charset="utf-8")
            doc.asis('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
            doc.stag("meta", name="date", content=str(datetime.date.today()))

            with tag("title"):
                text(report_name)

            with tag("script", src=srch[0]):
                text()

            doc.stag("meta", name="viewport", content="width=device-width, initial-scale=1")

            with tag("link", href=srch[1], rel="stylesheet"):
                text()

            with tag("script", src=srch[2]):
                text()

            with tag("script", src=srch[3]):
                text()

            with tag("script", src=srch[4]):
                text()

            with tag("script", src=srch[5]):
                text()

            with tag("link", href=srch[6], rel="stylesheet"):
                text()

            with tag("script", src=srch[7]):
                text()

            with tag("script", src=srch[8]):
                text()

            with tag("link", href=srch[9], rel="stylesheet"):
                text()

            with tag("script", src=srch[10]):
                text()

            with tag("link", href=srch[11], rel="stylesheet"):
                text()

            with tag("script", src=srch[12]):
                text()

            with tag("style", type="text/css"):
                text("code{white-space: pre;}")

            with tag("style", type="text/css"):
                text("\n  pre:not([class]){\n    background-color: white;\n  }")

            with tag("script", type="text/javascript"):
                doc.asis(
                    '\nif (window.hljs) {\n  hljs.configure({languages: []});\n  hljs.initHighlightingOnLoad();\n  if (document.readyState && document.readyState === "complete") {\n    window.setTimeout(function() { hljs.initHighlighting(); }, 0);\n  }\n}'
                )

            with tag("style", type="text/css"):
                text(
                    """
                .title1 {
                    font-size: 40px;
                    font-family: Roboto;
                    font-weight: bold;
                    line-height: 53px;
                    color: #20262A;
                    opacity: 1;
                    }
                """
                )
                text(
                    """
                    .text1 {
                    font-size: 16px;
                    font-family: Roboto;
                    font-weight: 400;
                    line-height: 21px;
                    color: #20262A;
                    opacity: 1;
                    }
                    }
                """
                )
                text(
                    """
                    .text2 {
                        font-size: 14px;
                        font-family: Roboto;
                        font-weight: 500;
                        color: #171717;
                        opacity: 1;
                    }
                """
                )
                # card1 for 1 row 2 cards
                text(
                    """
                    card1 {
                        width: 300px;
                        height: 40px;
                        background: rgba(0, 82, 204, 0.1);
                        border-radius: 8px;
                        float:left;
                        display: block;
                        margin-right: 24px;
                        margin-bottom: 43px;
                        padding: 10px 24px 10px 20px
                    }
                """
                )
                # card2 for 1 row 1 cards
                text(
                    """
                    card2 {
                        width: 250px;
                        height: 40px;
                        background: rgba(0, 82, 204, 0.1);
                        border-radius: 8px;
                        display: block;
                        margin-right: 24px;
                        margin-bottom: 43px;
                        padding: 10px 24px 10px 20px
                    }
                """
                )
                text("\nh1 {\n  font-size: 34px;\n}\n")
                text("h2 {\n  font-size: 24px;\n}\n")
                text("h3 {\n  font-size: 18px;\n}\n")
                text("h4 {\n  font-size: 10px;\n}\n")
                text("h5 {\n  font-size: 10px;\n}\n")
                text(".table th:not([align]) {\n  text-align: left;\n}")

            with tag("style", type="text/css"):
                text(
                    "\ntable.customize {\n	font-size:12px;\n	color:#333333;\n	border-width: 1px;\n	border-color: #888888;\n	border-collapse: collapse;\n}"
                )
                text(
                    "\ntable.customize th {\n	border-width: 1px;\n	padding: 8px;\n	border-style: solid;\n	border-color: #888888;\n}"
                )
                text(
                    "\ntable.customize td {\n	border-width: 2px;\n	padding: 6px;\n	border-left-style: none;\n	border-right-style: none;\n	border-top-style: solid;\n	border-bottom-style: solid;\n	border-color: #DFDFDF;\n}"
                )


def write_body(
    report_name,
    doc,
    tag,
    text,
    line,
    fastqcRes,
    identifyAdapterRes,
    bismarkRes,
    qualimapRes,
    deduplicateRes,
    rmduplicateRes,
    fraglenplotRes,
    CNVplotRes,
    CNVheatmapRes,
    CNV_GCcorrectRes,
    fragprof_GCcorrectRes,
    DeconCCNRes,
    outputdir,
):
    with tag("body"):
        with tag("style", type="text/css"):
            text("\n.main-container {\n  max-width: 940px;\n  margin-left: auto;\n  margin-right: auto;\n}")
            text("\ncode {\n  color: inferit;\n  background-color: rgba(0, 0, 0, 0.04);\n}")
            text("\nimg {\n  max-width: 100%;\n  height: auto;\n}")
            text("\n.tabbed-pane {\n  padding-top: 12px;\n}")
            text("\nbutton.code-folding-btn:focus {\n  outling: none;\n}")

        # Main title
        with tag("div", id="container", style="width:1280px;margin:0 auto;"):
            with tag(
                "div",
                style="background:rgba(0,0,0,1);;padding:10px 0px 0px 108px;height:100px;width:1280px;background:url(./HTML_Elements/header_blue.png);background-size:1280px 100px;background-repeat:no-repeat;z-index: 10",
            ):
                doc.stag(
                    "img",
                    src=os.path.join("./HTML_Elements", "logo_1.png"),
                    style="margin-right:8px;width:36px;height:46.46px;float:left",
                )
                with tag(
                    "div", style="float:left;margin-bottom:8px;color:white", klass="title1",
                ):
                    text(report_name)

                with tag("div", style="clear:both"):
                    with tag(
                        "div", klass="text1", style="margin-left:650px;margin-bottom:32px;color:white",
                    ):
                        text(str(datetime.date.today()))

        # TOC part, all parts are controlled by TOC
        with tag("div", klass="container-fluid main-container"):
            with tag("script"):
                doc.asis('\n$(document).ready(function () {\n  window.buildTabsets("TOC");\n});')

            with tag("script"):
                doc.asis(
                    "\n$(document).ready(function ()  {\n\n    // move toc-ignore selectors from section div to header\n    $('div.section.toc-ignore')\n        .removeClass('toc-ignore')\n        .children('h1,h2,h3,h4,h5').addClass('toc-ignore');\n\n    // establish options\n    var options = {\n      selectors: \"h1,h2,h3\",\n      theme: \"bootstrap3\",\n      context: '.toc-content',\n      hashGenerator: function (text) {\n        return text.replace(/[.\\/?&!#<>]/g, '').replace(/\s/g, '_').toLowerCase();\n      },\n      ignoreSelector: \".toc-ignore\",\n      scrollTo: 0\n    };\n    options.showAndHide = true;\n    options.smoothScroll = true;\n\n    // tocify\n    var toc = $(\"#TOC\").tocify(options).data(\"toc-tocify\");\n});"
                )

            with tag("style", type="text/css"):
                text(
                    "\n#TOC {\n  margin: 50px 0px 20px 0px;\n}\n@media (max-width: 768px) {\n#TOC {\n  position: relative;\n  width: 100%;\n}\n}"
                )
                text("\n.toc-content {\n  padding-left: 30px;\n  padding-right: 40px;\n}")
                text("\ndiv.main-container {\n  max-width: 1200px;\n}")
                text("\ndiv.tocify {\n  width: 20%;\n  max-width: 260px;\n  max-height: 85%;\n}")
                text("\n@media (min-width: 768px) and (max-width: 991px) {\n  div.tocify {\n    width: 25%;\n  }\n}")
                text("\n@media (max-width: 767px) {\n  div.tocify {\n    width: 100%;\n    max-width: none;\n  }\n}")
                text("\n.tocify ul, .tocify li {\n  line-height: 20px;\n}")
                text(
                    "\n.tocify-subheader .tocify-item {\n  font-size: 0.90em;\n  padding-left: 25px;\n  text-indent: 0;\n}"
                )
                text("\n.tocify .list-group-item {\n  border-radius: 0px;\n}")

            with tag("div", klass="row-fluid"):
                with tag("div", klass="col-xs-12 col-sm-4 col-md-3"):
                    with tag("div", id="TOC", klass="tocify"):
                        text()

                with tag("div", klass="toc-content col-xs-12 col-sm-8 col-md-9"):
                    title_count = 1

                    # fastqc report
                    if fastqcRes is not None:
                        with tag(
                            "div", id="fastqc_report", klass="section level1", style="margin:120px 20px 20px 20px",
                        ):
                            with tag("h1"):
                                with tag("span", klass="header-section-number"):
                                    text(str(title_count) + ". Fastq Quality Control")

                            write_fastqc_report(doc, tag, text, line, fastqcRes, outputdir)

                        doc.stag("br")

                        title_count += 1

                    # identifyadapter report
                    if identifyAdapterRes is not None:
                        with tag(
                            "div", id="idadapter_report", klass="section level1", style="margin:20px",
                        ):
                            with tag("h1"):
                                with tag("span", klass="header-section-number"):
                                    text(str(title_count) + ". Adapter Detection")

                            write_identifyadapter_report(doc, tag, text, line, identifyAdapterRes)

                        doc.stag("br")

                        title_count += 1

                    # bismark report
                    if bismarkRes is not None:
                        with tag(
                            "div", id="bismark_report", klass="section level1", style="margin:20px",
                        ):
                            with tag("h1"):
                                with tag("span", klass="header-section-number"):
                                    text(str(title_count) + ". Bismark Alignment")
                            write_bismark_report(doc, tag, text, line, bismarkRes)

                        doc.stag("br")

                        title_count += 1

                    # qualimap report
                    if qualimapRes is not None:
                        with tag(
                            "div", id="qualimap_report", klass="section level1", style="margin:20px",
                        ):
                            with tag("h1"):
                                with tag("span", klass="header-section-number"):
                                    text(str(title_count) + ". Qualimap")

                            write_qualimap_report(doc, tag, text, line, qualimapRes, outputdir)

                        doc.stag("br")

                        title_count += 1

                    # deduplicate report
                    if deduplicateRes is not None:
                        with tag(
                            "div", id="deduplicate_report", klass="section level1", style="margin:20px",
                        ):
                            with tag("h1"):
                                with tag("span", klass="header-section-number"):
                                    text(str(title_count) + ". Alignment Duplication Analysis")

                            write_deduplicate_report(doc, tag, text, line, deduplicateRes)

                        doc.stag("br")

                        title_count += 1

                    # rmduplicate report
                    if rmduplicateRes is not None:
                        with tag(
                            "div", id="rmduplicate_report", klass="section level1", style="margin:20px",
                        ):
                            with tag("h1"):
                                with tag("span", klass="header-section-number"):
                                    text(str(title_count) + ". Alignment Duplication Analysis")

                            write_rmduplicate_report(doc, tag, text, line, rmduplicateRes)

                        doc.stag("br")

                        title_count += 1

                    # fraglenplot report
                    if fraglenplotRes is not None:
                        with tag(
                            "div", id="fraglenplot_report", klass="section level1", style="margin:20px",
                        ):
                            with tag("h1"):
                                with tag("span", klass="header-section-number"):
                                    text(str(title_count) + ". Fragment Length Distribution")

                            write_fraglenplot_report(doc, tag, text, line, fraglenplotRes, outputdir)

                        doc.stag("br")

                        title_count += 1

                    # CNVplot report
                    if CNVplotRes is not None:
                        with tag(
                            "div", id="CNVplot_report", klass="section level1", style="margin:20px",
                        ):
                            with tag("h1"):
                                with tag("span", klass="header-section-number"):
                                    text(str(title_count) + ". Copy Number Variation Analysis")

                            write_CNVplot_report(doc, tag, text, line, CNVplotRes, outputdir)

                        doc.stag("br")

                        title_count += 1

                    # CNVheatmap report
                    if CNVheatmapRes is not None:
                        with tag(
                            "div", id="CNVheatmap_report", klass="section level1", style="margin:20px",
                        ):
                            with tag("h1"):
                                with tag("span", klass="header-section-number"):
                                    text(str(title_count) + ". CNV Heatmap")

                            write_CNVheatmap_report(doc, tag, text, line, CNVheatmapRes, outputdir)

                        doc.stag("br")

                        title_count += 1

                    # CNV GCcorrect report
                    if CNV_GCcorrectRes is not None:
                        with tag(
                            "div", id="CNV_GCcorrect_report", klass="section level1", style="margin:20px",
                        ):
                            with tag("h1"):
                                with tag("span", klass="header-section-number"):
                                    text(str(title_count) + ". Arm-Level CNV GC Bias Correction")

                            write_GCcorrect_report(
                                doc, tag, text, line, CNV_GCcorrectRes, outputdir, duplicatekey="CNV",
                            )

                        doc.stag("br")

                        title_count += 1

                    # fragprof GCcorrect report
                    if fragprof_GCcorrectRes is not None:
                        with tag(
                            "div", id="fragprof_GCcorrect_report", klass="section level1", style="margin:20px",
                        ):
                            with tag("h1"):
                                with tag("span", klass="header-section-number"):
                                    text(str(title_count) + ". Fragmentation Profile GC Bias Correction")

                            write_GCcorrect_report(
                                doc, tag, text, line, fragprof_GCcorrectRes, outputdir, duplicatekey="fp",
                            )

                        doc.stag("br")

                        title_count += 1

                    # DeconCCN report
                    if DeconCCNRes is not None:
                        with tag(
                            "div", id="fragprof_DeconCCN_report", klass="section level1", style="margin:20px",
                        ):
                            with tag("h1"):
                                with tag("span", klass="header-section-number"):
                                    text(str(title_count) + ". DeconCCN Result")

                            write_DeconCCN_report(
                                doc, tag, text, line, DeconCCNRes, outputdir,
                            )

                        doc.stag("br")

                        title_count += 1

        with tag("script"):
            doc.asis(
                "\nfunction bootstrapStylePandocTables() {\n  $('tr.header').parent('thead').parent('table').addClass('table table-condensed');\n$(document).ready(function () {\n  bootstrapStylePandocTables();\n});"
            )

        with tag("script"):
            doc.asis(
                '\n (function () {\n    var script = document.createElement("script");\n    script.type = "text/javascript";\n    script.src  = "https://mathjax.rstudio.com/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML";\n    document.getElementsByTagName("head")[0].appendChild(script);\n  })();'
            )


def write_bismark_report(doc, tag, text, line, report_dir, max_sample=5):
    sample_num = 0
    for report in report_dir.getOutput("bismkRepOutput"):
        sample_num += 1
        if sample_num > max_sample:  # ignore the rest to shorten the report length
            break
        with tag("div", id="bismark_report_sub", klass="section level2", style="margin:20px"):
            with tag("h2"):
                text("Sample: " + report.split("/")[-1].split(".")[0])
            write_bismark_report_contents(doc, tag, text, line, report)


def write_bismark_report_contents(doc, tag, text, line, report):
    # read and locate PE_report.txt
    fin = open(report, "r", encoding="utf-8")
    cont = fin.readlines()
    for i in range(len(cont)):
        cont[i] = cont[i].strip("\n")
        if cont[i] == "Final Alignment report":
            p = i

    # Final Alignment Report
    with tag("div", style="line-height:30px"):
        with tag("div", style="font-size:18px"):
            text("Final Alignment Report")
        with tag("ul", id="bismark_report_content"):
            for j in range(p + 2, p + 8):
                line("li", cont[j])

            with tag("li"):
                text(cont[p + 9])

                with tag("div", style="line-height:20px"):
                    with tag("table", klass="customize", width="100%"):
                        for j in range(p + 10, p + 14):
                            linex = cont[j].split("\t")
                            with tag("tr"):
                                if j % 2 == 0:
                                    doc.attr(klass="odd")
                                else:
                                    doc.attr(klass="even")

                                with tag("td", align="left"):
                                    text(linex[0])

                                with tag("td", align="left"):
                                    text(linex[1])

                                with tag("td", align="left"):
                                    text(linex[2])

                line("li", cont[p + 15])

    for i in range(len(cont)):
        cont[i] = cont[i].strip("\n")
        if cont[i] == "Final Cytosine Methylation Report":
            p = i

    MC_CHG = int(cont[p + 5].split()[-1])
    MC_CHH = int(cont[p + 6].split()[-1])
    MC_UnknownC = int(cont[p + 7].split()[-1])
    UNC_CHG = int(cont[p + 10].split()[-1])
    UNC_CHH = int(cont[p + 11].split()[-1])
    UNC_UnknownC = int(cont[p + 12].split()[-1])
    estimated_conversion_rate = 1 - (MC_CHG + MC_CHH + MC_UnknownC) / (
        MC_CHG + MC_CHH + MC_UnknownC + UNC_CHG + UNC_CHH + UNC_UnknownC
    )

    # Final Cytosine Methylation Report
    with tag("div", style="line-height:30px"):
        with tag("div", style="font-size:18px"):
            text("Final Cytosine Methylation Report")
        with tag("ul", id="bismark_report_content"):
            for j in range(p + 2, p + 17):
                if cont[j] != "":
                    line("li", cont[j])

            line(
                "li", "Estimated Bisulfite Conversion Rate: " + str(round(estimated_conversion_rate, 3) * 100) + "%",
            )

    fin.close()


def write_identifyadapter_report(doc, tag, text, line, report_dir, max_sample=5):
    sample_num = 0
    for tmp_output in report_dir.getOutputs():
        if "-adapterFile" in tmp_output:
            sample_num += 1
            if sample_num > max_sample:  # ignore the rest to shorten the report length
                break
            report = report_dir.getOutput(tmp_output)
            with tag("div", id="idadapters_sub", klass="section level2", style="margin:20px"):
                with tag("h2"):
                    text("Sample: " + report.split("/")[-1].replace("-adapters.log", ""))
                write_identifyadapter_report_contents(doc, tag, text, line, report)


def write_identifyadapter_report_contents(doc, tag, text, line, report):
    # read and locate adapters.log
    fin = open(report, "r", encoding="utf-8")
    cont = fin.readlines()

    # contents
    with tag("div", style="line-height:30px"):
        for i in range(len(cont)):
            if "--adapter" in cont[i]:
                with tag("pre", id="adapter_content"):
                    for j in range(i, i + 4):
                        text(cont[j] + "\n")

                doc.stag("br")

            elif "Top 5" in cont[i]:
                text(cont[i][4:] + "\n")
                with tag("div", style="line-height:20px"):
                    with tag("div", style="overflow-y: auto; height: 100px"):
                        with tag("table", klass="customize", width="100%"):
                            for j in range(i + 1, i + 6):
                                linex = cont[j].split(" ")
                                with tag("tr"):
                                    if j % 2 == 0:
                                        doc.attr(klass="odd")
                                    else:
                                        doc.attr(klass="even")
                                    for k in range(len(linex)):
                                        if linex[k] != "" and ":" not in linex[k] and "=" not in linex[k]:
                                            with tag("td", align="left"):
                                                text(linex[k])

                doc.stag("br")

    fin.close


def write_fastqc_report(doc, tag, text, line, report_dir, outputdir, max_sample=5):
    text(
        "The followings are quality control files generated by FastQC. For more detailed information, please click the hyperlinks below."
    )
    sample_num = 0

    dstdir = os.path.join(outputdir, "Fastq_Quality_Control")
    if not os.path.exists(dstdir):
        os.makedirs(dstdir)

    qcfiles = glob.glob(os.path.join(report_dir.getOutput("outputdir"), "*fastqc.html"))
    qcfiles.sort()

    if Configure.getType() == "paired":
        for file1, file2 in zip(qcfiles[0::2], qcfiles[1::2]):
            sample_num += 1

            if sample_num > max_sample:  # ignore the rest to shorten the report length
                break

            sample_name = getMaxFileNamePrefix(file1, file2)

            # copy files
            shutil.copyfile(file1, os.path.join(dstdir, os.path.basename(file1)))
            shutil.copyfile(file2, os.path.join(dstdir, os.path.basename(file2)))

            with tag(
                "div", id="fastqc_report_sub", klass="section level2", style="margin:20px",
            ):
                with tag("h2"):
                    text("Sample: " + sample_name)

                # file1
                with tag("card1"):
                    doc.stag(
                        "img",
                        src=os.path.join("./HTML_Elements", "icon_1.png"),
                        style="cursor:pointer;height:20px;width:20px;float:left;margin-right:16px",
                    )
                    with tag("div", klass="text2", style="float:left"):
                        text(os.path.basename(file1))
                    with tag("a", href="./Fastq_Quality_Control/" + os.path.basename(file1), target="_blank"):
                        doc.stag(
                            "img",
                            src=os.path.join("./HTML_Elements", "icon_2.png"),
                            style="cursor:pointer;margin-top:3px;height:14.14px;width:8.5px;float:right",
                        )

                # file2
                with tag("card1"):
                    doc.stag(
                        "img",
                        src=os.path.join("./HTML_Elements", "icon_1.png"),
                        style="cursor:pointer;height:20px;width:20px;float:left;margin-right:16px",
                    )
                    with tag("div", klass="text2", style="float:left"):
                        text(os.path.basename(file2))
                    with tag("a", href="./Fastq_Quality_Control/" + os.path.basename(file2), target="_blank"):
                        doc.stag(
                            "img",
                            src=os.path.join("./HTML_Elements", "icon_2.png"),
                            style="cursor:pointer;margin-top:3px;height:14.14px;width:8.5px;float:right",
                        )

            doc.stag("br")
    elif Configure.getType() == "single":
        for qcfile in qcfiles:
            sample_num += 1

            if sample_num > max_sample:  # ignore the rest to shorten the report length
                break

            sample_name = rmEndString(os.path.split(qcfile)[-1], ["*fastqc.html", "R", "_", ".", "*"])

            # copy files
            shutil.copyfile(qcfile, os.path.join(dstdir, os.path.basename(qcfile)))

        with tag(
            "div", id="fastqc_report_sub", klass="section level2", style="margin:20px",
        ):
            with tag("h2"):
                text("Sample: " + sample_name)

            with tag("card2"):
                doc.stag(
                    "img",
                    src=os.path.join("./HTML_Elements", "icon_1.png"),
                    style="cursor:pointer;height:20px;width:20px;float:left;margin-right:16px",
                )
                with tag("div", klass="text2", style="float:left"):
                    text(os.path.basename(qcfile))
                with tag(
                    "a", href="./Fastq_Quality_Control/" + os.path.basename(qcfile), target="_blank",
                ):
                    doc.stag(
                        "img",
                        src=os.path.join("./HTML_Elements", "icon_2.png"),
                        style="cursor:pointer;margin-top:3px;height:14.14px;width:8.5px;float:right",
                    )

    else:
        raise commonError("Data type must be paired or single!")


def write_qualimap_report(doc, tag, text, line, report_dir, outputdir, max_sample=5):
    text("The followings are Qualimap reports. For more detailed information, please click the hyperlinks below.")
    sample_num = 0
    for report in report_dir.getOutput("htmlOutput"):
        sample_num += 1
        if sample_num > max_sample:  # ignore the rest to shorten the report length
            break
        report_dir, report_name = os.path.split(report)
        dstdir = outputdir + "/Qualimap/" + report_dir.split("/")[-1] + "/"
        if not os.path.exists(dstdir):
            os.makedirs(dstdir)
        for root, dirs, files in os.walk(report_dir):
            for file in files:
                src_file = os.path.join(root, file)
                shutil.copy(src_file, dstdir)
            for dir in dirs:
                subdir = os.path.join(root, dir)
                subdstdir = dstdir + "/" + dir
                if not os.path.exists(subdstdir):
                    os.makedirs(subdstdir)
                for subroot, subdirs, subfiles in os.walk(subdir):
                    for subfile in subfiles:
                        src_subfile = os.path.join(subdir, subfile)
                        shutil.copy(src_subfile, subdstdir)
            break
        shutil.copy(report, dstdir)

        with tag(
            "div", id="qualimap_report_sub", klass="section level2", style="margin:20px",
        ):
            with tag("h2"):
                text("Sample: " + report_dir.split("/")[-1])

            with tag("card2"):
                doc.stag(
                    "img",
                    src=os.path.join("./HTML_Elements", "icon_1.png"),
                    style="cursor:pointer;height:20px;width:20px;float:left;margin-right:16px",
                )
                with tag("div", klass="text2", style="float:left"):
                    text(report_name)
                with tag(
                    "a", href="Qualimap/" + report_dir.split("/")[-1] + "/" + report_name, target="_blank",
                ):
                    doc.stag(
                        "img",
                        src=os.path.join("./HTML_Elements", "icon_2.png"),
                        style="cursor:pointer;margin-top:3px;height:14.14px;width:8.5px;float:right",
                    )


def write_CNVplot_report(doc, tag, text, line, report_dir, outputdir, max_sample=5):
    text(
        "The followings are plots generated by cnvPlot. For more detailed information, please click the hyperlinks below."
    )

    # create folder
    dstdir = os.path.join(outputdir, "CNV_Plot")
    if not os.path.exists(dstdir):
        os.makedirs(dstdir)

    sample_num = 0
    if "diagram_pdf" in report_dir.getOutputs():
        for report in report_dir.getOutput("diagram_pdf"):
            sample_num += 1
            if sample_num > max_sample:  # ignore the rest to shorten the report length
                break
            with tag(
                "div", id="CNVplot_report_sub", klass="section level2", style="margin:20px",
            ):
                with tag("h2"):
                    text("Sample: " + report.split("/")[-1].replace("_diagram.pdf", ""))

                # copy diagram.pdf
                _, report_name = os.path.split(report)
                shutil.copyfile(report, os.path.join(dstdir, report_name))

                with tag("card1"):
                    doc.stag(
                        "img",
                        src=os.path.join("./HTML_Elements", "icon_1.png"),
                        style="cursor:pointer;height:20px;width:20px;float:left;margin-right:16px",
                    )
                    with tag("div", klass="text2", style="float:left"):
                        text(report_name)
                    with tag("a", href="./CNV_Plot/" + report_name, target="_blank"):
                        doc.stag(
                            "img",
                            src=os.path.join("./HTML_Elements", "icon_2.png"),
                            style="cursor:pointer;margin-top:3px;height:14.14px;width:8.5px;float:right",
                        )

                if "scatter_pdf" in report_dir.getOutputs():
                    if os.path.exists(report.replace("_diagram.pdf", "_scatter.pdf")):
                        with tag("card1"):
                            doc.stag(
                                "img",
                                src=os.path.join("./HTML_Elements", "icon_1.png"),
                                style="cursor:pointer;height:20px;width:20px;float:left;margin-right:16px",
                            )
                            with tag("div", klass="text2", style="float:left"):
                                text(report_name)
                            with tag("a", href="./CNV_Plot/" + report_name, target="_blank"):
                                doc.stag(
                                    "img",
                                    src=os.path.join("./HTML_Elements", "icon_2.png"),
                                    style="cursor:pointer;margin-top:3px;height:14.14px;width:8.5px;float:right",
                                )

            doc.stag("br")
    else:
        if "scatter_pdf" in report_dir.getOutputs():
            for report in report_dir.getOutput("scatter_pdf"):
                sample_num += 1
                if sample_num > max_sample:  # ignore the rest to shorten the report length
                    break

                # copy diagram.pdf
                _, report_name = os.path.split(report)
                shutil.copyfile(report, os.path.join(dstdir, report_name))

                with tag(
                    "div", id="CNVplot_report_sub", klass="section level2", style="margin:20px",
                ):
                    with tag("h2"):
                        text("Sample: " + report.split("/")[-1].replace("_scatter.pdf", ""))
                        with tag("card2"):
                            doc.stag(
                                "img",
                                src=os.path.join("./HTML_Elements", "icon_1.png"),
                                style="cursor:pointer;height:20px;width:20px;float:left;margin-right:16px",
                            )
                            with tag("div", klass="text2", style="float:left"):
                                text(report_name)
                            with tag(
                                "a", href="./CNV_Plot/" + report_name, target="_blank",
                            ):
                                doc.stag(
                                    "img",
                                    src=os.path.join("./HTML_Elements", "icon_2.png"),
                                    style="cursor:pointer;margin-top:3px;height:14.14px;width:8.5px;float:right",
                                )

                doc.stag("br")


def write_CNVheatmap_report(doc, tag, text, line, report_dir, outputdir):
    text("For more detailed information, please click the hyperlinks below.")
    report = report_dir.getOutput("heatmap")
    dstdir = os.path.join(outputdir, "CNV_Heatmap")
    if not os.path.exists(dstdir):
        os.makedirs(dstdir)

    report_dir, report_name = os.path.split(report)
    shutil.copyfile(report, os.path.join(dstdir, report_name))
    with tag("div", id="CNVheatmap_report_sub", klass="section level2", style="margin:20px"):
        with tag("card2"):
            doc.stag(
                "img",
                src=os.path.join("./HTML_Elements", "icon_1.png"),
                style="cursor:pointer;height:20px;width:20px;float:left;margin-right:16px",
            )
            with tag("div", klass="text2", style="float:left"):
                text(report_name)
            with tag(
                "a", href="CNV_Heatmap/" + report_name, target="_blank",
            ):
                doc.stag(
                    "img",
                    src=os.path.join("./HTML_Elements", "icon_2.png"),
                    style="cursor:pointer;margin-top:3px;height:14.14px;width:8.5px;float:right",
                )


def write_deduplicate_report(doc, tag, text, line, report_dir, max_sample=5):
    sample_num = 0
    for report in report_dir.getOutput("reportOutput"):
        sample_num += 1
        if sample_num > max_sample:  # ignore the rest to shorten the report length
            break
        with tag(
            "div", id="deduplicate_report_sub", klass="section level3", style="margin:20px",
        ):
            with tag("h2"):
                text("Sample: " + report.split("/")[-1].split(".")[0])
            write_deduplicate_report_contents(
                doc, tag, text, line, report,
            )


def write_deduplicate_report_contents(doc, tag, text, line, report):
    f = open(report, "r")
    rs = f.readlines()
    with tag("div", style="line-height:30px"):
        with tag("ul", id="deduplicate_report_content"):
            line("li", rs[2])
            line("li", rs[5])
    f.close()


def write_rmduplicate_report(doc, tag, text, line, report_dir, max_sample=5):
    sample_num = 0
    with tag("div", id="rmduplicate_report_sub", klass="section level2", style="margin:20px"):
        with tag("div", style="line-height:20px"):
            with tag("table", klass="customize", width="100%"):
                with tag("tr"):
                    doc.attr(klass="odd")

                    with tag("td", align="left"):
                        text("SAMPLE_NAME")

                    with tag("td", align="left"):
                        text("READ_PAIRS_EXAMINED")

                    with tag("td", align="left"):
                        text("READ_PAIR_DUPLICATES")

                    with tag("td", align="left"):
                        text("PERCENT_DUPLICATION")

                    with tag("td", align="left"):
                        text("ESTIMATED_LIBRARY_SIZE")

                for report in report_dir.getOutput("metricsOutput"):
                    sample_num += 1
                    if sample_num > max_sample:  # ignore the rest to shorten the report length
                        break
                    with tag("tr"):
                        if sample_num % 2 == 0:
                            doc.attr(klass="odd")
                        else:
                            doc.attr(klass="even")
                        write_rmduplicate_report_contents(doc, tag, text, line, report)


def write_rmduplicate_report_contents(doc, tag, text, line, report):
    # read and locate rmdup.txt
    fin = open(report, "r", encoding="utf-8")
    conts = fin.readlines()
    cont = conts[7]
    data = cont.split("\t")

    # contents
    with tag("td", align="left"):
        text(report.split("/")[-1].replace("-rmdup.txt", ""))

    with tag("td", align="left"):
        text(data[2])

    with tag("td", align="left"):
        text(data[6])

    with tag("td", align="left"):
        text(data[8])

    with tag("td", align="left"):
        text(data[9])

    fin.close()


def write_fraglenplot_report(doc, tag, text, line, report_dir, outputdir):
    report = report_dir.getOutput("multiplotOutput")
    with tag("div", id="fraglenplot_report_sub", klass="section level2"):
        text("Fragment length distribution of the samples:")
    write_fraglenplot_report_contents(doc, tag, text, line, report, outputdir)


def write_fraglenplot_report_contents(doc, tag, text, line, report, outputdir):
    dstdir = outputdir + "/Fragment_Length/"
    if not os.path.exists(dstdir):
        os.makedirs(dstdir)
    report_dir, report_name = os.path.split(report)
    dstfile = os.path.join(dstdir, report_name)
    shutil.copyfile(report, dstfile)
    doc.stag("img", src="Fragment_Length/" + report_name, alt=dstfile)


def write_GCcorrect_report(doc, tag, text, line, report_dir, outputdir, duplicatekey, max_sample=5):
    with tag("div", id="GCcorrect_report_sub", klass="section level2"):
        text("GC correction of the samples: (left is before correction, right is after correction)")
    sample_num = 0
    for report in report_dir.getOutput("plotOutput"):
        sample_num += 1
        if sample_num > max_sample:  # ignore the rest to shorten the report length
            break
        with tag(
            "div", id="GCcorrect_report_sub", klass="section level2", style="margin:20px",
        ):
            with tag("h2"):
                text("Sample: " + report.split("/")[-1].replace("_gc_cor", "").replace(".png", ""))
            write_GCcorrect_report_contents(doc, tag, text, line, report, outputdir, duplicatekey)


def write_GCcorrect_report_contents(doc, tag, text, line, report, outputdir, duplicatekey):
    dstdir = outputdir + "/GC_Correct_" + duplicatekey + "/"
    if not os.path.exists(dstdir):
        os.makedirs(dstdir)
    report_dir, report_name = os.path.split(report)
    dstfile = os.path.join(dstdir, report_name)
    shutil.copyfile(report, dstfile)
    doc.stag("img", src="GC_Correct_" + duplicatekey + "/" + report_name, alt=dstfile)


def write_DeconCCN_report(doc, tag, text, line, report_dir, outputdir):
    report = report_dir.getOutput("plotOutput")
    with tag("div", id="OCF_report_sub", klass="section level2", style="margin:20px"):
        text("DeconCCN results for part of the samples:")
    write_DeconCCN_report_contents(doc, tag, text, line, report, outputdir)


def write_DeconCCN_report_contents(doc, tag, text, line, report, outputdir):
    dstdir = outputdir + "/DeconCCN/"
    if not os.path.exists(dstdir):
        os.makedirs(dstdir)
    report_dir, report_name = os.path.split(report)
    dstfile = os.path.join(dstdir, report_name)
    shutil.copyfile(report, dstfile)
    doc.stag("img", src="DeconCCN/" + report_name, alt=dstfile)
