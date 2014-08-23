def generate(labels, data_list):
    return {
                "labels": labels,
                "datasets": build_datasets(data_list)
            }
def build_datasets(data_list):
    return map(build_dataset, data_list)

def build_dataset(data):
    return  {
                "fillColor" : "rgba(172,194,132,0.4)",
                "strokeColor" : "#ACC26D",
                "pointColor" : "#fff",
                "pointStrokeColor" : "#9DB86D",
                "data": data
            }
