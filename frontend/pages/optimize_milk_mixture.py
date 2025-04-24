import numpy as np
from scipy.optimize import linprog

def optimize_milk_mixture(target_fat, target_snf, target_protein, target_lactose, materials,
                          weights={'fat': 10, 'snf': 10, 'protein': 10, 'lactose': 1}):
    """
    Optimize milk mixture with custom weights for different nutrients.

    Parameters:
    - weights: Dictionary with relative importance of each nutrient
               Higher values make satisfying that constraint more important
    """
    # Extract material properties
    material_names = list(materials.keys())
    fat_percentages = [materials[m][0] / 100 for m in material_names]
    snf_percentages = [materials[m][1] / 100 for m in material_names]
    protein_percentages = [materials[m][2] / 100 for m in material_names]
    lactose_percentages = [materials[m][3] / 100 for m in material_names]

    n_materials = len(material_names)

    # Try strict equality first
    A_eq_strict = [
        fat_percentages,
        snf_percentages,
        protein_percentages,
        lactose_percentages,
        [1] * n_materials  # Sum to 1 constraint
    ]

    b_eq_strict = [target_fat, target_snf, target_protein, target_lactose, 1]
    c_strict = [0] * n_materials

    # Try to find exact solution
    result_strict = linprog(c_strict, A_eq=A_eq_strict, b_eq=b_eq_strict,
                           bounds=[(0, None) for _ in range(n_materials)],
                           method='highs')

    if result_strict.success:
        result = result_strict
        quantities = result.x
    else:
        # Use weighted slack variables if exact solution not possible
        # Set weights for slack variables based on input priorities
        fat_weight = weights['fat']
        snf_weight = weights['snf']
        protein_weight = weights['protein']
        lactose_weight = weights['lactose']

        # Coefficients for the objective function
        # For each nutrient, we have a negative slack and positive slack
        c = [0] * n_materials + [
            fat_weight, fat_weight,           # Fat under/over
            snf_weight, snf_weight,           # SNF under/over
            protein_weight, protein_weight,   # Protein under/over
            lactose_weight, lactose_weight    # Lactose under/over
        ]

        A_eq = [
            fat_percentages + [-1, 1, 0, 0, 0, 0, 0, 0],
            snf_percentages + [0, 0, -1, 1, 0, 0, 0, 0],
            protein_percentages + [0, 0, 0, 0, -1, 1, 0, 0],
            lactose_percentages + [0, 0, 0, 0, 0, 0, -1, 1]
        ]

        b_eq = [target_fat, target_snf, target_protein, target_lactose]

        bounds = [(0, None) for _ in range(n_materials + 8)]

        result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

        if result.success:
            quantities = result.x[:n_materials]
        else:
            return {"error": "Optimization failed", "message": result.message}

    # Compute actual values
    actual_fat = sum(q * fat_percentages[i] for i, q in enumerate(quantities))
    actual_snf = sum(q * snf_percentages[i] for i, q in enumerate(quantities))
    actual_protein = sum(q * protein_percentages[i] for i, q in enumerate(quantities))
    actual_lactose = sum(q * lactose_percentages[i] for i, q in enumerate(quantities))

    mix = {name: round(quantity, 4) for name, quantity in zip(material_names, quantities)}

    return {
        'mix': mix,
        'total_quantity': sum(quantities),
        'actual': {
            'fat': round(actual_fat, 4),
            'snf': round(actual_snf, 4),
            'protein': round(actual_protein, 4),
            'lactose': round(actual_lactose, 4)
        },
        'target': {
            'fat': target_fat,
            'snf': target_snf,
            'protein': target_protein,
            'lactose': target_lactose
        },
        'error': {
            'fat': round(abs(actual_fat - target_fat), 4),
            'snf': round(abs(actual_snf - target_snf), 4),
            'protein': round(abs(actual_protein - target_protein), 4),
            'lactose': round(abs(actual_lactose - target_lactose), 4)
        }
    }