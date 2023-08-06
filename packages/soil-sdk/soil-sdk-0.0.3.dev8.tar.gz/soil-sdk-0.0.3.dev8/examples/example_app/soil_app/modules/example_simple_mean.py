from soil import modulify
from soil.data_structures.simple_datastructure import SimpleDataStructure


@modulify(output_types=lambda *input_types, **args: [SimpleDataStructure])
def simple_mean(patients, aggregation_column=None):
    if aggregation_column is None:
        raise TypeError('Expected aggregation_column parameter')
    total_sum = 0
    count = 0
    for patient in patients:
        if hasattr(patient, aggregation_column):
            val = patient[aggregation_column]
            total_sum += val
            count += 1
    return [SimpleDataStructure({'mean': round(total_sum / count)})]
