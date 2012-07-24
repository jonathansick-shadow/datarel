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
#root.workflow["association"].task["isr"].preScript.template = "/home/srp/dag/templates/preScript.template"
#root.workflow["association"].task["isr"].preScript.outputFile = "pre.sh"

root.workflow["association"].task["isr"].preJob.script.template = "/nfs/lsst/home/daues/work/ptest/dag/sdss/pcoadd/dag/templates/preJob.sh.template"
root.workflow["association"].task["isr"].preJob.script.outputFile = "preJob.sh"
root.workflow["association"].task["isr"].preJob.template = "/nfs/lsst/home/daues/work/ptest/dag/sdss/pcoadd/dag/templates/preJob.condor.template"
root.workflow["association"].task["isr"].preJob.outputFile = "S2012Pipe.pre"

root.workflow["association"].task["isr"].postJob.script.template = "/nfs/lsst/home/daues/work/ptest/dag/sdss/pcoadd/dag/templates/postJob.sh.template"
root.workflow["association"].task["isr"].postJob.script.outputFile = "postJob.sh"
root.workflow["association"].task["isr"].postJob.template = "/nfs/lsst/home/daues/work/ptest/dag/sdss/pcoadd/dag/templates/postJob.condor.template"
root.workflow["association"].task["isr"].postJob.outputFile = "S2012Pipe.post"

# root.workflow["association"].task["isr"].workerJob.script.template = "/nfs/lsst/home/daues/work/ptest/dag/sdss/pcoadd/dag/templates/helloworld.sh.template"
# root.workflow["association"].task["isr"].workerJob.script.outputFile = "helloworld.sh"
root.workflow["association"].task["isr"].workerJob.script.template = "/nfs/lsst/home/daues/work/ptest/dag/sdss/pcoadd/dag/templates/worker.sh.template"
root.workflow["association"].task["isr"].workerJob.script.outputFile = "worker.sh"
root.workflow["association"].task["isr"].workerJob.template = "/nfs/lsst/home/daues/work/ptest/dag/sdss/pcoadd/dag/templates/workerJob.condor.template"
root.workflow["association"].task["isr"].workerJob.outputFile = "S2012Pipeline-template.condor"

root.workflow["association"].task["isr"].dagGenerator.dagName = "S2012Pipe"
root.workflow["association"].task["isr"].dagGenerator.script = "/nfs/lsst/home/daues/work/ptest/dag/sdss/pcoadd/dag/scripts/newgenerateDag.py"
# root.workflow["association"].task["isr"].dagGenerator.input = "/nfs/lsst/home/daues/work/ptest/dag/sdss/pcoadd/dag/input/80000.sdss.input"

# root.workflow["association"].task["isr"].dagGenerator.input = "/nfs/lsst/home/daues/work/ptest/dag/sdss/pcoadd/dag/input/19260.sdss.input"

# root.workflow["association"].task["isr"].dagGenerator.input = "/nfs/lsst/home/daues/work/ptest/dag/sdss/pcoadd/dag/input/10.sdss.input"
# root.workflow["association"].task["isr"].dagGenerator.input = "/nfs/lsst/home/daues/work/ptest/dag/sdss/pcoadd/dag/input/2000.sdss.input"
# root.workflow["association"].task["isr"].dagGenerator.input = "/nfs/lsst/home/daues/work/ptest/dag/sdss/pcoadd/dag/input/144.sdss.input"
# root.workflow["association"].task["isr"].dagGenerator.input = "/nfs/lsst/home/daues/work/ptest/dag/sdss/pcoadd/dag/input/4608.sdss.input"

# root.workflow["association"].task["isr"].dagGenerator.input = "/nfs/lsst/home/daues/work/ptest/dag/sdss/pcoadd/dag/input/2355.sdss.input"
root.workflow["association"].task["isr"].dagGenerator.input = "/nfs/lsst/home/daues/work/ptest/dag/sdss/pcoadd/dag/input/20.sdss.coadd.input"


