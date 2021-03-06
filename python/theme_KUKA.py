from update_themes import *

#************************************  KUKA language   **************************************
repository = {}
#------------------------------------

# Comment
repo_begin_end(repository, ";", r'(?=\n)', name_comment, "comment")

# String
repo_begin_end(repository, r'"', r'"', name_string, "string")

# Declaration of external calls
repo_begin_end(repository, r'EXT', r'( )', name_string, "fcn-call")

# Special header comment match
match = r'\&.+'
repo_match(repository, match, name_numeric, "numbers")

#Numeric constants
match = r'\-?\d+(\.\d+)?'
repo_match(repository, match, name_numeric, "numbers")

# 
match = "REPEAT FOR WHILE LOOP DEF IF THEN ELSE SWITCH LOOP"
match += " UNTIL ENDFOR ENDWHILE ENDLOOP END ENDIF ENDSWITCH ENDLOOP"
match += " DEF INI END ENDFCT ENDDAT WAIT GOTO CASE DEFAULT DEFFCT ENDFCT SEC"
match += " DEFDAT PUBLIC ENDDAT RETURN EXIT HALT"
match += " INTERRUPT WHEN DO BRAKE RESUME ENABLE DISABLE"

# Frame Coordinates
match += " X Y Z A B C E1 E2 E3 E4 E5 E6"
match += " A1 A2 A3 A4 A5 A6"
repo_match(repository, match, name_control, "control")


match = "PTP LIN CIRC SPTP SLIN"
repo_match(repository, match, name_movements, "movement")
match = r'\w+\(\)' #regex for subroutine call ex Subprogram()
repo_match(repository, match, name_movements, "movement")


match = "BAS SET_KRLMSG EXISTS_KRLMSG CLEAR_KRLMSG TRIGGER DISTANCE SET_KRLDLG EXISTS_KRLDLG StrClear LOOP_MSG LOOP_CONT"
repo_match(repository, match, name_builtInFcn, "built-in-fcn")
#LOOP_MSG and LOOP_CONT need special cases because they are used like variables sometimes.
match = r"\$LOOP_MSG"
repo_match(repository, match, name_builtInFcn, "built-in-fcn")
match = r"\$LOOP_CONT"
repo_match(repository, match, name_builtInFcn, "built-in-fcn")


match_type = "built-in-types"
match = "DECL GLOBAL CONST INT REAL BOOL CHAR PRIO FRAME POS E6POS AXIS E6AXIS"
repo_match(repository, match, name_builtInTypes, "built-in-types")

match = "BASE_DATA TOOL_DATA ADVANCE TOOL BASE AXIS_ACT ACT_EX_AX EX_AX_DATA"
match += " INITMOV BWDSTART INITMOV VEL_PTP ACC_PTP"
match += " ANOUT OUT IN ANIN ON OFF TRUE FALSE"
match += " ACC VEL APO C_DIS C_PTP"
match += " TIMER_STOP TIMER_FLAG TIMER"
match += " VEL.CP ACT_BASE APO.CPTP APO.CDIS"
match += " VEL.ORI1 VEL.ORI2 ACC.ORI1 ACC.ORI2"

# KUKA dollar sign does not work
#match = match.replace('$','$$')
repo_match(repository, match, name_builtInVar, "built-in-var")

#Kuka variables can also be accessed with a # or a $
for word in match.split():
    matchKeyWord1 = '\\#'
    matchKeyWord1 += word
    matchKeyWord2 = '\\$'
    matchKeyWord2 += word
    repo_match(repository, matchKeyWord1, name_builtInVar, "built-in-var")
    repo_match(repository, matchKeyWord2, name_builtInVar, "built-in-var")

#matchlist = r"$ACC $ADVANCE $TOOL $BASE $AXIS_ACT $ACT_EX_AX $EX_AX_DATA #INITMOV $ACC $VEL $APO"
#matchlist += r" $TIMER_STOP $TIMER_FLAG $TIMER $VEL.CP $ACT_BASE $APO.CPTP $APO.CDIS"
#matchlist += r" $VEL.ORI1 $VEL.ORI2 $ACC.ORI1 $ACC.ORI2"

#for word in matchlist.split():
#    match = '\\'
#    match += word
#    #repo_match(repository, match, name_builtInVar, "built-in-var")


match_type = "operator"
match = r'\\b= < > + - , ( ) { } [ ]\\b'
repo_match(repository, match, name_operator, "operator")



config_i = dict(default_config)
language_i = {}
language_i["id"] = "KUKA"
language_i["aliases"]     = "KUKA KRC KRC2 KRC4 SRC DAT".split(" ")
language_i["extensions"]  = ".src .dat".split(" ")
language_i["configuration"] = getFileConfig(language_i["id"])
config_i["comments"] = {"lineComment": ";" }
config_i["folding"] = {
        "markers": {
            "start": r'^\s*;FOLD',
            "end": r'^\s*;ENDFOLD'
        }
    }


print("Updating syntax...")
update_syntax(language_i["id"], repository)

print("Updating configuration...")
update_config(language_i["id"], config_i)

print("Done")

    
