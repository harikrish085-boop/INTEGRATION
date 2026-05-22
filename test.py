	# =========================================================
	# IGNITION GATEWAY TIMER SCRIPT
	#
	# PURPOSE:
	#   Read tags recursively from folders
	#   Batch insert into SQL Server
	#   Prevent overlapping execution
	#   Auto recover from stuck execution
	#
	# TIMER SETTINGS:
	#
	# Delay Type : Fixed Delay
	# Delay      : 15000 ms
	# Threading  : Dedicated
	#
	# =========================================================
	
	#import system
	logger = system.util.getLogger("KepwareTagStore2")
	
	MAX_RUNTIME_MS = 60000
	
	
	# =========================================================
	# LOCK MANAGEMENT
	# =========================================================
	
	currentMillis = system.date.toMillis(
	    system.date.now()
	)
	
	# Initialize variables first time
	if not hasattr(system.util, "tagInsertRunning"):
	
	    system.util.tagInsertRunning = False
	
	if not hasattr(system.util, "tagInsertStartTime"):
	
	    system.util.tagInsertStartTime = 0
	
	
	# ---------------------------------------------------------
	# CHECK IF PREVIOUS EXECUTION STILL RUNNING
	# ---------------------------------------------------------
	
	if system.util.tagInsertRunning:
	
	    runningTime = (
	
	        currentMillis
	        -
	        system.util.tagInsertStartTime
	
	    )
	
	    # FORCE RESET IF STUCK
	    if runningTime > MAX_RUNTIME_MS:
	
	        logger.warn(
	
	            "Previous execution exceeded timeout. Resetting lock."
	
	        )
	
	        system.util.tagInsertRunning = False
	
	        system.util.tagInsertStartTime = 0
	
	    else:
	
	        logger.warn(
	
	            "Previous execution still running for %s ms. Skipping cycle."
	
	            % runningTime
	
	        )
	
	        return
	
	
	# ---------------------------------------------------------
	# ACQUIRE LOCK
	# ---------------------------------------------------------
	
	system.util.tagInsertRunning = True
	
	system.util.tagInsertStartTime = currentMillis


# =========================================================
# RECURSIVE TAG BROWSER
# =========================================================

def getAllTags(folderPaths):

    allTags = []

    try:

        for folderPath in folderPaths:

            browseResults = system.tag.browse(
                folderPath
            ).getResults()

            for tag in browseResults:

                tagType = str(tag["tagType"])

                # Atomic Tag
                if tagType == "AtomicTag":

                    allTags.append(
                        str(tag["fullPath"])
                    )

                # Recursive Folder Browse
                elif tagType == "Folder":

                    subFolder = str(
                        tag["fullPath"]
                    )

                    subTags = getAllTags(
                        [subFolder]
                    )

                    allTags.extend(subTags)

    except Exception as e:

        logger.error(
            "Browse Error : " + str(e)
        )

    return allTags


# =========================================================
# MAIN STORE FUNCTION
# =========================================================

def storeTags():

    startTime = system.date.now()

    try:

        # -------------------------------------------------
        # FOLDERS
        # -------------------------------------------------

        folders = [

            "[default]DataSource/Agratas/IN11/MES",

            "[default]DataSource/Agratas/IN11/E101/MES",

            "[default]DataSource/Agratas/IN11/E101/PRO/ACAL101/MES",

            "[default]DataSource/Agratas/IN11/E101/PRO/ACOT101/MES",

            "[default]DataSource/Agratas/IN11/E101/PRO/AMIX101/MES",

            "[default]DataSource/Agratas/IN11/E101/PRO/MES"

        ]


        # -------------------------------------------------
        # GET TAGS
        # -------------------------------------------------

        tags = getAllTags(folders)

        if len(tags) == 0:

            logger.warn(
                "No tags found"
            )

            return


        logger.info(
            "Total Tags Found : %s"
            % len(tags)
        )


        # -------------------------------------------------
        # READ TAGS
        # -------------------------------------------------

        values = system.tag.readBlocking(
            tags
        )


        # -------------------------------------------------
        # PREPARE BATCH INSERT
        # -------------------------------------------------

        batchArgs = []

        currentTime = system.date.now()

        machineId = "M" + system.date.format(
            currentTime,
            "yyyyMMdd"
        )


        for i in range(len(values)):

            try:

                valueObj = values[i]

                if valueObj.quality.isGood():

                    tagName = str(
                        tags[i]
                    )

                    tagValue = str(
                        valueObj.value
                    )

                    tagQuality = str(
                        valueObj.quality
                    )

                    batchArgs.append([

                        machineId,

                        tagName,

                        tagValue,

                        tagQuality,

                        currentTime

                    ])

            except Exception as innerEx:

                logger.error(

                    "Tag Processing Error : %s -> %s"

                    % (

                        tags[i],

                        str(innerEx)

                    )

                )


        # -------------------------------------------------
        # DATABASE INSERT
        # -------------------------------------------------

        if len(batchArgs) > 0:

            query = """

            INSERT INTO MachineTags
            (

                machineId,

                tagName,

                tagValue,

                tagQuality,

                eventTime

            )

            VALUES
            (
                ?, ?, ?, ?, ?
            )

            """


            # ---------------------------------------------
            # BATCH INSERT
            # ---------------------------------------------

            try:

                system.db.runPrepUpdateBatch(

                    query,

                    batchArgs,

                    "Dev_MSSQL_Server"

                )

            except AttributeError:

                logger.info(

                    "runPrepUpdateBatch unavailable; using runPrepUpdate per row"

                )

                for args in batchArgs:

                    system.db.runPrepUpdate(

                        query,

                        args,

                        "Dev_MSSQL_Server"

                    )


            logger.info(

                "Inserted %s records successfully"

                % len(batchArgs)

            )

        else:

            logger.warn(
                "No good quality tags"
            )


    except Exception as e:

        logger.error(
            "StoreTags Error : " + str(e)
        )


    finally:

        # -------------------------------------------------
        # EXECUTION TIME
        # -------------------------------------------------

        executionTime = system.date.millisBetween(

            startTime,

            system.date.now()

        )

        logger.info(

            "Execution Time : %s ms"

            % executionTime

        )


        # -------------------------------------------------
        # RELEASE LOCK
        # -------------------------------------------------

        system.util.tagInsertRunning = False

        system.util.tagInsertStartTime = 0


# =========================================================
# EXECUTE ASYNCHRONOUSLY
# =========================================================
#import system
logger = system.util.getLogger("KepwareTagStore2")
try:

    system.util.invokeAsynchronous(
        storeTags
    )

except Exception as e:

    logger.error(
        "Async Execution Error : " + str(e)
    )

    system.util.tagInsertRunning = False

    system.util.tagInsertStartTime = 0