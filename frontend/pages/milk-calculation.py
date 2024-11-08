import streamlit as st
import pandas as pd
import numpy as np
from pages.datasets import df_compositions, df_recepies

# ------------------------------------------------------------- DEFINE INITIAL & SESSION_STATE
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

# ------------------------------------------------------------- 1. form input
if st.session_state.stage >= 0 and st.session_state.stage < 4:
    st.header('Step 1 - Input Calculation')
    selected_recipe = st.selectbox(
            'Choose Recipe !',
            [None, 'Chocolate', 'Plain', 'Strawberry'],
            on_change=set_state,
            args=[1]
        )
    if selected_recipe != None :
        recipe = set_recipe(recipe_map[selected_recipe])

if st.session_state.stage >= 1 and st.session_state.stage < 4 and selected_recipe != None: 
    st.write(f'Recipe Choosen is: {recipe} - {selected_recipe}')  
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.fresh_milk = st.number_input('Quantity Fresh Milk')
    with col2:
        st.session_state.production_batch = st.number_input('Quantity Batch')
    with col3:
        show_ingredient = st.selectbox(
        'Show (a)ll ingredient or (d)efault?',
        ['Show All','Default Only'],
        on_change=set_state,
        args=[2]
    )    
    st.markdown("<hr>", unsafe_allow_html=True)

if st.session_state.stage >=2 and st.session_state.stage < 4:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.fresh_milk_fat = st.number_input('Fresh Milk Fat')
    with col2:
        st.session_state.fresh_milk_snf = st.number_input('Fresh Milk SnF')
    with col3:
        st.session_state.fresh_milk_protein = st.number_input(
            'Fresh Milk Protein',
            on_change = set_state,
            args=[3]
            )
        
    st.write('Total Solid (TS) in fresh milk is : 9999')
    st.markdown("<hr>", unsafe_allow_html=True)

if st.session_state.stage >=3 and st.session_state.stage < 4:
    rework_pick = st.selectbox(
        'Any rework of finish product?',
        ['Yes','No'],
    )

    if rework_pick == 'Yes':
        col1,col2 = st.columns(2)
        with col1:
            st.session_state.rework = st.number_input('Rework Quantity')
        with col2:
            st.session_state.rework_ts = st.number_input(
                'Total Solid'
                )
        st.write(f'rework : {st.session_state.rework}, total solid : {st.session_state.rework_ts}')
        st.markdown("<hr>", unsafe_allow_html=True)

    st.button('Calculate Now !', 
        type='primary', 
        use_container_width=True,
        on_click= set_state,
        args=[4]
        )

# DEFINE FRESH MILK COMPOSITION & REWORK
fresh_milk_compositions_default={
    'Fat':st.session_state.fresh_milk_fat, 
    'Snf':st.session_state.fresh_milk_snf,
    'Protein':st.session_state.fresh_milk_protein,
    'Stabilizer_a':0, 
    'Stabilizer_b':0, 
    'Cocoa_a':0,
    'Cocoa_b':0, 
    'Sugar':0, 
    'Minor':0
}
rework_default={
    'Qty':st.session_state.rework,
    'TS':st.session_state.rework_ts
}
# SET GLOBAL VARIABLES
recipe = st.session_state.selected_recipe
fresh_milk = st.session_state.fresh_milk
production_batch = st.session_state.production_batch
rework = st.session_state.rework
rework_ts = st.session_state.rework_ts

# ------------------------------------------------------------- 2. generate composition
if st.session_state.stage == 4:
    st.header('Step 2 - Review Calculation')

    # DEBUG
    col4,col5 = st.columns(2)
    with col4:
        st.write('Fresh Milk Compositions')
        st.write(fresh_milk_compositions_default)
    with col5:
        st.write('Rework Quantity & Total Solid')
        st.write(rework_default)

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
    #========= rework_compositions
    temp=dict()
    for i in compositions_list:
        temp[i]=df_recepies.iloc[:,recipe][i]*(rework_ts/recipe_ts)*rework
    rework_compositions=pd.Series(temp,name='rework_compositions')
    #============== mixing_ds
    temp=dict()
    for i in compositions_list:
        temp[i]=recipe_compositions[i]-fresh_milk_compositions[i]-rework_compositions[i]
    mixing_ds=pd.Series(temp,name='mixing_ds')
    #============ mixing target
    temp=dict()
    for i in compositions_list:
        temp[i]=mixing_ds[i]/production_batch
    mixing_target=pd.Series(temp,name='mixing_target')
    #=======
    df_target=pd.DataFrame([recipe_compositions,fresh_milk_compositions,rework_compositions,mixing_ds,mixing_target]).transpose()
    st.session_state.df_target = df_target
    st.dataframe(df_target.style.highlight_max(axis=0),use_container_width=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # B. Inverse Matrix
    st.subheader('2. Inverse Matrix of Material Composition')
    df_inv = pd.DataFrame(np.linalg.pinv(df_compositions.values),df_compositions.columns, df_compositions.index)
    st.session_state.df_inv = df_inv
    st.dataframe(df_inv.style.highlight_max(axis=0),use_container_width=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # C. Multiply Inverse Matrix
    st.subheader('3. Multiply Inverse Matrix with Target Matrix')
    mixing_target_inverse=df_inv.dot(df_target.mixing_target)
    st.session_state.mixing_target_inverse = mixing_target_inverse
    st.dataframe(mixing_target_inverse)

    col1,col2 = st.columns(2)
    with col1 :
        st.button('Back Process', 
                  on_click= set_state, 
                  args=[3], 
                  icon=':material/arrow_back:',
                  use_container_width=True,
                  )
    with col2 :
        st.button('Calculate Now !', 
                type='primary', 
                use_container_width=True,
                on_click= set_state,
                args=[5]
                )
        
# SET GLOBAL VARIABLES
df_target = st.session_state.df_target
df_inv = st.session_state.df_inv
mixing_target_inverse = st.session_state.mixing_target_inverse

#  ------------------------------------------------------------- 3. Final Calculation
if st.session_state.stage == 5:
    # TITLE PAGE
    st.header('Step 3 - Final Calculation')
    st.subheader('Final Calculation')

    # ======================= START NEW, init the variables
    material_list=list(df_compositions.keys())
    compositions_list=list(df_compositions.index)
    final=dict()
    final_list=[]
    #======== final_kg, usage material to achieve target
    final['kg']=pd.Series(list('0'*len(material_list)),index=material_list,dtype='float')
    final['kg']=dict(final['kg'])
    for i in material_list:
        final['kg'][i]=mixing_target_inverse[i]*production_batch
    final['kg']['Fresh_milk']=fresh_milk
    final['kg']['Rework']=rework
    final['kg']['material']=sum(final['kg'].values())
    final['kg']['water']=production_batch-final['kg']['material']
    final_list.append(pd.Series(final['kg'],name='final_kg'))
    final_temp=final['kg']
    comp_pos=0
    for j in range(len(compositions_list)):
        comp_pos=j
        temp=pd.Series(list('0'*len(material_list)),index=material_list,dtype='float')
        temp=dict(temp)
        for i in material_list:
            temp[i]=final_temp[i]*df_compositions.loc[
            compositions_list[comp_pos],[i]].values[0]
        temp['Fresh_milk']=final['kg']['Fresh_milk']*fresh_milk_compositions_default[
            compositions_list[comp_pos]]
        temp['Rework']=df_target.loc[compositions_list[comp_pos],'rework_compositions']
        temp['material']=sum(temp.values())
        temp['ds']=temp['material']/production_batch
        final[compositions_list[comp_pos]]=temp
        final_list.append(pd.Series(temp,name=compositions_list[comp_pos]))

    df_final=pd.DataFrame(final)
    df_final.loc['ds','kg']=pd.DataFrame(final).loc['ds',:].sum()

    # PREVIEW RESULT
    st.dataframe(df_final.style.highlight_max(axis=0))

    # PREVIEW COMPARISON
    st.write('total ds in recipe:',df_recepies.iloc[:,recipe].sum())
    st.write('total ds final calculation:',df_final.loc['ds','kg'])
    st.write('difference ds:',df_final.loc['ds','kg']-df_recepies.iloc[:,recipe].sum(),'\n')
    st.write('Fresh Milk:',fresh_milk,'fat:',st.session_state.fresh_milk_fat,'snf',st.session_state.fresh_milk_snf,'protein:',st.session_state.fresh_milk_protein)
    st.write('Batch:',production_batch)
    st.write('Rework:',rework,'ts:',rework_ts)
    st.write(f'Recipe chosen is >{recipies_list[recipe]}<\n')

    st.markdown("<hr>", unsafe_allow_html=True)
    col7,col8,col9=st.columns(3)
    with col7:
        st.write('Composition')
    with col8:
        st.write('Target')
    with col9:
        st.write('Final')
    # st.write('Composition:         Target:   Final:')

    for i in range(len(df_recepies.index)):
        # line ='{:<20}'.format(df_recepies.index[i])+':'+'{:.3%}'.format(df_recepies.iloc[i,recipe])+':  {:.3%}'.format(df_final.iloc[13,i+1])
        col4,col5,col6 = st.columns(3)
        with col4:
            st.write('{:<20}'.format(df_recepies.index[i]))
        with col5:
            st.write('{:.3%}'.format(df_recepies.iloc[i,recipe]))
        with col6:
            st.write('{:.3%}'.format(df_final.iloc[13,i+1]))
        # st.write(line)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.write('\n\nMaterial use:\n')
    n=0
    for i in df_final.kg.index:
        line = '{0:0.2f}'.format(float(df_final.kg[i]))
        st.write(i.ljust(12)+':',line.rjust(10))

    col1,col2 = st.columns(2)
    with col1 :
        st.button('Back Process', 
                  on_click= set_state, 
                  args=[4], 
                  icon=':material/arrow_back:',
                  use_container_width=True,
                  )
    with col2 :
        st.button('Finished', 
                    type='primary', 
                    use_container_width=True,
                    on_click= set_state,
                    args=[0]
                )