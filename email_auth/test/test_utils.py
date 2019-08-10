def create_expected_repr(instance, fields):
    """
    Create the expected string representation of an instance.

    Args:
        instance:
            The instance to create the expected repr of.
        fields:
            An array of field names that should be in the repr.

    Returns:
        The expected output of ``repr(instance)``.
    """
    values = [f"{field}={repr(getattr(instance, field))}" for field in fields]

    return f"{instance.__class__.__name__}({', '.join(values)})"
