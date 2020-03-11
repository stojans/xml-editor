class ReleaseData():
    def __init__(self):
        self.release = ""
        self.platform = ""

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, item, value):
        self.__dict__[item] = value


class SWCData():
    def __init__(self):
        self.comment = ""
        self.documentid = ""
        self.documentversion = ""
        self.documentstatus = ""
        self.documentdescription = ""
        self.name = ""
        self.company = ""
        self.address = ""
        self.email = ""
        self.tel = ""
        self.documentcreationdate = ""
        self.overallresult = ""
        self.ir_rec_result = ""
        self.ptc_integritybaselinelabel = ""
        self.ptc_integritytestsession_id = ""
        self.ptc_integrationtestelement = ""
        self.used_aitfw_providedbyintegrator = ""
        self.testframeworkversion = ""
        self.changedescription = ""
        self.effects = ""
        self.testpcswimage = ""
        self.allreportedviolationjustified = ""
        self.requiredlevel = ""
        self.advisorylevel = ""

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, item, value):
        self.__dict__[item] = value


class SWC:
    def __init__(self):
        self.swc_name = ""
        self.releasekind = ""
        self.releaseversion = ""
        self.ifset_variant = ""
        self.ifset_major = ""
        self.ifset_minor = ""
        self.platform_major = ""
        self.platform_minor = ""
        self.platform_buildtimestamp = ""
        self.swc_major = ""
        self.swc_minor = ""
        self.swc_buildtimestamp = ""
        self.swc_asil_level = ""
        self.swc_host = ""
        self.description = ""

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, item, value):
        self.__dict__[item] = value


class TestCase:
    def __init__(self):
        self.Name = ""
        self.Description = ""
        self.Comment = ""
        self.Explanation = ""
        self.begindate = ""
        self.begintime = ""
        self.enddate = ""
        self.endtime = ""
        self.Ratio_A = ""
        self.Ratio_B = ""
        self.tcpriority = ""
        self.result = ""
        self.TestCaseNumber = ""
        self.ID = ""
        self.bug_ref_list = []


    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, item, value):
        self.__dict__[item] = value


class TestCaseTable:
    def __init__(self):
        self.ref = ""
        self.name = ""
        self.header = []
        self.row_list = []

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, item, value):
        self.__dict__[item] = value


class TableCell:
    def __init__(self):
        self.align = ""
        self.width = ""
        self.value = ""

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, item, value):
        self.__dict__[item] = value


class Acronym:
    def __init__(self):
        self.name = ""
        self.Description = ""

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, item, value):
        self.__dict__[item] = value


class TestArtefact:
    def __init__(self):
        self.Filename = ""
        self.Version = ""
        self.Comment = ""

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, item, value):
        self.__dict__[item] = value


class Revision:
    def __init__(self):
        self.Date = ""
        self.Document_Version = ""
        self.Description = ""
        self.ResponsiblePerson = ""

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, item, value):
        self.__dict__[item] = value


class Reference:
    def __init__(self):
        self.name = ""
        self.Description = ""

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, item, value):
        self.__dict__[item] = value


class Limitation:
    def __init__(self):
        self.CompanyIssueIdentifier = ""
        self.Description = ""

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, item, value):
        self.__dict__[item] = value


class AdditionalTool:
    def __init__(self):
        self.SoftwareName = ""
        self.Version = ""
        self.Description = ""

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, item, value):
        self.__dict__[item] = value


class SupAddInfo:
    def __init__(self):
        self.Additional_Data = ""

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, item, value):
        self.__dict__[item] = value

