def qualitycontrol(entry):
    appnd = True

    try:
        img_link = entry.image

        if img_link.lower() == "none":
            appnd = False
    except Exception:
        appnd = False

    return appnd
