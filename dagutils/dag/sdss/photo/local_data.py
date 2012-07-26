#
# Orchestration Layer Config for a DC3 production
#
root.production.shortName = "DataRelease"
root.production.eventBrokerHost = "lsst8.ncsa.uiuc.edu"
root.production.repositoryDirectory = "/home/srp/working/pipeline_new"
root.production.productionShutdownTopic = "productionShutdown2"

root.database["db1"].name = "dc3bGlobal"
root.database["db1"].system.authInfo.host = "lsst10.ncsa.illinois.edu"
root.database["db1"].system.authInfo.port = 3306
root.database["db1"].system.runCleanup.daysFirstNotice = 7
root.database["db1"].system.runCleanup.daysFinalNotice = 1

root.database["db1"].configurationClass = "lsst.ctrl.orca.db.DC3Configurator"
root.database["db1"].configuration["production"].globalDbName = "GlobalDB"
# root.database["db1"].configuration["production"].dcVersion = "PT1_2"
root.database["db1"].configuration["production"].dcVersion = "S12_sdss"
root.database["db1"].configuration["production"].dcDbName = "DC3b_DB"
root.database["db1"].configuration["production"].minPercDiskSpaceReq = 10
root.database["db1"].configuration["production"].userRunLife = 2
root.database["db1"].logger.launch = True

root.workflow["association"].platform.dir.defaultRoot = "/oasis/scratch/ux453102/temp_project/lsst"
root.workflow["association"].platform.dir.workDir = "work"
root.workflow["association"].platform.dir.inputDir = "input"
root.workflow["association"].platform.dir.outputDir = "output"
root.workflow["association"].platform.dir.updateDir = "update"
root.workflow["association"].platform.dir.scratchDir = "scratch"

root.workflow["association"].platform.deploy.defaultDomain = "ncsa.illinois.edu"

root.workflow["association"].shutdownTopic = "workflowShutdown2"

root.workflow["association"].configurationType = "condor"
root.workflow["association"].configurationClass = "lsst.ctrl.orca.CondorWorkflowConfigurator"
root.workflow["association"].configuration["condor"].condorData.localScratch = "/lsst/home/daues/orca-scratch/"
# root.workflow["association"].configuration["condor"].deployData.dataRepository = "/lsst/DC3/data/obstest"
# root.workflow["association"].configuration["condor"].deployData.collection = "CFHTLS/D2"
# root.workflow["association"].configuration["condor"].deployData.script = "/home/srp/working/pipeline_new/deployData.sh"


root.workflow["association"].task["isr"].scriptDir = "workers"
#root.workflow["association"].task["isr"].preScript.script.inputFile = "/home/srp/dag/templates/preScript.template"
#root.workflow["association"].task["isr"].preScript.script.outputFile = "pre.sh"

root.workflow["association"].task["isr"].preJob.script.inputFile = "$DATAREL_DIR/dagutils/dag/sdss/photo/dag/templates/preJob.sh.template"
root.workflow["association"].task["isr"].preJob.script.outputFile = "preJob.sh"
root.workflow["association"].task["isr"].preJob.condor.inputFile = "$DATAREL_DIR/dagutils/dag/sdss/photo/dag/templates/preJob.condor.template"
root.workflow["association"].task["isr"].preJob.condor.outputFile = "S2012Pipe.pre"

root.workflow["association"].task["isr"].postJob.script.inputFile = "$DATAREL_DIR/dagutils/dag/sdss/photo/dag/templates/postJob.sh.template"
root.workflow["association"].task["isr"].postJob.script.outputFile = "postJob.sh"
root.workflow["association"].task["isr"].postJob.condor.inputFile = "$DATAREL_DIR/dagutils/dag/sdss/photo/dag/templates/postJob.condor.template"
root.workflow["association"].task["isr"].postJob.condor.outputFile = "S2012Pipe.post"

root.workflow["association"].task["isr"].workerJob.script.inputFile = "$DATAREL_DIR/dagutils/dag/sdss/photo/dag/templates/worker.sh.template"
root.workflow["association"].task["isr"].workerJob.script.outputFile = "worker.sh"
root.workflow["association"].task["isr"].workerJob.condor.inputFile = "$DATAREL_DIR/dagutils/dag/sdss/photo/dag/templates/workerJob.condor.template"
root.workflow["association"].task["isr"].workerJob.condor.outputFile = "S2012Pipeline-template.condor"


# root.workflow["association"].task["isr"].preJob.script.keywords[" "] = "
# root.workflow["association"].task["isr"].postJob.script.keywords[" "] = "
# root.workflow["association"].task["isr"].workerJob.script.keywords[" "] = "

root.workflow["association"].task["isr"].preJob.script.keywords["OUTREFRUN"] = "s2012outc_sd0214"
root.workflow["association"].task["isr"].preJob.script.keywords["SKYMAPRUN"] = "v5-run0a"
root.workflow["association"].task["isr"].preJob.script.keywords["SKYMAPDATA"] = ""
root.workflow["association"].task["isr"].preJob.script.keywords["SKYMAPDEC"] = ""
root.workflow["association"].task["isr"].preJob.script.keywords["SKYMAPDIM"] = ""

root.workflow["association"].task["isr"].preJob.script.keywords["REFRUN"] = "s2012prod_sd0202"
root.workflow["association"].task["isr"].preJob.script.keywords["USERHOME"] = "/home/ux453102"
root.workflow["association"].task["isr"].preJob.script.keywords["USERNAME"] = "ux453102"
root.workflow["association"].task["isr"].preJob.script.keywords["DATADIR"] = "/oasis/scratch/ux453102/temp_project/lsst/dr7-coadds/deep2/field3_camcol4"
root.workflow["association"].task["isr"].preJob.script.keywords["EUPS_PATH"] = "/oasis/scratch/ux453102/temp_project/lsst/beta-0713/lsst_home"
root.workflow["association"].task["isr"].preJob.script.keywords["LSST_HOME"] = "/oasis/scratch/ux453102/temp_project/lsst/beta-0713/lsst_home"


root.workflow["association"].task["isr"].workerJob.script.keywords["DBNAME"] = "daues_S12_sdss_u_s2012prod_im0200c"
root.workflow["association"].task["isr"].workerJob.script.keywords["STRIP"] = "S"
root.workflow["association"].task["isr"].workerJob.script.keywords["CAMCOLS"] = "4,4"
root.workflow["association"].task["isr"].workerJob.script.keywords["REFRUN"] = "s2012prod_sd0202"
root.workflow["association"].task["isr"].workerJob.script.keywords["USERHOME"] = "/home/ux453102"
root.workflow["association"].task["isr"].workerJob.script.keywords["USERNAME"] = "ux453102"
root.workflow["association"].task["isr"].workerJob.script.keywords["DATADIR"] = "/oasis/scratch/ux453102/temp_project/lsst/dr7-coadds/deep2/field3_camcol4"
root.workflow["association"].task["isr"].workerJob.script.keywords["EUPS_PATH"] = "/oasis/scratch/ux453102/temp_project/lsst/beta-0713/lsst_home"
root.workflow["association"].task["isr"].workerJob.script.keywords["LSST_HOME"] = "/oasis/scratch/ux453102/temp_project/lsst/beta-0713/lsst_home"


root.workflow["association"].task["isr"].dagGenerator.dagName = "S2012Pipe"
root.workflow["association"].task["isr"].dagGenerator.script = "$DATAREL_DIR/dagutils/dag/sdss/photo/dag/scripts/newgenerateDag.py"
root.workflow["association"].task["isr"].dagGenerator.idsPerJob=12
# root.workflow["association"].task["isr"].dagGenerator.input = "$DATAREL_DIR/dagutils/dag/sdss/photo/dag/input/80000.sdss.input"

# root.workflow["association"].task["isr"].dagGenerator.input = "$DATAREL_DIR/dagutils/dag/sdss/photo/dag/input/19260.sdss.input"

# root.workflow["association"].task["isr"].dagGenerator.input = "$DATAREL_DIR/dagutils/dag/sdss/photo/dag/input/10.sdss.input"
# root.workflow["association"].task["isr"].dagGenerator.input = "$DATAREL_DIR/dagutils/dag/sdss/photo/dag/input/2000.sdss.input"
# root.workflow["association"].task["isr"].dagGenerator.input = "$DATAREL_DIR/dagutils/dag/sdss/photo/dag/input/144.sdss.input"
# root.workflow["association"].task["isr"].dagGenerator.input = "$DATAREL_DIR/dagutils/dag/sdss/photo/dag/input/4608.sdss.input"


# root.workflow["association"].task["isr"].dagGenerator.input = "/nfs/lsst/home/daues/work/dag-sdss-SA/dag/input/2355.sdss.input"
# root.workflow["association"].task["isr"].dagGenerator.input = "/nfs/lsst/home/daues/work/ptest/dag-sdss-SA/dag/input/sky-tiles"
# root.workflow["association"].task["isr"].dagGenerator.input = "/nfs/lsst/home/daues/work/dag-sdss-coadd/dag/input/20.sdss.coadd.input"

root.workflow["association"].task["isr"].dagGenerator.input = "/nfs/lsst/home/daues/work/dag-sdss-ccd/dag/input/2355.sdss.input"
