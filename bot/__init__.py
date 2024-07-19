import sys

from bot.config import settings

if settings.OS == "Windows_NT":
    sys.path.append(fr"{settings.PATH_TO_PROJECT_WINDOWS}")
else:
    sys.path.append(fr"{settings.PATH_TO_PROJECT_UNIX}")
