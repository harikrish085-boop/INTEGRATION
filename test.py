def doPost(request, session):

    import system
    import base64
    import traceback

    # IMPORTANT FOR SQL VARBINARY
    from jarray import array

    logger = system.util.getLogger("POSTIMAGE")

    try:

        logger.info("POST Image API Called")

        # Safe payload read
        data = request.get("data", {})

        # Read fields safely
        machinelocation = str(
            data.get("machinelocation", "")
        ).strip()

        status = str(
            data.get("status", "")
        ).strip()

        pinholes = str(
            data.get("pinholes", "")
        ).strip()

        imageName = str(
            data.get("imageName", "")
        ).strip()

        imageType = str(
            data.get("imageType", "jpg")
        ).strip()

        imageBase64 = data.get(
            "imageData",
            ""
        )

        # Use server timestamp
        createdAt = system.date.now()

        logger.info(
            "machinelocation=%s imageName=%s imageType=%s status=%s pinholes=%s"
            % (
                machinelocation,
                imageName,
                imageType,
                status,
                pinholes
            )
        )

        # Validate machinelocation
        if machinelocation == "":

            logger.warn("machinelocation missing")

            return {
                "json": {
                    "status": "error",
                    "message": "machinelocation missing"
                }
            }

        # Validate imageName
        if imageName == "":

            logger.warn("imageName missing")

            return {
                "json": {
                    "status": "error",
                    "message": "imageName missing"
                }
            }

        # Validate imageData
        if imageBase64 == "":

            logger.warn("imageData missing")

            return {
                "json": {
                    "status": "error",
                    "message": "imageData missing"
                }
            }

        # Decode Base64 safely
        try:

            logger.info("Decoding Base64 image")

            decoded = base64.b64decode(imageBase64)

            # Convert to Java byte[]
            imageBytes = array(decoded, 'b')

        except Exception as decodeError:

            logger.error("Base64 decode failed")
            logger.error(str(decodeError))

            return {
                "json": {
                    "status": "error",
                    "message": "Invalid Base64 image"
                }
            }

        # Log image size only
        logger.info(
            "Image Size Bytes = %s" % len(imageBytes)
        )

        # SQL Insert Query
        query = """
            INSERT INTO images_demo
            (
                machinelocation,
                status,
                pinholes,
                imageName,
                imageType,
                createdAt,
                imageData
            )
            VALUES
            (
                ?, ?, ?, ?, ?, ?, ?
            )
        """

        logger.info("Executing SQL Insert")

        # Execute Insert
        rows = system.db.runPrepUpdate(
            query,
            [
                machinelocation,
                status,
                pinholes,
                imageName,
                imageType,
                createdAt,
                imageBytes
            ],
            "MESDEV"
        )

        logger.info(
            "Image inserted successfully"
        )

        # Success Response
        return {
            "json": {
                "status": "success",
                "rowsAffected": rows,
                "machinelocation": machinelocation,
                "imageName": imageName,
                "imageType": imageType,
                "createdAt": str(createdAt)
            }
        }

    except Exception as e:

        logger.error(
            "POST Image Error: " + str(e)
        )

        logger.error(
            traceback.format_exc()
        )

        return {
            "json": {
                "status": "error",
                "message": str(e)
            }
        }