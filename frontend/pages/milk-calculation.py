import streamlit as st
import pandas as pd
import numpy as np
import pages.datasets as datasets
import pages.optimize_milk_mixture as optimize

# ------------------------------------------------------------- DEFINE INITIAL & SESSION_STATE
df_compositions = pd.DataFrame(datasets.get_material_data())
df_compositions = df_compositions.set_index('ingridient')
df_recepies = pd.DataFrame(datasets.get_recipe_data())
df_recepies = df_recepies.set_index('receipe')

def initialize_session_state():
    if 'stage' not in st.session_state:
        st.session_state.stage = 0
    if 'selected_recipe' not in st.session_state:
        st.session_state.selected_recipe = None
    if 'fresh_milk' not in st.session_state:
        st.session_state.fresh_milk = 0
    if 'production_batch' not in st.session_state:
        st.session_state.production_batch = 0
    if 'fresh_milk_fat' not in st.session_state:
        st.session_state.fresh_milk_fat = 0
    if 'fresh_milk_snf' not in st.session_state:
        st.session_state.fresh_milk_snf = 0
    if 'fresh_milk_protein' not in st.session_state:
        st.session_state.fresh_milk_protein = 0
    if 'fresh_milk_lactose' not in st.session_state:
        st.session_state.fresh_milk_lactose = 0
    if 'fat_priority' not in st.session_state:
        st.session_state.fat_priority = 0
    if 'snf_priority' not in st.session_state:
        st.session_state.snf_priority = 0
    if 'pro_priority' not in st.session_state:
        st.session_state.pro_priority = 0
    if 'lac_priority' not in st.session_state:
        st.session_state.lac_priority = 0
        
    if 'remaining_fat' not in st.session_state:
        st.session_state.remaining_fat = 0
    if 'remaining_snf' not in st.session_state:
        st.session_state.remaining_snf = 0
    if 'remaining_prot' not in st.session_state:
        st.session_state.remaining_prot = 0
    if 'remaining_lact' not in st.session_state:
        st.session_state.remaining_lact = 0

    if 'rework' not in st.session_state:
        st.session_state.rework = 0
    if 'rework_ts' not in st.session_state:
        st.session_state.rework_ts = 0
    if 'df_target' not in st.session_state:
        st.session_state.df_target = pd.DataFrame()
    if 'df_inv' not in st.session_state:
        st.session_state.df_inv = pd.DataFrame()
    if 'mixing_target_inverse' not in st.session_state:
        st.session_state.mixing_target_inverse = pd.DataFrame()

def set_recipe(i) : st.session_state.selected_recipe = i
def set_state(i): st.session_state.stage = i
initialize_session_state()

# DEFINE
# production_batch=30000
# fresh_milk=9408
# fresh_milk_fat = 0.034
# fresh_milk_snf = 0.0795
# fresh_milk_protein = 0.028
# rework=1650
# rework_ts= 0.0835

# fresh_milk_compositions_default={
#     'Fat':fresh_milk_fat, 'Snf':fresh_milk_snf,'Protein':fresh_milk_protein,
#     'Stabilizer_a':0, 'Stabilizer_b':0, 'Cocoa_a':0,'Cocoa_b':0, 'Sugar':0, 'Minor':0}

recipies_list = list(df_recepies.columns)
recipe_map = {'Chocolate': 0, 'Plain': 1, 'Strawberry': 2}
compositions_list=list(df_compositions.index)

# ------------------------------------------- HEADER

st.title('Milk Calculation')
st.image("https://www.ultrajaya.co.id/images/header-products.jpg",use_column_width=True)

# st.dataframe(df_compositions)
# st.dataframe(df_recepies)

# ------------------------------------------------------------- 1. form input
if st.session_state.stage >= 0 and st.session_state.stage < 5:
    st.header('Step 1 - Input Calculation')
    selected_recipe = st.selectbox(
            'Choose Recipe !',
            #[None, 'Chocolate', 'Plain', 'Strawberry'],
            [None, 'Plain'],
            on_change=set_state,
            args=[1]
        )
    if selected_recipe != None :
        recipe = set_recipe(recipe_map[selected_recipe])

if st.session_state.stage >= 1 and st.session_state.stage < 5 and selected_recipe != None: 
    st.write(f'Recipe Choosen is: {recipe} - {selected_recipe}')  
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.fresh_milk = st.number_input('Quantity Fresh Milk')
    with col2:
        st.session_state.production_batch = st.number_input('Quantity Batch',
        on_change=set_state,
        args=[2]
        )
    # with col3:
    #     show_ingredient = st.selectbox(
    #     'Show (a)ll ingredient or (d)efault?',
    #     ['Show All','Default Only'],
    #     on_change=set_state,
    #     args=[2]
    # )    
    st.markdown("<hr>", unsafe_allow_html=True)

if st.session_state.stage >=2 and st.session_state.stage < 5:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.session_state.fresh_milk_fat = st.number_input('Fresh Milk Fat')
    with col2:
        st.session_state.fresh_milk_snf = st.number_input('Fresh Milk SnF')
    with col3:
        st.session_state.fresh_milk_protein = st.number_input('Fresh Milk Protein')
    with col4:
        st.session_state.fresh_milk_lactose = st.number_input(
            'Fresh Milk Lactose',
            on_change = set_state,
            args=[3]
            )
        
    # st.write('Total Solid (TS) in fresh milk is : 9999')
    st.markdown("<hr>", unsafe_allow_html=True)

# if st.session_state.stage >=3 and st.session_state.stage < 4:
#     rework_pick = st.selectbox(
#         'Any rework of finish product?',
#         ['Yes','No'],
#     )

#     if rework_pick == 'Yes':
#         col1,col2 = st.columns(2)
#         with col1:
#             st.session_state.rework = st.number_input('Rework Quantity')
#         with col2:
#             st.session_state.rework_ts = st.number_input(
#                 'Total Solid'
#                 )
#         st.write(f'rework : {st.session_state.rework}, total solid : {st.session_state.rework_ts}')
#         st.markdown("<hr>", unsafe_allow_html=True)

#     st.button('Calculate Now !', 
#         type='primary', 
#         use_container_width=True,
#         on_click= set_state,
#         args=[4]
#         )

# DEFINE FRESH MILK COMPOSITION & REWORK
fresh_milk_compositions_default={
    'fat':st.session_state.fresh_milk_fat, 
    'snf':st.session_state.fresh_milk_snf,
    'prot':st.session_state.fresh_milk_protein,
    'lactose':st.session_state.fresh_milk_lactose,
    'sugar':0,
    'sugar_syrup':0,
    'garam':0,
    'stab':0,
    'budal':0
}
rework_default={
    'Qty':0, #st.session_state.rework,
    'TS':0, #st.session_state.rework_ts
}
# SET GLOBAL VARIABLES
recipe = st.session_state.selected_recipe
fresh_milk = st.session_state.fresh_milk
production_batch = st.session_state.production_batch
rework = st.session_state.rework
rework_ts = st.session_state.rework_ts

# ------------------------------------------------------------- 2. generate composition
if st.session_state.stage >= 3 and st.session_state.stage < 5:
    st.header('Step 2 - Review Calculation')

    # DEBUG
    col4,col5 = st.columns(2)
    with col4:
        st.write('Fresh Milk Compositions')
        st.write(fresh_milk_compositions_default)
    # with col5:
    #     st.write('Rework Quantity & Total Solid')
    #     st.write(rework_default)

    # st.write(df_compositions) 
    # st.write(f'check {fresh_milk_compositions_default["SMP"]}')

    # @st.dialog("Confirmation")
    # def confirm_dialog():
    #     st.write('All calculation is correct ?')
    #     col1,col2 = st.columns(2)
    #     with col1:
    #         if st.button('Cancel',use_container_width=True,):
    #             st.rerun()
    #     with col2:
    #         if st.button('Generate Now', 
    #                 type='primary', 
    #                 use_container_width=True,
    #                 ): 
    #             set_state(5)
    #             st.rerun()

    # A. Target Composition
    st.subheader('1. Target Composition')

    recipe = recipe - 1 

    recipe_ts=df_recepies.iloc[:,recipe].sum()
    recipe_compositions=df_recepies.iloc[:,recipe]*production_batch
    compositions_list=list(df_compositions.index)
    material_list=list(df_compositions.columns)
    # fresh_milk_compositions_dict=dict(fresh_milk_compositions_default)

    #fresh_milk_compositions
    temp=dict()
    for i in compositions_list:
        temp[i]=fresh_milk*fresh_milk_compositions_default[i]
    fresh_milk_compositions=pd.Series(temp,name='fresh_milk_compositions')

    #sugar
    temp=dict()
    for i in compositions_list:
        temp[i]=(df_recepies.loc['sugar'].values[0]*production_batch)*df_compositions['sugar'][i]
    sugar=pd.Series(temp,name='sugar')

    #garam
    temp=dict()
    for i in compositions_list:
        temp[i]=(df_recepies.loc['garam'].values[0]*production_batch)*df_compositions['garam'][i]
    garam=pd.Series(temp,name='garam')

    #stab
    temp=dict()
    for i in compositions_list:
        temp[i]=(df_recepies.loc['stab'].values[0]*production_batch)*df_compositions['stab'][i]
    stab=pd.Series(temp,name='stab')

    #budal
    temp=dict()
    for i in compositions_list:
        temp[i]=(df_recepies.loc['budal'].values[0]*production_batch)*df_compositions['budal'][i]
    budal=pd.Series(temp,name='budal')

    #========= rework_compositions
    temp=dict()
    for i in compositions_list:
        temp[i]=df_recepies.iloc[:,recipe][i]*(rework_ts/recipe_ts)*rework
    rework_compositions=pd.Series(temp,name='rework_compositions')
    #============== mixing_ds
    temp=dict()
    for i in compositions_list:
        temp[i]=recipe_compositions[i]-fresh_milk_compositions[i]-sugar[i]-garam[i]-stab[i]-budal[i]-rework_compositions[i]
    mixing_ds=pd.Series(temp,name='mixing_ds')
    #============ mixing target
    temp=dict()
    for i in compositions_list:
        temp[i]=mixing_ds[i]/production_batch
    mixing_target=pd.Series(temp,name='mixing_target')
    #=======
    df_target=pd.DataFrame([recipe_compositions,fresh_milk_compositions,sugar,garam,stab,budal,rework_compositions,mixing_ds,mixing_target]).transpose()

    st.session_state.df_target = df_target
    st.dataframe(df_target.style.highlight_max(axis=0),use_container_width=False)
    st.markdown("<hr>", unsafe_allow_html=True)

    # # B. Material Remaining Needed
    st.subheader('2. Material Remaining Needed')
    # Extract and round values from the Series to 4 decimal places
    st.session_state.remaining_fat = round(mixing_ds['fat'], 4)    # Gets 6.4980
    st.session_state.remaining_snf = round(mixing_ds['snf'], 4)    # Gets 615.6309
    st.session_state.remaining_prot = round(mixing_ds['prot'], 4)  # Gets 223.6500
    st.session_state.remaining_lact = round(mixing_ds['lactose'], 4)  # Gets 223.6500
    st.text(f'Fat: {st.session_state.remaining_fat} kg')
    st.text(f'SNF: {st.session_state.remaining_snf} kg') 
    st.text(f'Protein: {st.session_state.remaining_prot} kg')
    st.text(f'Lactose: {st.session_state.remaining_lact} kg')

    # # C. Priority List
    st.subheader('3. Set Priority Order for Milk Components (1-10), as 10 is the highest priority')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.session_state.fat_priority = st.number_input('FAT')
    with col2:
        st.session_state.snf_priority = st.number_input('SnF')
    with col3:
        st.session_state.pro_priority = st.number_input('Protein')
    with col4:
        st.session_state.lac_priority = st.number_input(
            'Lactose',
            on_change = set_state,
            args=[4]
            )
    
# ------------------------------------------------------------- 2. generate composition
if st.session_state.stage >= 4 and st.session_state.stage < 5:
    st.header('Step 3 - Result Calculation')
    total = 0
    def get_material_values(ingredients_df, *materials):
        return {
            material: tuple(float(ingredients_df.loc[nutrient, material]) * 100
                            for nutrient in ['fat', 'snf', 'prot', 'lactose'])
            for material in materials
        }
    # Declare Wights
    weights = {
        'fat': st.session_state.fat_priority,
        'snf': st.session_state.snf_priority,
        'protein': st.session_state.pro_priority,
        'lactose': st.session_state.lac_priority,
        }

    # Run the optimization
    result = optimize.optimize_milk_mixture(
        st.session_state.remaining_fat, 
        st.session_state.remaining_snf, 
        st.session_state.remaining_prot,
        st.session_state.remaining_lact, 
        get_material_values(df_compositions, 'smp', 'wmp', 'whey'),
        weights
        )

    # st.text the results
    st.text("-" * 50)
    st.text("Optimal Milk Mixture:")
    st.text("-" * 50)
    if 'error' in result and 'message' in result:
        st.text(f"Error: {result['error']}")
        st.text(f"Message: {result['message']}")
    else:
        st.text("Material Quantities:")
        for material, quantity in result['mix'].items():
            if quantity > 0.0001:  # Only show materials with non-zero quantities
                st.text(f"  {material}: {quantity:.4f}")

        st.text("\nTotal Quantity: {:.4f}".format(result['total_quantity']))

        st.text("\nNutritional Values:")
        st.text(f"  Fat:     Target: {result['target']['fat']:.4f}, Actual: {result['actual']['fat']:.4f}, Error: {result['error']['fat']:.4f}")
        st.text(f"  SNF:     Target: {result['target']['snf']:.4f}, Actual: {result['actual']['snf']:.4f}, Error: {result['error']['snf']:.4f}")
        st.text(f"  Protein: Target: {result['target']['protein']:.4f}, Actual: {result['actual']['protein']:.4f}, Error: {result['error']['protein']:.4f}")
        st.text(f"  Lactose: Target: {result['target']['lactose']:.4f}, Actual: {result['actual']['lactose']:.4f}, Error: {result['error']['lactose']:.4f}")

        st.text("-" * 50)
        st.text("\n\nTotaled All Materials:")
        st.text("-" * 50)

        st.text(f"  {'Fresh Milk'}: {st.session_state.fresh_milk:.4f}")
        total = total + st.session_state.fresh_milk
        
        for material, quantity in result['mix'].items():
            if quantity > 0.0001:  # Only show materials with non-zero quantities
                st.text(f"  {material}: {quantity:.4f}")
                total = total + quantity
        
        st.text(f"  {'Sugar'}: {st.session_state.df_target['plain']['sugar']:.4f}")
        total = total + st.session_state.df_target['plain']['sugar']
        st.text(f"  {'Sugar Syrup'}: {st.session_state.df_target['plain']['sugar_syrup']:.4f}")
        total = total + st.session_state.df_target['plain']['sugar_syrup']
        st.text(f"  {'Garam'}: {st.session_state.df_target['plain']['garam']:.4f}")
        total = total + st.session_state.df_target['plain']['garam']
        st.text(f"  {'Stabilizer'}: {st.session_state.df_target['plain']['stab']:.4f}")
        total = total + st.session_state.df_target['plain']['stab']
        st.text(f"  {'Budal Milk'}: {st.session_state.df_target['plain']['budal']:.4f}")
        total = total + st.session_state.df_target['plain']['budal']
        st.text(f"  {'Water'}: {st.session_state.production_batch-total:.4f}")
        st.text(f"  {'Total Material'}: {total+(st.session_state.production_batch-total):.4f}")