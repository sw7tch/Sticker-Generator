#!/usr/bin/env python

###################################################
#  sticker-generator.py
#  Author:  nathan
#  Date:    26/04/2018
#  Brief:   a python program to scrape a jobs txt file, save
#           all the parts into arrays and then generate a pdf file
#           that is to be printed on the AVERY *(L7157REV)* sticker labels
###################################################


import labels
from reportlab.graphics import shapes
from collections import namedtuple
import  os.path
import sys
import re

print
print " N4tH4N's                          "
print "          __  .__        __                 "
print "  _______/  |_|__| ____ |  | __ ___________ "
print " /  ___/\   __\  |/ ___\|  |/ // __ \_  __ \\"
print " \___ \  |  | |  \  \___|    <\  ___/|  | \/"
print "/____  > |__| |__|\___  >__|_ \\\\___  >__|   "
print "     \/               \/     \/    \/      __                       "
print "   ____   ____   ____   ________________ _/  |_  ___________ "
print "  / ___\_/ __ \ /    \_/ __ \_  __ \__  \\\\   __\/  _ \_  __ \\"
print " / /_/  >  ___/|   |  \  ___/|  | \// __ \|  | (  <_> )  | \/"
print " \___  / \___  >___|  /\___  >__|  (____  /__|  \____/|__|   "
print "/_____/      \/     \/     \/           \/                   "
print
print " |-------------------------------|"
print " |   1) Print Labels             |"
print " |   2) Test Mode                |"
print " |-------------------------------|"
print
mode = raw_input("# Please enter an option number: ")

print_labels = False
test_mode = False

if mode == "1":
    print_labels = True
elif mode == "2":
    test_mode = True


###########################################################################
############    Defining and opening the .txt file to work on    ##########
###########################################################################

# prompting the user for the job number
user_input = raw_input("##  Enter the Job Number: ")
# combining the 'user_input' string with the extension '.txt'
input_file = user_input + ".txt"

if os.path.isfile(input_file):
    txt_file = open(input_file, "r")
    contents = txt_file.read()
    txt_file_lines = contents.splitlines()  # have to do this because python adds extra line breaks
    txt_file.close()
else:
    print
    print "   WhAt??!?!?"
    print "   That file doesn't seem to exist..."
    print "   Are you sure you exported the job from iTMS?"
    print
    sys.exit(-1)

print
print

##################################################################
#######   Finding all the lines that have * - number *    ########
##################################################################

ticket_line_number_array = []
customer = ""
job_number = ""

counter = 1
for line in txt_file_lines:
    # finding the start of each job ticket
    # using regex to find lines that contain for e.g. *88931-1*
    if re.match("^\*.*-[0-9]*\*", line) is not None:
        ticket_line_number_array.append(counter)
    # the customers name is always on line 2
    if counter == 2:
        customer = line
    # the fist job ticket start on line 3
    elif counter == 3:
        job_number = line
        # removing the '*' from the job number
        job_number = job_number.replace("*", "")
        # removing everything after the '-' to leave only the job number left
        job_number = re.sub("-.*$", "", job_number)
    counter += 1

array_length = len(ticket_line_number_array)

print "Customer =", customer
print "Job Number =", job_number
print "The number of parts in the job =", array_length


###########################################################
############  Defining the customer variable  #############
###########################################################

if customer == "G H VARLEY - TOMAGO (McINTYRE ROAD - DEFENCE)":
    customer = "VARLEY_TOMAGO_DEFENCE"


##################################################################
############  Creating the Client Part Number Array  #############
##################################################################

client_part_number_array = []

for i in ticket_line_number_array:
    lines_ahead_array = []
    for counter, line in enumerate(txt_file_lines, 1):
        if counter < ( i + 12 ) and counter > ( i + 2 ):
            lines_ahead_array.append(line)

    if customer == "VARLEY":
        for j, item in enumerate(lines_ahead_array):
            if j < 3 and item.find("Issue Date") >= 0:
                # going back by one line and splitting the string by {TAB}
                client_part_number_array.append(lines_ahead_array[j-1].split("\t")[1])
            elif j > 4 and item.find("Issue Date") >= 0:
                # going back by two lines
                client_part_number_array.append(lines_ahead_array[j-2])

    # TRITIUM and VARLEY TOMAGO DEFENCE get the client part number from the line below 'Part Description'
    # once it finds 'Part Description', it will look one line ahead, then split the line at the first space " "
    # and keep the first string that is there
    if customer == "TRITIUM" or customer == "VARLEY_TOMAGO_DEFENCE":
        for j , item in enumerate(lines_ahead_array):
            # tritium has their client part number in the part description field
            # looking for "Part Description" then jumping one line ahead
            if item.find("Part Description") >= 0:
                # adding "CUSTOMER LABELS" if the next line contains "CUSTOMER"
                if lines_ahead_array[j+1].split(" ")[0] == "CUSTOMER":
                    client_part_number_array.append("CUSTOMER-LABELS")
                else:
                    # one line down from "Part Description" and splitting the string with the first white space
                    client_part_number_array.append(lines_ahead_array[j+1].split(" ")[0])


###################################################
############  Creating the Qty Array  #############
###################################################

qty_array = []

for i in ticket_line_number_array:
    lines_ahead_array = []
    for counter, line in enumerate(txt_file_lines, 1):
        if counter < ( i + 15 ) and counter > ( i + 6 ):
            lines_ahead_array.append(line)

    for j, item in enumerate(lines_ahead_array):
        if item.find("Order Qty") >= 0:
            qty_array.append(lines_ahead_array[j+1].split("\t")[4])


#################################################################
#####  Arrays and Variables for VARLEY TOMAGO DEFENCE only  #####
#################################################################

if customer == "VARLEY_TOMAGO_DEFENCE":

    # starting to find the Order Number
    for i in enumerate(ticket_line_number_array):
        # only searching the first element in the ticket_line_number_array
        if i < 1:
            lines_ahead_array = []
            for counter, line in enumerate(txt_file_lines, 1):
                # only reading in lines 5 to 14 from the txt file into the array
                if counter > 4 and counter < 15:
                    lines_ahead_array.append(line)

    # searching each line for the word "Order No"
    for j, item in enumerate(lines_ahead_array):
        if item.find("Order No") >= 0:
            # the Order Number is one line below, and the third tab over
            order_no = lines_ahead_array[j+1].split("\t")[2]

    print "Order Number =", order_no
    print
    print

    # Getting the Kit Number from the USER, this changes with each order
    print "*  VARLEY - TOMAGO DEFENCE, require a kit number to be printed on each label."
    print "*  The kit number should be written on the 'CUSTOMER-LABELS' ticket."
    print "*  If there is no kit number on that ticket, see Jamie."
    print
    kit_number = raw_input("##  Please enter the Kit Number for this job: ")

    # Creating the Revision Array

    revision_array = []

    for i in ticket_line_number_array:
        lines_ahead_array = []
        for counter, line in enumerate(txt_file_lines, 1):
            if counter < ( i +  14 ) and counter > ( i + 3 ):
                lines_ahead_array.append(line)

        for j, item in enumerate(lines_ahead_array):
            if item.find("Revision") >= 0:
                # added the 'try' because you will get an IndexError if there is no revision in iTMS
                try:
                    # the revision will be one line down and the 5th tab over
                    revision_array.append(lines_ahead_array[j+1].split("\t")[4])
                except IndexError:
                    # adding an empty string to the array if there is no revision
                    revision_array.append(" ")


###############################################################
##############   Starting to print the labels   ###############
###############################################################

if print_labels == True:
        # Create an A4 portrait (210mm x 297mm) sheet with 3 columns and 11 rows of
        # labels. Each label is 64mm x 24.3mm with a 2mm rounded corner. The margins are
        # automatically calculated.
        # left_margin is 7, top_margin is 15, column_gap is 2.7
        specs = labels.Specification(210, 297, 3, 11, 63.6, 24.1, corner_radius=2,
                                     left_padding=3, bottom_padding=1.5, left_margin=6.5, top_margin=16,
                                     row_gap=0.5, column_gap=2.7)


        Part = namedtuple(
            'Part',
            ['gci_group', 'customer', 'division_kit_number', 'part_number', 'rev_qty'])

        def draw_part(label, width, height, part):
            lines = [
                part.rev_qty,
                part.part_number,
                part.division_kit_number,
                part.customer,
                part.gci_group
            ]

            group = shapes.Group()
            x, y = 0, 0

            for line in lines:
                if not line:
                    continue
                shape = shapes.String(x, y, line, textAnchor="start", fontName="Helvetica", fontSize=6)
                # _, _, _, y = shape.getBounds()
                y += 11
                group.add(shape)
            # _, _, lx, ly = label.getBounds()
            # _, _, gx, gy = group.getBounds()

            label.add(group)

        sheet = labels.Sheet(specs, draw_part, border=False)


        # counter = 1
        # while counter <= 10:
        #     part = Part("GCI GROUP" + (" "*55) + job_number + "-" + str(counter),
        #                 "CUSTOMER: VARLEY - TOMAGO",
        #                 "DIVISION: DEFENCE & AERO" + (" "*10) + "KIT NUMBER: " + kit_no,
        #                 "PART NUMBER: " + str(counter),
        #                 "REV: " + str(counter) + (" "*25) + "QTY: " + str(counter))
        #     sheet.add_label(part)
        #     counter += 1

        label_counter = 1
        for i, item in enumerate(ticket_line_number_array):
            counter = 1
            while counter <= int(qty_array[i]):
                # print "Ticket Number: " + str(job_number) + "-" + str(i + 1)
                # print "Part Number: " + str(client_part_number_array[i])
                # print "Revision: " + str(revision_array[i])
                # print "Quantity: " + str(counter) + " of " + str(qty_array[i])
                # print

                part = Part("GCI GROUP" + (" "*55) + str(job_number) + "-" + str(i + 1),
                            "CUSTOMER:  VARLEY - TOMAGO",
                            "DIVISION:  DEFENCE & AERO" + (" " * 10) + "KIT NUMBER:  " + kit_number,
                            "PART NUMBER:  " + str(client_part_number_array[i]),
                            "REV:  " + str(revision_array[i]) + (" "*25) + "QTY:  " + str(counter) + "  of  " + str(qty_array[i])
                            )

                print "* generating label number: " + str(label_counter) + " *"

                sheet.add_label(part)
                counter += 1

                label_counter +=1

        print
        print "Saving the pdf as " + str(job_number) + ".pdf"
        print

        pdf_name = job_number + '.pdf'
        sheet.save(pdf_name)


#################################
##########  Test Mode  ##########
#################################

if test_mode == True:

    print
    print "****  Test Mode  ****"
    print "Looping through and testing all of the arrays."
    print

    for i, item in enumerate(ticket_line_number_array):
        print "Ticket Number:", job_number+"-"+str(i+1)
        print "Part Number: ", client_part_number_array[i]
        if customer == "VARLEY_TOMAGO_DEFENCE":
            print "Revision:", revision_array[i]
        print "Quantity:", qty_array[i]
        print

print "Generating the labels is complete."
print "Open the PDF generated and print this onto the AVERY 'L7175REV' Labels"
print "Make sure you printer is printing at 'Actual Size' and not scaling the pdf :D"
print "If in doubt ask Nathan"
print
