"""Command for the power operation, loaded as a plugin."""
from app.plugins.example_plugin import PLUGIN_REGISTRY

def execute_power(x, y):
    """Executes the power command using the plugin."""
    return PLUGIN_REGISTRY['power'](x, y)
