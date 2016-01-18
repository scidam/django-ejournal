from appconf import AppConf


class AcmeAppConf(AppConf):
    # allowed keywords field length 
    MAX_KEYWORDS_LENGTH = 600
    # allowed length of the abstrat
    MAX_ABSTRACT_LENGTH = 1000

    class Meta:
        prefix = 'ejournal'