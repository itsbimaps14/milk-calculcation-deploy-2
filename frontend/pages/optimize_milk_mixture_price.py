import numpy as np
from scipy.optimize import linprog

def optimize_milk_mixture(target_fat_kg, target_snf_kg, target_protein_kg, target_lactose_kg, materials,
                          prices=None, weights={'fat': 10, 'snf': 10, 'protein': 5, 'lactose': 1}):
    """
    Optimize milk mixture with cost optimization and custom weights for different nutrients.

    Parameters:
    - target_fat_kg: Target fat amount in kg
    - target_snf_kg: Target solids-not-fat amount in kg
    - target_protein_kg: Target protein amount in kg
    - target_lactose_kg: Target lactose amount in kg
    - materials: Dictionary with material properties {name: [fat%, snf%, protein%, lactose%]}
    - prices: Dictionary with price per kg for each material {name: price}
    - weights: Dictionary with relative importance of each nutrient
               Higher values make satisfying that constraint more important

    Returns:
    - Dictionary with optimization results
    """
    from scipy.optimize import linprog

    # Extract material properties
    material_names = list(materials.keys())
    fat_percentages = [materials[m][0] / 100 for m in material_names]
    snf_percentages = [materials[m][1] / 100 for m in material_names]
    protein_percentages = [materials[m][2] / 100 for m in material_names]
    lactose_percentages = [materials[m][3] / 100 for m in material_names]

    n_materials = len(material_names)

    # Calculate total target weight
    total_target_kg = target_fat_kg + target_snf_kg

    # Set up price coefficients
    if prices is None:
        # If no prices provided, set all to 1 (equal cost)
        prices = {name: 1 for name in material_names}

    # Make sure all materials have prices
    for name in material_names:
        if name not in prices:
            prices[name] = 1  # Default price if not specified

    price_coefficients = [prices[name] for name in material_names]

    # Try strict equality with cost optimization
    A_eq_strict = [
        fat_percentages,     # Fat contribution per kg of each material
        snf_percentages,     # SNF contribution per kg of each material
        protein_percentages, # Protein contribution per kg of each material
        lactose_percentages, # Lactose contribution per kg of each material
    ]

    b_eq_strict = [target_fat_kg, target_snf_kg, target_protein_kg, target_lactose_kg]

    # Use prices as cost coefficients to minimize
    c_strict = price_coefficients

    # Try to find exact solution that minimizes cost
    result_strict = linprog(c_strict, A_eq=A_eq_strict, b_eq=b_eq_strict,
                           bounds=[(0, None) for _ in range(n_materials)],
                           method='highs')

    if result_strict.success:
        result = result_strict
        quantities = result.x  # Quantities in kg
        total_cost = sum(quantities[i] * price_coefficients[i] for i in range(n_materials))
    else:
        # Use weighted slack variables if exact solution not possible
        # Set weights for slack variables based on input priorities
        fat_weight = weights['fat']
        snf_weight = weights['snf']
        protein_weight = weights['protein']
        lactose_weight = weights['lactose']

        # Coefficients for the objective function
        # For each nutrient, we have a negative slack and positive slack
        # Add a large constant (M) to ensure cost is optimized after constraints
        M = 10  
        # Large constant to prioritize meeting nutrient constraints over cost
        # M Value	Behavior
        # Very large (like 10¹⁶)	Nutrient matching is more important than cost.
        # Small (like 0.1 or 1)	Cost is prioritized over nutrient matching.
        # Medium (say 10 or 1000)	Balanced tradeoff between cost and nutrient matching.

        c = price_coefficients + [
            M * fat_weight, M * fat_weight,           # Fat under/over
            M * snf_weight, M * snf_weight,           # SNF under/over
            M * protein_weight, M * protein_weight,   # Protein under/over
            M * lactose_weight, M * lactose_weight    # Lactose under/over
        ]

        A_eq = [
            fat_percentages + [-1, 1, 0, 0, 0, 0, 0, 0],
            snf_percentages + [0, 0, -1, 1, 0, 0, 0, 0],
            protein_percentages + [0, 0, 0, 0, -1, 1, 0, 0],
            lactose_percentages + [0, 0, 0, 0, 0, 0, -1, 1]
        ]

        b_eq = [target_fat_kg, target_snf_kg, target_protein_kg, target_lactose_kg]

        bounds = [(0, None) for _ in range(n_materials + 8)]

        result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

        if result.success:
            quantities = result.x[:n_materials]  # Quantities in kg
            total_cost = sum(quantities[i] * price_coefficients[i] for i in range(n_materials))
        else:
            return {"error": "Optimization failed", "message": result.message}

    # Compute actual values
    actual_fat_kg = sum(q * fat_percentages[i] for i, q in enumerate(quantities))
    actual_snf_kg = sum(q * snf_percentages[i] for i, q in enumerate(quantities))
    actual_protein_kg = sum(q * protein_percentages[i] for i, q in enumerate(quantities))
    actual_lactose_kg = sum(q * lactose_percentages[i] for i, q in enumerate(quantities))

    mix = {name: round(quantity, 4) for name, quantity in zip(material_names, quantities)}

    # Calculate individual material costs
    material_costs = {name: round(quantity * prices[name], 4)
                     for name, quantity in zip(material_names, quantities)}

    return {
        'mix': mix,
        'total_quantity': round(sum(quantities), 4),
        'total_cost': round(total_cost, 4),
        'material_costs': material_costs,
        'actual': {
            'fat': round(actual_fat_kg, 4),
            'snf': round(actual_snf_kg, 4),
            'protein': round(actual_protein_kg, 4),
            'lactose': round(actual_lactose_kg, 4)
        },
        'target': {
            'fat': target_fat_kg,
            'snf': target_snf_kg,
            'protein': target_protein_kg,
            'lactose': target_lactose_kg
        },
        'error': {
            'fat': round(abs(actual_fat_kg - target_fat_kg), 4),
            'snf': round(abs(actual_snf_kg - target_snf_kg), 4),
            'protein': round(abs(actual_protein_kg - target_protein_kg), 4),
            'lactose': round(abs(actual_lactose_kg - target_lactose_kg), 4)
        }
    }