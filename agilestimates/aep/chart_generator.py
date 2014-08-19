def generate(labels, data):
    return {
                "labels": labels,
                "datasets": [
                                {
                                     "fillColor" : "rgba(172,194,132,0.4)",
                                     "strokeColor" : "#ACC26D",
                                     "pointColor" : "#fff",
                                     "pointStrokeColor" : "#9DB86D",
                                     "data": data
                                }
                            ]
            }
