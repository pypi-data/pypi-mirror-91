# importing PluginConfig
from extras.plugins import PluginConfig


class PatchTrackerConfig(PluginConfig):
    name = "patch_tracker"
    verbose_name = "Patch Tracker"
    description = "Tracks pre-patches using existing NetBox tagging."
    version = "0.1"
    author = "Daniel Murphy"
    author_email = "dev@danielmurphy.email, dmurphy@pilotfiber.com"
    base_url = "patch-tracker"
    required_settings = []
    default_settings = {}

# instantiating our config
config = PatchTrackerConfig
