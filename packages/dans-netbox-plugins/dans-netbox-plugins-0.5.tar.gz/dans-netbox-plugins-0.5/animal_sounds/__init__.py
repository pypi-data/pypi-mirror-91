# importing PluginConfig
from extras.plugins import PluginConfig

# defining config class for animal sounds
class AnimalSoundsConfig(PluginConfig):
    name = "netbox_animal_sounds"
    verbose_name = "Animal Sounds"
    description = "Tracks animal sounds, by animal."
    version = "0.1"
    author = "Daniel Murphy"
    author_email = "dev@danielmurphy.email"
    base_url = "animal-sounds"
    required_settings = []
    # default settings that will affect our plugin behavior
    default_settings = {
        'loud' : False
    }

# instantiating our config
config = AnimalSoundsConfig
