from .test import *

COMPREHENSIVE_THEME_DIRS = [
    REPO_ROOT / "themes",
    REPO_ROOT / "common/test",
    REPO_ROOT / "common/test/appsembler",
]
DEFAULT_SITE_THEME = "appsembler-theme"
USE_S3_FOR_CUSTOMER_THEMES = False
CUSTOMER_THEMES_LOCAL_DIR = os.path.join(COMPREHENSIVE_THEME_DIRS[-1], 'customer_themes')

FEATURES['ENABLE_SYSADMIN_DASHBOARD'] = False

import logging
logging.disable(logging.WARNING)
