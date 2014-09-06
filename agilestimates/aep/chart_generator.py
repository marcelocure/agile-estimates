from random import choice
rgb_list = ['#FF0000','#4D00FF','#00FF80','#FFEF00']

def generate(labels, data_list):
    return {
                "labels": labels,
                "datasets": build_datasets(data_list)
            }
def build_datasets(data_list):
    color = ''
    datasets = []
    for data in data_list:

        dataset, prev_color = build_dataset(data["data"], color, data["title"])
        color = prev_color
        datasets.append(dataset)
    return datasets

def build_dataset(data, prev_color, title):
    color = choice(rgb_list)
    while prev_color == color:
        color = choice(rgb_list)
    dataset = {
                "fillColor" : "rgba(172,194,132,0.4)",
                "strokeColor" : color,
                "pointColor" : "#fff",
                "pointStrokeColor" : "#9DB86D",
                "data": data,
                "label": title
            }
    return dataset, color