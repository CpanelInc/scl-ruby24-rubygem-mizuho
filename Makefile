OBS_PROJECT := EA4
OBS_PACKAGE := scl-ruby24-rubygem-mizuho
DISABLE_BUILD := arch=i586 repository=CentOS_8 repository=CentOS_9
include $(EATOOLS_BUILD_DIR)obs.mk
