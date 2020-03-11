# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib
from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig
from fpdf import FPDF
import os
import math


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(CURRENT_DIR, 'icons', 'ftn-logo.png')

project_name = u"Diplomski rad" 

class PDF(FPDF):
    def header(self):

        if self.page_no() == 1:
            self.image(LOGO_PATH, self.w - self.r_margin - 35, 7, 25)

        else:
            # logo
            epw = self.w - 2*self.l_margin
            self.image(LOGO_PATH, self.w - self.r_margin - 15, 7, 15)

            # thick line
            self.ln(7)
            self.set_draw_color(1, 130, 172)
            self.set_line_width(0.8)
            y = 25
            self.line(20, y, epw + self.l_margin, y)

            # text
            self.ln(2)
            self.set_x(23)
            self.set_draw_color(0, 0, 0)
            self.set_font('arial', '', 8.0)
            self.cell(h=0.0, align='L', w=0, txt="Project:  " + project_name, border=0)
            self.set_x(epw / 2)
            self.set_font('arial', 'B', 8.0)
            self.cell(h=0.0, align='L', w=0, txt="Application Acceptance Test Report", border=0)
            self.set_x(epw + 10)
            self.set_font('arial', '', 8.0)
            self.cell(0, 0, 'Page ' + str(self.page_no()), 0, 0, 'L')

            # thin line
            self.ln(5)
            self.set_draw_color(1, 130, 172)
            self.set_line_width(0.2)
            y = self.get_y()
            self.line(20, y, epw + self.l_margin, y)

    def footer(self):

        epw = self.w - 2*self.l_margin

        if self.page_no() == 1:

            self.set_draw_color(1, 1, 1)
            self.set_line_width(0.2)
            self.line(20, 275, 190.0, 275)


            text = "Copyright " + u'\u00a9' + " 2019, Stefan Stojanovic, FTN"
            self.set_y(280)
            self.set_x(20)
            self.set_font('arial', '', 6.0)
            self.cell(0, 0, text, "L")
            

            self.set_y(280)
            self.set_x(-53)
            self.set_font('arial', '', 6.0)
            self.cell(36, 0, "Subject to change and corrections")

        else:

            self.set_y(self.h - self.t_margin)
            self.set_x(20)
            self.set_font('arial', 'B', 6.0)
            self.cell(0, 0, "Author:  ", 'C')
            self.set_x(30)
            self.set_font('arial', '', 6.0)
            self.cell(0, 0, self.author, "L")

            self.set_x(epw / 2)
            self.set_font('arial', 'B', 6.0)
            self.cell(0, 0, "Document generation timestamp:  ", "L")
            self.set_x(epw / 2 + 35)
            self.set_font('arial', '', 6.0)
            self.cell(0, 0, self.date, "L")

            self.set_font('arial', 'B', 6.0)
            self.set_x(-50)
            self.cell(36, 0, u'\u00a9' + " 2019, Stefan Stojanovic, FTN", "L")

    def set_footer_data(self, author, date):
        self.author = author
        self.date = date

def main(parent, pdf_dest, file_name, release_data, swc_data, swc_row, tc_list, sup_ta_list, int_ta_list, rev_list, add_tool_list, add_info_list):

    tc_a_num = 0
    tc_b_num = 0
    tc_c_num = 0
    tc_total_num = len(tc_list)

    a_passed = 0
    b_passed = 0
    c_passed = 0
    tc_total_passed = 0

    a_failed = 0
    b_failed = 0
    c_failed = 0
    tc_total_failed = 0

    a_not_exe = 0
    b_not_exe = 0
    c_not_exe = 0
    tc_total_not_exe = 0

    for tc in tc_list:
        if tc["tcpriority"] == "PRIO_A":
            tc_a_num += 1
            if tc["result"] == "passed":
                a_passed += 1
            elif tc["result"] == "failed":
                a_failed += 1
            elif tc["result"] == "not_executed":
                a_not_exe += 1

        elif tc["tcpriority"] == "PRIO_B":
            tc_b_num += 1
            if tc["result"] == "passed":
                b_passed += 1
            elif tc["result"] == "failed":
                b_failed += 1
            elif tc["result"] == "not_executed":
                b_not_exe += 1

        elif tc["tcpriority"] == "PRIO_C":
            tc_c_num += 1
            if tc["result"] == "passed":
                c_passed += 1
            elif tc["result"] == "failed":
                c_failed += 1
            elif tc["result"] == "not_executed":
                c_not_exe += 1

    tc_total_passed = a_passed + b_passed + c_passed
    tc_total_failed = a_failed + b_failed + c_failed
    tc_total_not_exe = a_not_exe + b_not_exe + c_not_exe
            
    if tc_a_num:
        tc_a_perc = float(tc_a_num) / tc_total_num * 100
    else:
        tc_a_perc = 0

    if tc_b_num:
        tc_b_perc = float(tc_b_num) / tc_total_num * 100
    else:
        tc_b_perc = 0

    if tc_b_num:
        tc_c_perc = float(tc_c_num) / tc_total_num * 100
    else:
        tc_c_perc = 0

    if a_passed:
        a_passed_perc = float(a_passed) / tc_a_num * 100
    else:
        a_passed_perc = 0

    if b_passed:
        b_passed_perc = float(b_passed) / tc_b_num * 100
    else:
        b_passed_perc = 0

    if c_passed:
        c_passed_perc = float(c_passed) / tc_c_num * 100
    else:
        c_passed_perc = 0
 
    if tc_total_passed:
        total_passed_perc = float(tc_total_passed) / tc_total_num * 100
    else:
        total_passed_perc = 0

    if a_failed:
        a_failed_perc = float(a_failed) / tc_a_num * 100
    else:
        a_failed_perc = 0

    if b_failed:
        b_failed_perc = float(b_failed) / tc_b_num * 100
    else:
        b_failed_perc = 0

    if c_failed:
        c_failed_perc = float(c_failed) / tc_c_num * 100
    else:
        c_failed_perc = 0

    if tc_total_failed:
        total_failed_perc = float(tc_total_failed) / tc_total_num * 100
    else:
        total_failed_perc = 0

    if a_not_exe:
        a_not_exe_perc = float(a_not_exe) / tc_a_num * 100
    else:
        a_not_exe_perc = 0

    if b_not_exe:
        b_not_exe_perc = float(b_not_exe) / tc_b_num * 100
    else:
        b_not_exe_perc = 0
    
    if c_not_exe:
        c_not_exe_perc = float(c_not_exe) / tc_c_num * 100
    else:
        c_not_exe_perc = 0

    if tc_total_not_exe:
        total_not_exe_perc = float(tc_total_not_exe) / tc_total_num * 100
    else:
        total_not_exe_perc = 0

    if tc_total_num != 0:
        total_exe = tc_total_num - tc_total_not_exe
        total_exe_perc = 100 - total_not_exe_perc

    else:
        total_exe_perc = 0
        total_not_exe_perc = 0


    if a_not_exe_perc:
        a_exe_perc = 100 - a_not_exe_perc
    else:
        a_exe_perc = 100
    if tc_a_num == 0:
        a_exe_perc = 0

    if b_not_exe_perc:
        b_exe_perc = 100 - b_not_exe_perc
    else:
        b_exe_perc = 100
    if tc_b_num == 0:
        b_exe_perc = 0
        
    if c_not_exe_perc:
        c_exe_perc = 100 - c_not_exe_perc
    else:
        c_exe_perc = 100
    if tc_c_num == 0:
        c_exe_perc = 0
    



    title = "Application Acceptance Test Report"

    pdf = PDF()

    pdf.set_footer_data(swc_data["name"], swc_data["documentcreationdate"])

    pdf.add_page()                                                  # page 1

    pdf.set_margins(20,20,20)
    epw = pdf.w - 2*pdf.l_margin

    pdf.set_xy(36.02, 70.66)
    pdf.set_font('arial', 'B', 20.0)
    pdf.cell(h=0.0, align='L', w=0, txt=title, border=0)

    pdf.ln(25)
    pdf.set_x(36.02)
    pdf.set_font('arial', '', 16.0)
    pdf.cell(h=0.0, align='L', w=0, txt="Release Name:", border=0)
    pdf.set_x(106.02)
    pdf.cell(h=0.0, align='L', w=0, txt=release_data["release"], border=0)

    pdf.ln(25)
    pdf.set_x(36.02)
    pdf.set_font('arial', '', 16.0)
    pdf.cell(h=0.0, align='L', w=0, txt="Project:", border=0)
    pdf.set_x(106.02)
    pdf.cell(h=0.0, align='L', w=0, txt=project_name, border=0)

    pdf.ln(25)
    pdf.set_x(36.02)
    pdf.line(20, 143, 190.0, 143)

    pdf.ln(3)
    pdf.set_x(36.02)
    pdf.set_font('arial', 'B', 12.0)
    pdf.cell(h=0.0, align='L', w=0, txt="Author:", border=0)
    pdf.set_x(106.02)
    pdf.set_font('arial', '', 12.0)
    pdf.cell(h=0.0, align='L', w=0, txt=swc_data["name"], border=0)

    pdf.ln(5)
    pdf.set_x(36.02)
    pdf.set_font('arial', 'B', 12.0)
    pdf.cell(h=0.0, align='L', w=0, txt="Security:", border=0)
    pdf.set_x(106.02)
    pdf.set_font('arial', '', 12.0)
    pdf.cell(h=0.0, align='L', w=0, txt="Confidential", border=0)

    pdf.ln(5)
    pdf.set_x(36.02)
    pdf.set_font('arial', 'B', 12.0)
    pdf.cell(h=0.0, align='L', w=0, txt="Document number:", border=0)
    pdf.set_x(106.02)
    pdf.set_font('arial', '', 12.0)
    pdf.cell(h=0.0, align='L', w=0, txt="-", border=0)

    pdf.ln(5)
    pdf.set_x(36.02)
    pdf.set_font('arial', 'B', 12.0)
    pdf.cell(h=0.0, align='L', w=0, txt="Version:", border=0)
    pdf.set_x(106.02)
    pdf.set_font('arial', '', 12.0)
    pdf.cell(h=0.0, align='L', w=0, txt=swc_data["documentversion"], border=0)

    pdf.ln(5)
    pdf.set_x(36.02)
    pdf.set_font('arial', 'B', 12.0)
    pdf.cell(h=0.0, align='L', w=0, txt="Date:", border=0)
    pdf.set_x(106.02)
    pdf.set_font('arial', '', 12.0)
    pdf.cell(h=0.0, align='L', w=0, txt=swc_data["documentcreationdate"], border=0)

    pdf.ln(5)
    pdf.set_x(36.02)
    pdf.set_font('arial', 'B', 12.0)
    pdf.cell(h=0.0, align='L', w=0, txt="Status:", border=0)
    pdf.set_x(106.02)
    pdf.set_font('arial', '', 12.0)
    pdf.cell(h=0.0, align='L', w=0, txt=swc_data["documentstatus"], border=0)

    pdf.ln(5)
    pdf.set_x(36.02)
    pdf.set_font('arial', 'B', 12.0)
    pdf.cell(h=0.0, align='L', w=0, txt="SW-C:", border=0)
    pdf.set_x(106.02)
    pdf.set_font('arial', '', 12.0)
    pdf.cell(h=0.0, align='L', w=0, txt=swc_row["swc_name"], border=0)

    pdf.ln(3)
    pdf.set_x(36.02)
    pdf.line(20, 184, 190.0, 184)

    pdf.add_page()                                              # TOC PAGE

    # -------------------------------------------------------------------------------------------------------

    pdf.add_page()

    pdf.set_y(45)
    pdf.set_x(20)
    pdf.set_font('arial', 'B', 20.0)
    pdf.cell(h=0, w=0, txt="Revision Chart", align="L", border=0)


    pdf.set_margins(20,20,20)
    epw = pdf.w - 2*pdf.l_margin

    # Set column width to 1/4 of effective page width to distribute content 
    # evenly across table and page
    col_width = epw/4
    th = 12

    # Line break equivalent to 4 lines
    pdf.ln(10)

    pdf.set_fill_color(1, 130, 172)                                                         # PLAVE
    pdf.set_text_color(256,256,256)
    pdf.set_font('arial','B',10.0) 
    pdf.cell(col_width*3/4, th*3/4, "Version", border=1, align="C", fill=1)
    pdf.cell(col_width*3/4, th*3/4, "Date", border=1, align="C", fill=1)
    pdf.cell(col_width*3/4, th*3/4, "Resp. person", border=1, align="C", fill=1)
    pdf.cell(0, th*3/4, "Description", border=1, align="C", fill=1)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('arial','',10.0) 
    pdf.ln(th*3/4)

    for row in rev_list:                                                                    # REFERENCE TABLE

        y = pdf.get_y()
        if y > 260:
            pdf.add_page()
            pdf.ln(8)
            y = pdf.get_y()
        pdf.set_x(20+3*col_width*3/4)
        pdf.multi_cell(0, 5, str(row["Description"]) + "\n", border=1, align="C")        
        cell_w = pdf.get_y() - y
        pdf.set_y(y)
        pdf.set_x(20)
        pdf.cell(col_width*3/4, cell_w, str(row["Document_Version"]), border=1, align="C")
        pdf.set_x(20 + col_width*3/4)
        pdf.cell(col_width*3/4, cell_w, str(row["Date"]), border=1, align="C")
        pdf.set_x(20 + 2*col_width*3/4)
        pdf.cell(col_width*3/4, cell_w, str(row["ResponsiblePerson"]), border=1, align="C")
        
        pdf.ln(cell_w)


    pdf.add_page()                                                                          #
    pdf.set_y(45)
    pdf.set_x(20)
    pdf.set_font('arial', 'B', 20.0)
    pdf.ln(10)
    pdf.cell(0, 0, "1. Application Acceptance Test Result", "L")
    pdf.set_font('arial', '', 10.0)
    pdf.ln(10)
    pdf.cell(0, 0, "This chapter documents the overall test results of the performed Application Acceptance Test.", "L")
    pdf.set_font('arial', '', 14.0)
    pdf.ln(8)
    pdf.cell(0, 0, "1.1 SW-C Overall Test Result & Integration Recommendation", "L")
    pdf.ln(8)

    pdf.set_fill_color(1, 130, 172)
    pdf.set_text_color(256,256,256)
    pdf.set_font('arial','B',10.0) 
    pdf.cell(epw/3, th*3/4, "SWC Name", border=1, align="C", fill=1)
    pdf.cell(epw/3, th*3/4, "Version", border=1, align="C", fill=1)
    pdf.cell(epw/3, th*3/4, "Integration recomm.", border=1, align="C", fill=1)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('arial','',10.0)
    pdf.ln(th*3/4)
    pdf.cell(epw/3, th*3/4, str(swc_row["swc_name"]), border=1, align="C")
    pdf.cell(epw/3, th*3/4, str(release_data["release"]), border=1, align="C")
    pdf.set_font('arial','B',10.0)
    if swc_data["ir_rec_result"].lower() == "passed":
        pdf.set_fill_color(0, 128, 0)
        pdf.cell(epw/3, th*3/4, str(swc_data["ir_rec_result"]), border=1, align="C", fill=1)
    elif swc_data["ir_rec_result"].lower() == "failed":
        pdf.set_fill_color(255, 0, 0)
        pdf.cell(epw/3, th*3/4, str(swc_data["ir_rec_result"]), border=1, align="C", fill=1)
    elif swc_data["ir_rec_result"].lower() == "failed_integrate":
        pdf.set_fill_color(255, 155, 0)
        pdf.cell(epw/3, th*3/4, str(swc_data["ir_rec_result"]), border=1, align="C", fill=1)
    elif swc_data["ir_rec_result"].lower() == "not_executed":
        pdf.set_fill_color(128, 128, 128)
        pdf.cell(epw/3, th*3/4, str(swc_data["ir_rec_result"]), border=1, align="C", fill=1)
    else:
        pdf.cell(epw/3, th*3/4, str(swc_data["ir_rec_result"]), border=1, align="C")

    pdf.ln(12)
    pdf.set_font('arial','B',8.0)
    pdf.cell(0, 0, "Table 1 Application Acceptance Test Result & Integration Recommendation", "L")
    pdf.ln(6)
    pdf.set_fill_color(0, 128, 0)    
    pdf.cell(7, 6, "", fill=1)
    pdf.set_y(111)
    pdf.set_x(28)
    pdf.ln(3)
    pdf.set_fill_color(255, 0, 0)   
    pdf.cell(7, 6, "", fill=1)
    pdf.set_x(28)
    pdf.ln(6)
    pdf.set_fill_color(255, 155, 0)   
    pdf.cell(7, 6, "", fill=1)
    pdf.set_x(28)
    pdf.ln(6)
    pdf.set_fill_color(128, 128, 128)   
    pdf.cell(7, 6, "", fill=1)

    pdf.set_y(111)
    pdf.set_x(28)
    pdf.cell(0, 0, "Passed, integrate all test cases were without errors or only priority C failures occurred")
    pdf.ln(6)
    pdf.set_x(28)
    pdf.cell(0, 0, "Failed, do not integrate at least one priority A failure occurred")
    pdf.ln(6)
    pdf.set_x(28)
    pdf.cell(0, 0, "Failed, but still integrate at least one priority B failure occurred")
    pdf.ln(6)
    pdf.set_x(28)
    pdf.cell(0, 0, "Not Executed")


    pdf.set_font('arial', '', 14.0)
    pdf.ln(14)
    pdf.cell(0, 0, "1.2 Statistics","L")

    pdf.ln(8)
    pdf.set_x(20)

    pdf.set_fill_color(1, 130, 172)                                             # STATISTICS TABELA 
    pdf.set_text_color(256,256,256)
    pdf.set_font('arial','B',10.0) 
    pdf.cell(epw*2/6, th/2, "", border=1, align="C", fill=1)
    pdf.cell(epw*1/6, th/2, "Priority A", border=1, align="C", fill=1)
    pdf.cell(epw*1/6, th/2, "Priority B", border=1, align="C", fill=1)
    pdf.cell(epw*1/6, th/2, "Priority C", border=1, align="C", fill=1)
    pdf.cell(epw*1/6, th/2, "Total", border=1, align="C", fill=1)


    pdf.ln(th/2)
    pdf.cell(epw*2/6, th/2, "Overall number of test cases", border=1, align="L", fill=1)
    pdf.set_text_color(0,0,0)
    pdf.set_font('arial','',10.0) 
    pdf.cell(epw*1/12, th/2, str(tc_a_num), border=1, align="C")
    pdf.cell(epw*1/12, th/2, "100" + "%", border=1, align="C")
    pdf.cell(epw*1/12, th/2, str(tc_b_num), border=1, align="C")
    pdf.cell(epw*1/12, th/2, "100" + "%", border=1, align="C")
    pdf.cell(epw*1/12, th/2, str(tc_c_num), border=1, align="C")
    pdf.cell(epw*1/12, th/2, "100" + "%", border=1, align="C")
    pdf.cell(epw*1/12, th/2, str(len(tc_list)), border=1, align="C")
    pdf.cell(epw*1/12, th/2, "100%", border=1, align="C")

    pdf.ln(th/2)
    pdf.set_text_color(256,256,256)
    pdf.set_font('arial','B',10.0) 
    pdf.cell(epw*2/6, th/2, "Executed test cases", border=1, align="L", fill=1)
    pdf.set_text_color(0,0,0)
    pdf.set_font('arial','',10.0) 
    pdf.cell(epw*1/12, th/2, str(tc_a_num - a_not_exe), border=1, align="C")
    pdf.cell(epw*1/12, th/2, "{0:.2f}".format(a_exe_perc) + "%", border=1, align="C")
    pdf.cell(epw*1/12, th/2, str(tc_b_num - b_not_exe), border=1, align="C")
    pdf.cell(epw*1/12, th/2, "{0:.2f}".format(b_exe_perc) + "%", border=1, align="C")
    pdf.cell(epw*1/12, th/2, str(tc_c_num - c_not_exe), border=1, align="C")
    pdf.cell(epw*1/12, th/2, "{0:.2f}".format(c_exe_perc) + "%", border=1, align="C")
    pdf.cell(epw*1/12, th/2, str(tc_total_num - tc_total_not_exe), border=1, align="C")
    pdf.cell(epw*1/12, th/2, "{0:.2f}".format(total_exe_perc) + "%", border=1, align="C")

    pdf.ln(th/2)
    pdf.set_text_color(256,256,256)
    pdf.set_font('arial','B',10.0) 
    pdf.cell(epw*2/6, th/2, "Not executed test cases", border=1, align="L", fill=1)
    pdf.set_text_color(0,0,0)
    pdf.set_font('arial','',10.0) 
    pdf.cell(epw*1/12, th/2, str(a_not_exe), border=1, align="C")
    pdf.cell(epw*1/12, th/2, "{0:.2f}".format(a_not_exe_perc) + "%", border=1, align="C")
    pdf.cell(epw*1/12, th/2, str(b_not_exe), border=1, align="C")
    pdf.cell(epw*1/12, th/2, "{0:.2f}".format(b_not_exe_perc) + "%", border=1, align="C")
    pdf.cell(epw*1/12, th/2, str(c_not_exe), border=1, align="C")
    pdf.cell(epw*1/12, th/2, "{0:.2f}".format(c_not_exe_perc) + "%", border=1, align="C")
    pdf.cell(epw*1/12, th/2, str(tc_total_not_exe), border=1, align="C")
    pdf.cell(epw*1/12, th/2, "{0:.2f}".format(total_not_exe_perc) + "%", border=1, align="C")

    pdf.ln(th/2)
    pdf.set_text_color(256,256,256)
    pdf.set_font('arial','B',10.0) 
    pdf.cell(epw*2/6, th/2, "Passed test cases", border=1, align="L", fill=1)
    pdf.set_text_color(0,0,0)
    pdf.set_font('arial','',10.0) 
    pdf.cell(epw*1/12, th/2, str(a_passed), border=1, align="C")
    pdf.cell(epw*1/12, th/2, "{0:.2f}".format(a_passed_perc) + "%", border=1, align="C")
    pdf.cell(epw*1/12, th/2, str(b_passed), border=1, align="C")
    pdf.cell(epw*1/12, th/2, "{0:.2f}".format(b_passed_perc) + "%", border=1, align="C")
    pdf.cell(epw*1/12, th/2, str(c_passed), border=1, align="C")
    pdf.cell(epw*1/12, th/2, "{0:.2f}".format(c_passed_perc) + "%", border=1, align="C")
    pdf.cell(epw*1/12, th/2, str(tc_total_passed), border=1, align="C")
    pdf.cell(epw*1/12, th/2, "{0:.2f}".format(total_passed_perc) + "%", border=1, align="C")

    pdf.ln(th/2)
    pdf.set_text_color(256,256,256)
    pdf.set_font('arial','B',10.0) 
    pdf.cell(epw*2/6, th/2, "Failed test cases", border=1, align="L", fill=1)
    pdf.set_text_color(0,0,0)
    pdf.set_font('arial','',10.0) 
    pdf.cell(epw*1/12, th/2, str(a_failed), border=1, align="C")
    pdf.cell(epw*1/12, th/2, "{0:.2f}".format(a_failed_perc) + "%", border=1, align="C")
    pdf.cell(epw*1/12, th/2, str(b_failed), border=1, align="C")
    pdf.cell(epw*1/12, th/2, "{0:.2f}".format(b_failed_perc) + "%", border=1, align="C")
    pdf.cell(epw*1/12, th/2, str(c_failed), border=1, align="C")
    pdf.cell(epw*1/12, th/2, "{0:.2f}".format(c_failed_perc) + "%", border=1, align="C")
    pdf.cell(epw*1/12, th/2, str(tc_total_failed), border=1, align="C")
    pdf.cell(epw*1/12, th/2, "{0:.2f}".format(total_failed_perc) + "%", border=1, align="C")

    pdf.ln(10)
    pdf.set_font('arial','B',8.0)
    pdf.cell(0, 0, "Table 2 Statistics", "L")

# ---------------------------------------------------------------------------------------------------------------------

    pdf.add_page(orientation="L")                                                  # TEST CASE RESULTS TABELA
    pdf.set_margins(20,20,20)
    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/4
    th = 12
    pdf.set_y(45)
    pdf.set_x(20)
    pdf.ln(10)

    pdf.set_font('arial','',14.0)
    pdf.cell(0, 0, "1.3 Test Case Results", "L")
    pdf.ln(8)

    pdf.set_fill_color(1, 130, 172)                                                         # PLAVE
    pdf.set_text_color(256,256,256)
    pdf.set_font('arial','B',10.0) 
    pdf.cell(col_width*3/4*1/6, th*3/4, "ID", border=1, align="C", fill=1)
    pdf.cell(col_width, th*3/4, "Test Case Description", border=1, align="C", fill=1)
    pdf.cell(col_width*1/4, th*3/4, "Priority", border=1, align="C", fill=1)
    pdf.cell(col_width*2/4, th*3/4, "Executed at", border=1, align="C", fill=1)
    pdf.cell(col_width*1/4*3/2, th*3/4, "Result*", border=1, align="C", fill=1)
    pdf.cell(col_width*6/5, th*3/4, "Explanation/Comment", border=1, align="C", fill=1)
    pdf.cell(0, th*3/4, "Bug references", border=1, align="C", fill=1)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('arial','',10.0) 
    pdf.ln(th*3/4)

    for tc in tc_list:


        y = pdf.get_y()
        cell_w = 0

        if (y + 3 * pdf.t_margin) > pdf.h:
            pdf.add_page(orientation="L")
            pdf.ln(8)
            y = pdf.get_y()

            pdf.set_fill_color(1, 130, 172)                                                         # PLAVE
            pdf.set_text_color(256,256,256)
            pdf.set_font('arial','B',10.0) 
            pdf.cell(col_width*3/4*1/6, th*3/4, "ID", border=1, align="C", fill=1)
            pdf.cell(col_width, th*3/4, "Test Case Description", border=1, align="C", fill=1)
            pdf.cell(col_width*1/4, th*3/4, "Priority", border=1, align="C", fill=1)
            pdf.cell(col_width*2/4, th*3/4, "Executed at", border=1, align="C", fill=1)
            pdf.cell(col_width*1/4*3/2, th*3/4, "Result*", border=1, align="C", fill=1)
            pdf.cell(col_width*6/5, th*3/4, "Explanation/Comment", border=1, align="C", fill=1)
            pdf.cell(0, th*3/4, "Bug references", border=1, align="C", fill=1)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('arial','',10.0) 
            pdf.ln(th*3/4)




        if len(tc["Description"]) >= len(tc["Comment"]):
            pdf.set_x(28.031252604166667)
            pdf.multi_cell(col_width, 3, "\n" + tc["Description"] + "\n\n", border=1, align='L')
            cell_w = pdf.get_y() - y
            pdf.set_x(164.56254687499998)
            pdf.set_y(y)
            pdf.multi_cell(col_width*6/5, cell_w / 3, "\n" + tc["Comment"] + "\n\n", border=0, align='L')
            
        else:
            pdf.set_x(164.56254687499998)
            pdf.multi_cell(col_width*6/5, 3, "\n" + tc["Comment"] + "\n\n", border=1, align='L')
            cell_w = pdf.get_y() - y
            pdf.set_y(y)
            pdf.set_x(28.031252604166667)
            pdf.multi_cell(col_width, 3, "\n" + tc["Description"] + "\n\n", border=0, align='L')
            pdf.ln(cell_w)

            
        pdf.set_x(20)
        pdf.set_font('arial','',10.0) 
        pdf.set_y(y)
        pdf.cell(col_width*3/4*1/6, cell_w, tc["ID"], border=1, align="C")
        pdf.set_x(92.28127343749999)
        pdf.cell(col_width*1/4, cell_w, tc["tcpriority"], border=1, align="C")
        pdf.set_x(108.34377864583332)
        pdf.set_font('arial','',8.0)
        pdf.set_y(y)
        pdf.set_x(108.34377864583332)
        pdf.multi_cell(col_width*2/4, cell_w / 3, tc["begindate"] + " - " + tc["begintime"] + "\n - \n" + tc["enddate"] + " - " + tc["endtime"], border=1, align="C")
        

        pdf.set_font('arial','B',10.0)
        if tc["result"] == "passed":
            pdf.set_fill_color(0, 128, 0)
        elif tc["result"] == "failed":
            pdf.set_fill_color(255, 0, 0)
        elif tc["result"] == "not_executed":
            pdf.set_fill_color(128, 128, 128)
        else:
            pdf.set_fill_color(1, 130, 172)

        pdf.set_y(y)
        pdf.set_x(140.46878906249998)
        pdf.cell(col_width*1/4*3/2, cell_w, tc["result"], border=1, align="C", fill=1)
        pdf.set_font('arial','',10.0) 

        if not tc["Comment"]:
            pdf.set_y(y)
            pdf.set_x(164.56254687499998)
            pdf.cell(col_width*6/5, cell_w, tc["Comment"], border=1, align="C")

        pdf.set_y(y)
        pdf.set_x(241.66257187499997)
        pdf.cell(0, cell_w, "No bug references", border=1, align="C")

        




        pdf.ln(cell_w)


#----------------------------------------------------------------------------------



    pdf.set_font('arial','',10.0) 
    pdf.cell(col_width*3/4*1/6, th*2/4, "", border=1, align="C")                    # poslednja vrsta
    pdf.cell(col_width, th*2/4, "", border=1, align="C")
    pdf.cell(col_width*1/4, th*2/4, "", border=1, align="C")
    pdf.cell(col_width*2/4, th*2/4, "Sum**", border=1, align="R")
    pdf.set_fill_color(255, 0, 0)
    pdf.set_font('arial','B',10.0)
    pdf.cell(col_width*1/4*3/2, th*2/4, str(tc_total_failed) + "/" + str(total_exe), border=1, fill=1, align="C")
    pdf.set_font('arial','',10.0)
    pdf.cell(col_width*6/5, th*2/4, "", border=1, align="C")
    pdf.cell(0, th*2/4, "", border=1, align="C")


    pdf.ln(10)
    pdf.set_font('arial','B',8.0)
    pdf.cell(0, 0, "Table 3 Test Case Results", "L")

    pdf.ln(6)
    pdf.cell(0, 0, "*If test case fails, number of errors are shown in this column", "L")
    pdf.ln(6)
    pdf.cell(0, 0, "**Ratio of test cases: failed/executed", "L")
    pdf.ln(6)

    pdf.set_fill_color(0, 128, 0)   
    pdf.cell(7, 6, "", fill=1)
    pdf.ln(3)
    pdf.set_x(28)
    pdf.cell(0, 0, "Passed")
    pdf.set_x(28)
    pdf.ln(3)
    pdf.set_fill_color(255, 0, 0)   
    pdf.cell(7, 6, "", fill=1)
    pdf.ln(3)
    pdf.set_x(28)
    pdf.cell(0, 0, "Failed")
    pdf.set_x(28)
    pdf.ln(3)
    pdf.set_fill_color(128, 128, 128)   
    pdf.cell(7, 6, "", fill=1)
    pdf.ln(3)
    pdf.set_x(28)
    pdf.cell(0, 0, "Not Executed")
    

# ---------------------------------------------------------------------------------------------------------------------

    pdf.add_page(orientation="P")                               # 2 Test Artefact Information

    pdf.set_margins(20,20,20)
    epw = pdf.w - 2*pdf.l_margin

    pdf.set_y(45)
    pdf.set_x(20)
    pdf.set_font('arial', 'B', 20.0)
    pdf.ln(10)
    pdf.cell(0, 0, "2. Test Artefact Information")
    pdf.set_font('arial', '', 10.0)
    pdf.ln(10)
    pdf.cell(0, 0, "The following describes the artefacts which were tested at the integrator and delivered by the SW-C supplier")
    pdf.ln(4)
    pdf.cell(0, 0,  "during Application Acceptance Testing", "L")
    pdf.set_font('arial', '', 14.0)
    pdf.ln(8)
    pdf.cell(0, 0, "2.1 Test Input Artefacts provided by the SWC-Supplier", "L")
    pdf.ln(8)

    pdf.set_x(20)
    pdf.set_fill_color(1, 130, 172)
    pdf.set_text_color(256, 256, 256)
    pdf.set_font('arial','B',10.0) 

    pdf.cell(40, 6, "Name", border=1, align="L",fill=1)
    pdf.set_font('arial','',10.0)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, swc_row["swc_name"], border=1, align="L")
    pdf.ln(6)
    pdf.set_font('arial','B',10.0)
    pdf.set_text_color(256, 256, 256) 
    pdf.cell(40, 6, "Version", border=1, align="L",fill=1)
    pdf.set_font('arial','',10.0)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, release_data["release"], border=1, align="L")
    pdf.ln(6)
    pdf.set_font('arial','B',10.0)
    pdf.set_text_color(256, 256, 256)
    pdf.cell(40, 6, "ASIL Level", border=1, align="L", fill=1)
    pdf.set_font('arial','',10.0)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, swc_row["swc_asil_level"], border=1, align="L")
    pdf.ln(6)
    pdf.set_font('arial','B',10.0)
    pdf.set_text_color(256, 256, 256)
    pdf.cell(40, 6, "Host", border=1, align="L",fill=1)
    pdf.set_font('arial','',10.0)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, swc_row["swc_host"], border=1, align="L")
    pdf.ln(6)
    pdf.set_font('arial','B',10.0)
    pdf.set_text_color(256, 256, 256)
    pdf.cell(40, 6, "Description", border=1, align="L",fill=1)
    pdf.set_font('arial','',10.0)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, swc_row["description"], border=1, align="L")

    pdf.ln(10)
    pdf.set_font('arial','B',8.0)
    pdf.cell(0, 0, "Table 4 Tested SWC", "L")
    pdf.ln(6)


#------------------------------------------------------------------------------------------

    pdf.set_font('arial','B',10.0)
    pdf.set_text_color(256, 256, 256)
    pdf.cell(epw*2/5, 6, "Name", border=1, align="L",fill=1)                         # SUP TA TABELA
    pdf.cell(epw*1/5, 6, "Version", border=1, align="L",fill=1)
    pdf.cell(epw*2/5, 6, "Comment", border=1, align="L",fill=1)
    pdf.ln(6)
    pdf.set_font('arial','',10.0)
    pdf.set_text_color(0, 0, 0)



    for ta in sup_ta_list: 

        y = pdf.get_y()               

        if len(ta["Filename"]) >= len(ta["Comment"]):

            pdf.set_x(20)
            pdf.multi_cell(epw*2/5, 3, "\n" + ta["Filename"] + "\n\n", border=1, align='L')
            cell_w = pdf.get_y() - y
            pdf.set_y(y)
            pdf.set_x(122.00093333333331)
            pdf.cell(epw*2/5, cell_w, "\n" + ta["Comment"] + "\n\n", border=1, align='L')
            pdf.set_y(y)
            pdf.set_x(88.0006222222222)
            pdf.cell(epw*1/5, cell_w,"\n" + ta["Version"] + "\n\n", border=1, align='L')

        else:

            pdf.set_x(122.00093333333331)
            pdf.multi_cell(epw*2/5, 3, "\n" + ta["Comment"] + "\n\n", border=1, align='L')
            cell_w = pdf.get_y() - y
            pdf.set_y(y)
            pdf.set_x(20)
            pdf.multi_cell(epw*2/5, 3, "\n" + ta["Filename"] + "\n\n", border=1, align='L')
            pdf.set_y(y)
            pdf.set_x(88.0006222222222)
            pdf.cell(epw*1/5, cell_w,"\n" + ta["Version"] + "\n\n", border=1, align='L')


        pdf.ln(cell_w)

    pdf.ln(4)
    pdf.set_font('arial','B',8.0)
    pdf.cell(0, 0, "Table 5 Tested Release Content", "L")

#---------------------------------------------------------------------------------

    pdf.ln(10)
    pdf.set_font('arial', '', 14.0)
    pdf.cell(0, 0, "2.2 Test Output Artefacts generated by the Integrator", "L")
    pdf.ln(6)

    pdf.set_font('arial','B',10.0)
    pdf.set_text_color(256, 256, 256)
    pdf.cell(epw*2/5, 6, "Name", border=1, align="L",fill=1)                # INT TA TABELA
    pdf.cell(epw*1/5, 6, "Version", border=1, align="L",fill=1)
    pdf.cell(epw*2/5, 6, "Comment", border=1, align="L",fill=1)
    pdf.ln(6)
    pdf.set_font('arial','',10.0)
    pdf.set_text_color(0, 0, 0)

    y = pdf.get_y()
#    cell_w = pdf.get_y() - y

    for ta in int_ta_list:
        y = pdf.get_y()
        if y > 260:
            pdf.add_page()
            pdf.ln(8)
            y = pdf.get_y()

        if len(ta["Filename"]) >= len(ta["Comment"]):

            pdf.set_x(20)
            pdf.multi_cell(epw*2/5, 3, "\n" + ta["Filename"] + "\n\n", border=1, align='L')
            cell_w = pdf.get_y() - y
            pdf.set_y(y)
            pdf.set_x(122.00093333333331)
            pdf.cell(epw*2/5, cell_w, "\n" + ta["Comment"] + "\n\n", border=1, align='L')
            pdf.set_y(y)
            pdf.set_x(88.0006222222222)
            pdf.cell(epw*1/5, cell_w,"\n" + ta["Version"] + "\n\n", border=1, align='L')

        else:

            pdf.set_x(122.00093333333331)
            pdf.multi_cell(epw*2/5, 3, "\n" + ta["Comment"] + "\n\n", border=1, align='L')
            cell_w = pdf.get_y() - y
            pdf.set_y(y)
            pdf.set_x(20)

            str_w = pdf.get_string_width(ta["Filename"])
            lines_no = str_w / (epw*2/5 - 1)
            lines_no = math.ceil( lines_no )

            if lines_no == 2:
                pdf.multi_cell(epw*2/5, cell_w / 3, ta["Filename"] + "\n\n", border=1, align='L')
            elif lines_no == 3:
                pdf.multi_cell(epw*2/5, cell_w / 3, ta["Filename"] + "\n\n", border=1, align='L')
            elif lines_no == 1:
                pdf.cell(epw*2/5, cell_w,"\n" + ta["Filename"] + "\n\n", border=1, align='L')


            pdf.set_y(y)
            pdf.set_x(88.0006222222222)
            pdf.cell(epw*1/5, cell_w,"\n" + ta["Version"] + "\n\n", border=1, align='L')


        pdf.ln(cell_w)




    pdf.ln(4)
    pdf.set_font('arial','B',8.0)
    pdf.cell(0, 0, "Table 6 Generated Test Artefacts", "L")

#-------------------------------------------------------------------------------------------------------------------------


    pdf.add_page()                                                                  # TEST ENV INFO

    pdf.set_margins(20,20,20)
    epw = pdf.w - 2*pdf.l_margin

    pdf.set_y(45)
    pdf.set_x(20)
    pdf.set_font('arial', 'B', 20.0)
    pdf.ln(10)
    pdf.cell(0, 0, "3 Test Environment Information", "L")
    pdf.set_font('arial', '', 14.0)
    pdf.ln(12)
    pdf.cell(0, 0, "3.1 Test Management", "L")
    pdf.ln(6)

    pdf.set_x(20)
    pdf.set_fill_color(1, 130, 172)
    pdf.set_text_color(256, 256, 256)
    pdf.set_font('arial','B',10.0) 

    pdf.cell(55, 12, "PTC Integrity Baseline Label", border=1, align="L",fill=1)                # TM TABELA
    pdf.set_font('arial','',10.0)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 12, swc_data["ptc_integritybaselinelabel"], border=1, align="L")
    pdf.ln(12)

    pdf.set_font('arial','B',10.0)
    pdf.set_text_color(256, 256, 256) 
    pdf.cell(55, 12, "PTC Integrity Test Session ID", border=1, align="L",fill=1)
    pdf.set_font('arial','',10.0)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 12, swc_data["ptc_integritytestsession_id"], border=1, align="L")
    pdf.ln(12)
    
    pdf.set_font('arial','B',10.0)
    pdf.set_text_color(256, 256, 256)
    pdf.cell(55, 12, "PTC Integration Test Element", border=1, align="L", fill=1)
    pdf.set_font('arial','',10.0)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 12, swc_data["ptc_integrationtestelement"], border=1, align="L")
 

    pdf.ln(16)
    pdf.set_font('arial','B',8.0)
    pdf.cell(0, 0, "Table 7 Test Management Table", "L")
    pdf.ln(12)
    
    pdf.set_font('arial', '', 14.0)
    pdf.cell(0, 0, "3.2 AAT Test Framework Information", "L")
    pdf.ln(10)

    pdf.set_x(20)
    pdf.set_fill_color(1, 130, 172)
    pdf.set_text_color(256, 256, 256)
    pdf.set_font('arial','B',10.0) 

    pdf.cell(55, 12, "AAT Test Framework Version", border=1, align="L",fill=1)            # TEST FW INFO TABELA
    pdf.set_font('arial','',10.0)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 12, swc_data["testframeworkversion"], border=1, align="L")
    pdf.ln(12)
    pdf.set_font('arial','B',10.0)
    pdf.set_text_color(256, 256, 256) 
    pdf.cell(55, 12, "Change Description", border=1, align="L",fill=1)
    pdf.set_font('arial','',10.0)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 12, swc_data["changedescription"], border=1, align="L")
    pdf.ln(12)
    pdf.set_font('arial','B',10.0)
    pdf.set_text_color(256, 256, 256)
    pdf.cell(55, 12, "Effects Of Change", border=1, align="L", fill=1)
    pdf.set_font('arial','',10.0)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 12, swc_data["effects"], border=1, align="L")

    pdf.ln(16)
    pdf.set_font('arial','B',8.0)
    pdf.cell(0, 0, "Table 8 AAT Test Framework Information", "L")

    pdf.ln(10)
    pdf.set_font('arial', '', 14.0)
    pdf.cell(0, 0, "3.3 Additional Software Tools", "L")

    pdf.ln(8)
    pdf.set_font('arial', '', 12.0)

    if len(add_tool_list) == 0:
        pdf.cell(0, 0, "{NO DATA}", "L")

    else:

        for tool in add_tool_list:
            pdf.set_font('arial','B',10.0)
            pdf.set_text_color(256, 256, 256) 
            pdf.cell(40, 6, "Software Name", border=1, align="L",fill=1)                # TM TABELA
            pdf.set_font('arial','',10.0)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 6, tool["SoftwareName"], border=1, align="L")
            pdf.ln(6)
            pdf.set_font('arial','B',10.0)
            pdf.set_text_color(256, 256, 256) 
            pdf.cell(40, 6, "Version", border=1, align="L",fill=1)
            pdf.set_font('arial','',10.0)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 6, tool["Version"], border=1, align="L")
            pdf.ln(6)
            pdf.set_font('arial','B',10.0)
            pdf.set_text_color(256, 256, 256)
            pdf.cell(40, 6, "Description", border=1, align="L", fill=1)
            pdf.set_font('arial','',10.0)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 6, tool["Description"], border=1, align="L")

    pdf.ln(16)
    pdf.set_font('arial', '', 14.0)
    pdf.cell(0, 0, "3.4 Test PC Software Image", "L")
    pdf.ln(8)
    pdf.set_font('arial', '', 12.0)

    if swc_data["testpcswimage"]:
        pdf.cell(0, 0, swc_data["testpcswimage"], "L")
    else:
        pdf.cell(0, 0, "{NO DATA}", "L")

    pdf.add_page()

    pdf.set_margins(20,20,20)
    epw = pdf.w - 2*pdf.l_margin

    pdf.set_y(45)
    pdf.set_x(20)
    pdf.set_font('arial', 'B', 20.0)
    pdf.ln(10)
    pdf.cell(0, 0, "Guidelines", "L")
    pdf.set_font('arial', '', 10.0)
    pdf.ln(12)

    if len(add_info_list) == 0 or all(x == None for x in add_info_list):

        pdf.cell(0, 0, "There are no guidelines.", "L")
        pdf.ln(6)

    else:
        y = pdf.get_y()
        for info in add_info_list:
            y = pdf.get_y()
            pdf.multi_cell(0, 4, "\t* " + info, border=0, align="L")
            cell_w = pdf.get_y() - y
            pdf.ln(6)



    if not pdf_dest.endswith(".pdf"):
        file_name = file_name[:-4] + ".pdf"
        pdf_dest = os.path.join(pdf_dest, file_name)

    pdf.output(pdf_dest, 'F')