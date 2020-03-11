# -*- coding: iso-8859-1 -*-
# Copyright (C) 2012-2018 TTTech Computertechnik AG. All rights reserved
# Schoenbrunnerstrasse 7, A--1040 Wien, Austria. office@tttech.com
# ++
# Name
#    CreateAATIssueList.py
#
# Purpose
#    Script for creating issues.txt file with issues
#     regarding AAT test reports
#
#
# Revision Dates
#     14-May-2018 (eILA) Creation
#
# Status: Development
# ------------------------------------------------------------------------------


import xml.etree.ElementTree as et
import os.path as path
import os
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(CURRENT_DIR, 'templates')


class Message():
    def __init__(self):
        self.message = ""
        self.prio = ""
        self.name = ""


class Issue():
    def __init__(self):
        self.swc = ""
        self.mssg = []


def xml_files_list(test_dir):
    list_issues = []
    xml_flag = 0
    if os.path.exists(test_dir):
        xml_flag = 0
        for child in os.listdir(test_dir):
            test_path = os.path.join(test_dir, child)
            if os.path.isdir(test_path):
                if os.path.isdir(test_path):
                    for filename in os.listdir(test_path):
                        if filename.endswith('.xml'):
                            xml_file = os.path.join(test_path, filename)
                            f_name = filename.split("_")[2]
                            issue = parse_test_report(xml_file, f_name[:-4])
                            list_issues.append(issue)
                            xml_flag = 1
    if xml_flag != 1:
        print "No expected XML files!"
        return -1
    return list_issues


def print_issue(list_of_issues, issue_path):
    file_system_loader = FileSystemLoader(TEMPLATE_PATH)
    env = Environment(loader=file_system_loader, trim_blocks=True)
    template = env.get_template("issues.template")
    context = {'issueList': list_of_issues
               }
    output = template.render(context)
    issue_path = os.path.join(issue_path, "issue.txt")

    try:
        with open(issue_path, "wb") as issue_file:
            issue_file.write(output)
            print "\nFile containing issues created: ", issue_path
    except:
        print "Issues report file is not created"
    flag_prio = 0
    counter = 0
    swc_counter = 0
    counter_witout = 0
    swc_prio_a = []
    swc_without = []
    for issue in list_of_issues:
        swc_counter = swc_counter + 1
        for msg in issue.mssg:
            if msg.prio == "PRIO_A":
                counter = counter + 1
                swc_prio_a.append(issue.swc)
                flag_prio = 1
                break
        if flag_prio != 1:
            counter_witout = counter_witout + 1
            swc_without.append(issue.swc)
        flag_prio = 0
    prio_msg = "\nNumber of SWCs with [PRIO_A]:   "
    print "%32s %2s" % (prio_msg, counter)
    for prio_a in swc_prio_a:
        print "    ", prio_a
    out_prio_msg = "\nNumber of SWCs without [PRIO_A]:"
    print "%32s %2s" % (out_prio_msg, counter_witout)
    for swc_no_prio_a in swc_without:
        print "    ", swc_no_prio_a
    total_msg = "\nTotal number od components:     "
    print "%32s %2s" % (total_msg, swc_counter)


def parse_test_report(xml_file, swc_name):
    tree = et.ElementTree(file=xml_file)
    root = tree.getroot()
    issue = Issue()
    issue.swc = swc_name
    tag_exp = '{http://tttech.com/SuplierReleaseNotes}Explanation'
    tag_name = '{http://tttech.com/SuplierReleaseNotes}Name'

    for child in root:
        if child.tag == '{http://tttech.com/TestReports}Test':
            for item in child.iter():
                if item.tag == '{http://tttech.com/TestReports}TestCase':
                    for ite in item.iter():
                        msg = Message()
                        if ite.tag == tag_exp:
                            if (ite.text is not None) and \
                                ("#NONE\n" not in ite.text) and \
                                    (ite.text != "\n"):
                                str_temp = ite.text
                                msg.prio = item.attrib["priority"]
                                for items in item.iter():

                                    if items.tag == tag_name:
                                        msg.name = (items.text)
                                        name_n = (items.text)
                                        explanation = \
                                            tc_name_check(name_n, str_temp)
                                msg.message = explanation
                                issue.mssg.append(msg)
    return issue


def tc_name_check(name, str_in):
    if "MISRA level check" in name:
        str_repl = str_in.replace("\n", " ")
        explanation = message_change(str_repl, name)
    elif "Check mandatory compiler/linker flags " in name:
        str_repl = str_in.replace("\n", " ")
        explanation = message_change(str_repl, name)
    elif "SWC limits check" in name:
        str_repl = str_in.replace("\n", " ")
        explanation = message_change(str_repl, name)
    elif "Check for mandatory MAP file" in name:
        str_repl = str_in.replace("\n", " ")
        explanation = message_change(str_repl, name)
    elif "Mandatory test case result check" in name:
        str_repl = str_in.replace("\n", " ")
        explanation = message_change(str_repl, name)
    elif "Check for mandatory test cases in the delivery" in name:
        str_repl = str_in.replace("\n", " ")
        explanation = message_change(str_repl, name)
    else:
        explanation = message_change(str_in.split("\n")[0], name)
    return explanation


def message_change(expl, name):
    if name == "Supplier's AITR check":
        explan = "AITR missing important information"
    elif name == "Release notes check":
        explan = "Release notes missing important information"
    elif name == "Supplier's AITR limits check":
        if "Runnable missing!" in expl:
            if "list:" in expl:
                str_rpl = expl.replace("list:", "")
            explan = str_rpl
        else:
            explan = "AITR's limits not equals to expected limits"
    elif name == "Mandatory test case result check":
        if " not executed." in expl:
            explan = "AITR contains test cases that not passed"
        else:
            explan = expl
    elif name == "Additional test case result check":
        explan = "AITR contains test cases that not passed"
    elif name == "RTE inteface usage check":
        if "Unused RTE Interfaces: " in expl:
            explan = "Unused RTE Interfaces."
        else:
            explan = expl
    elif name == "Check allowed compiler flags ":
        explan = "Not allowed flags found!"
    elif name == "Availability of dataset files check":
        if "Hex file" not in expl:
            explan = expl
        elif "found in 05_data" not in expl:
            strr = expl.split("\n")
            str_temp = strr[0].split(" ")
            str_t = str_temp[-2:]
            if str_t[0] == "Arcitecture":
                str_t[0] = "Architecture"
            explan = "Some hex files cannot be found in "+str_t[0]+" "+str_t[1]
        elif "found in 05_data" in expl:
            explan = \
                "Some hex files found in 05_data folder cannot be \
                found in Release Notes."
        else:
            explan = expl
    elif name == "Dataset version check":
        explan = "Some hex files have bad versions."
    elif name == "Interface check":
        string_list = expl.split(',')
        string_count = len(string_list)
        explan = (str(string_count) + " forbidden symbols found.")
    elif "Files missing from" in expl:
        explan = "Mandatory files missing"
    else:
        explan = expl
    return explan


def main(parent, tr_path, issue_path):
    lista = []
    dir_test_report = path.abspath(path.join(__file__, "../"))
    test_dir = tr_path
    try:
        lista = xml_files_list(test_dir)
        print_issue(lista, issue_path)
    except:
        return -1
