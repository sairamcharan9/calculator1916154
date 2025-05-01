"""Example plugin for dynamic operation loading."""

def power(x, y):
    """Return x raised to the power y."""
    return x ** y

# PLUGIN_REGISTRY is a convention for dynamic discovery
PLUGIN_REGISTRY = {
    'power': power
}
