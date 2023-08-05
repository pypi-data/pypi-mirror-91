#
#
#

from threading import local

_local = local()

# Access current context(s) 
def get_current_context(silent=False):
   
    try:
        return _local.stack[-1]
    except (AttributeError, IndexError):
        if not silent:
            raise RuntimeError("No active content available.")

# Push new content to the stack
def push_context(ctx):

    _local.__dict__.setdefault("stack", []).append(ctx)

# Removes the top level from the stack
def pop_context():
    _local.stack.pop()

# Returns/gets the default value of color flag
def resolve_color_default(color=None):
 
    if color is not None:
        return color
    ctx = get_current_context(silent=True)
    if ctx is not None:
        return ctx.color
