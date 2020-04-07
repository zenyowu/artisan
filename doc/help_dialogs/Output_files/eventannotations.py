
import prettytable
import re
from PyQt5.QtWidgets import QApplication
def u(x):
    return str(x)
if True:  #here just to achieve the indent
    if True:
# ----- Cut below ---------------------------------------------

        # autogenerated help pasted below

        newline = "\n"  #@UnusedVariable
        helpstr = ""
        helpstr += "<head><style>"
        helpstr += "td, th {border: 1px solid #ddd;  padding: 6px;}"
        helpstr += "th {padding-top: 6px;padding-bottom: 6px;text-align: left;background-color: #0C6AA6; color: white;}"
        helpstr += "</style></head>"
        helpstr += "<body>"
        helpstr += "<b>" + u(QApplication.translate('HelpDlg','EVENT ANNOTATIONS',None)) + "</b>"
        tbl_Annotations = prettytable.PrettyTable()
        tbl_Annotations.field_names = [u(QApplication.translate('HelpDlg','Prefix Field',None)),u(QApplication.translate('HelpDlg','Source',None)),u(QApplication.translate('HelpDlg','Example',None))]
        tbl_Annotations.add_row(['~E',u(QApplication.translate('HelpDlg','The value of Event',None)),60])
        tbl_Annotations.add_row(['~Y1',u(QApplication.translate('HelpDlg','ET value',None)),420])
        tbl_Annotations.add_row(['~Y2',u(QApplication.translate('HelpDlg','BT value',None)),372])
        tbl_Annotations.add_row(['~descr',u(QApplication.translate('HelpDlg','The Description field of the Event',None)),u(QApplication.translate('HelpDlg','Gas 10',None))])
        tbl_Annotations.add_row(['~type',u(QApplication.translate('HelpDlg','The Type field of the Event',None)),u(QApplication.translate('HelpDlg','Power',None))])
        tbl_Annotations.add_row(['~sldrunit',u(QApplication.translate('HelpDlg','The value of the Slider Unit for this Event',None)),u(QApplication.translate('HelpDlg','kPa',None))])
        tbl_Annotations.add_row(['~dCHARGE',u(QApplication.translate('HelpDlg','Number of seconds since CHARGE',None)),522])
        tbl_Annotations.add_row(['~dFCs',u(QApplication.translate('HelpDlg','Number of seconds after FCs \nBest used inside double quotes (see notes below) \nDisplays &#39;*&#39; prior to FCs',None)),47])
        tbl_Annotations.add_row(['~preFCs',u(QApplication.translate('HelpDlg','Number of seconds before FCs \nBest used inside single quotes or back ticks (see notes below) \nDisplays &#39;*&#39; after FCs',None)),50])
        tbl_Annotations.add_row(['~DTR',u(QApplication.translate('HelpDlg','Development time ratio. Note: DTR=0 before FCs \n100*(t{Event}-t{FCs})/(t{FCs}-t{CHARGE})',None)),12])
        tbl_Annotations.add_row(['~deg',u(QApplication.translate('HelpDlg','The degree symbol',None)),'\u00b0'])
        tbl_Annotations.add_row(['~mode',u(QApplication.translate('HelpDlg','Temperature mode (&#39;C&#39; or &#39;F&#39;)',None)),'F'])
        tbl_Annotations.add_row(['~degmode',u(QApplication.translate('HelpDlg','Degree symbol with Temperature mode',None)),'\u00b0C'])
        tbl_Annotations.add_row(['~quot',u(QApplication.translate('HelpDlg','Quote symbol',None)),'"'])
        tbl_Annotations.add_row(['~squot',u(QApplication.translate('HelpDlg','Single quote symbol',None)),'&#39;'])
        helpstr += tbl_Annotations.get_html_string(attributes={"width":"100%","border":"1","padding":"1","border-collapse":"collapse"})
        helpstr += "<br/><br/><b>" + u(QApplication.translate('HelpDlg','EXAMPLES',None)) + "</b>"
        tbl_Examplestop = prettytable.PrettyTable()
        tbl_Examplestop.header = False
        tbl_Examplestop.add_row([u(QApplication.translate('HelpDlg','Assumptions:  The event value is 50.  In the case of Gas the value 50 corresponds to either 5.0kPh or 50%.  \nFor a sensory milestone (see notes above) the value 50 corresponds to the "Hay" aroma. ',None))])
        helpstr += tbl_Examplestop.get_html_string(attributes={"width":"100%","border":"1","padding":"1","border-collapse":"collapse"})
        tbl_Examples = prettytable.PrettyTable()
        tbl_Examples.field_names = [u(QApplication.translate('HelpDlg','Annotation Field',None)),u(QApplication.translate('HelpDlg','Displays',None))]
        tbl_Examples.add_row([u(QApplication.translate('HelpDlg','Gas ~E @~Y2~degmode',None)),u(QApplication.translate('HelpDlg','Gas 50 @340\u00b0F',None))])
        tbl_Examples.add_row([u(QApplication.translate('HelpDlg','Gas ~E% @~Y2~mode',None)),u(QApplication.translate('HelpDlg','Gas 50% @340F',None))])
        tbl_Examples.add_row([u(QApplication.translate('HelpDlg','Gas ~E/10kPh @~Y2~mode',None)),u(QApplication.translate('HelpDlg','Gas 5.0kPh @340F',None))])
        tbl_Examples.add_row([u(QApplication.translate('HelpDlg','Gas ~E% &#39;@~Y2 ~degmode&#39;"@~DTR% DTR"',None)),u(QApplication.translate('HelpDlg','Before FCs:\nGas 50% @340 \u00b0F\n\nAfter FCs:\nGas 50% @12% DTR',None))])
        tbl_Examples.add_row([u(QApplication.translate('HelpDlg','Gas ~E% &#39;@~Y2 ~degmode`, ~preFCs sec before FCs`&#39;"@~DTR% DTR"',None)),u(QApplication.translate('HelpDlg','More than 90 seconds before FCs:\nGas 50% @340 \u00b0F\n\nLess than 90 seconds before FCs:\nGas 50% @340 \u00b0F, 50 sec before FCs \n\nAfter FCs:\nGas 50% @12% DTR',None))])
        tbl_Examples.add_row([u(QApplication.translate('HelpDlg','{20Fresh Cut Grass|50Hay|80Baking Bread|100A Point} @~Y2~degmode',None)),u(QApplication.translate('HelpDlg','Hay @340 \u00b0F',None))])
        helpstr += tbl_Examples.get_html_string(attributes={"width":"100%","border":"1","padding":"1","border-collapse":"collapse"})
        helpstr += "<br/><br/><b>" + u(QApplication.translate('HelpDlg','NOTES:',None)) + "</b>"
        tbl_Notes = prettytable.PrettyTable()
        tbl_Notes.field_names = ['&#160;']
        tbl_Notes.add_row([u(QApplication.translate('HelpDlg','Event annotations apply only for &#39;Step&#39; and &#39;Step+&#39; Events settings',None))])
        tbl_Notes.add_row([u(QApplication.translate('HelpDlg','Anything between double quotes " will show only after FCs. Example: "~E1 @~DTR%"',None))])
        tbl_Notes.add_row([u(QApplication.translate('HelpDlg','Anything between single quotes &#39; will show only before FCs. Example: &#39;~E1 @~degmode&#39;',None))])
        tbl_Notes.add_row([u(QApplication.translate('HelpDlg','Anything between back ticks ` will show only within 90 seconds before FCs. Example: `~E1 `FCs~dFCs sec`',None))])
        tbl_Notes.add_row([u(QApplication.translate('HelpDlg','When combining back ticks with single or double quotes the back ticks should be inside the quotes.',None))])
        tbl_Notes.add_row([u(QApplication.translate('HelpDlg','Background event annotations can be seen during a roast when &#39;Annotations&#39; is checked in the Profile Background window.',None))])
        tbl_Notes.add_row([u(QApplication.translate('HelpDlg','Simple scaling of the event value is possible. Use a single math operator (&#39;*&#39;, &#39;/&#39;, &#39;+&#39; or &#39;-&#39;) immediately following the field name "E". For example: \n&#39;~E/10&#39; will divide the E value by 10. \n&#39;~E+5&#39; adds 5 to the the value of E.',None))])
        tbl_Notes.add_row([u(QApplication.translate('HelpDlg','Another style of annotations allows to replace an event&#39;s numeric value with a text string, known as a nominal value. One example where this can be useful is when an event is used to record sensory milestones. The value 20 might be used for &#39;Fresh Cut Grass&#39; aroma, 50 for &#39;Hay&#39;, 80 for &#39;Baking Bread&#39;, and 100 to represent the &#39;A Point&#39;.  \n\nThis form of annotation must be enclosed in curly brackets &#39;{}&#39;. Entries are numeric values immediately followed by their nominal representation text.  Entries are separated by the vertical bar &#39;|&#39;. The following Annotation string implements this example.   \n{~E|20Fresh Cut Grass|50Hay|80Baking Bread|100A Point} \n\nNote that if the event value  does not match any value in the Annotation definition a blank string will be returned.  In the example above an event value of 30 will return a blank string.  The easiest way to ensure these values match is to use Custom Buttons to for the Event.',None))])
        helpstr += tbl_Notes.get_html_string(attributes={"width":"100%","border":"1","padding":"1","border-collapse":"collapse"})
        helpstr += "</body>"
        helpstr = re.sub(r"&amp;", r"&",helpstr)

        # autogenerated help pasted above

# ----- Cut above ---------------------------------------------
outfile = open('../output_files/eventannotations.html','w')
outfile.write(helpstr)
outfile.close()
outfile = open('../output_files/help.html','w')
outfile.write(helpstr)
outfile.close()