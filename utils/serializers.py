def to_dict(obj):
    if obj is None:
        return None

    data = obj.__dict__.copy()
    data.pop("_sa_instance_state", None)
    return data
