def detect(model, packets):
    """
    Returns:
    -1 => THREAT
     1 => SAFE
    """
    return model.predict(packets).tolist()
