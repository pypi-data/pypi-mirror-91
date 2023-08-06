from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link='plugins:netbox_animal_sounds:random_animal',
        link_text='Random sound',
        buttons=(
            PluginMenuButton('home', 'Button A', 'fa fa-info', ButtonColorChoices.BLUE),
            PluginMenuButton('home', 'Button B', 'fa fa-warning', ButtonColorChoices.GREEN),
        )
    ),
)
