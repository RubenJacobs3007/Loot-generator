# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 22:14:14 2025

@author: User
"""

import pandas as pd
import random as rd
import streamlit as st

magic_items = pd.read_csv('magic_items.csv')
magic_items['type'][269] = 'Staff'
common_potions = magic_items[(magic_items['type'] == 'Potion') & (magic_items['rarity']=='Common')]
common_potions.reset_index()
magic_items.count(0)
def random_item(rarities=None, types=None, count = 1):
    """
    Return a random magic item optionally filtered by rarities and/or types.
    
    Parameters:
        rarities: str or list of strings (optional)
        types: str or list of strings (optional)
    """
    fraction = magic_items.copy()
    
    if rarities is not None:
        if isinstance(rarities, str):
            rarities = [rarities]
        fraction = fraction[fraction['rarity'].isin(rarities)]
    
    if types is not None:
        if isinstance(types, str):
            types = [types]
        fraction = fraction[fraction['type'].isin(types)]
    
    if fraction.empty:
        return None
    
    # Pick a random row
    n = rd.sample(range(len(fraction)-1), count)
    return fraction.iloc[n]

def item_by_rarity(common=0, uncommon=0, rare=0, very_rare=0, legendary=0, artifact = 0, types = None):
    counts = {
        "Common": common,
        "Uncommon": uncommon,
        "Rare": rare,
        "Very Rare": very_rare,
        "Legendary": legendary,
        "Artifact": artifact
    }
    
    total = []

    for rarity, count in counts.items():
        if count > 0:
            df = magic_items[magic_items['rarity'] == rarity].reset_index(drop=True)
            if types is not None:
                if isinstance(types, str):
                    types = [types]
                df = df[df['type'].isin(types)]
            indices = rd.sample(range(len(df)), count)
            total.append(df.iloc[indices])
    
    return total


tab1, tab2 = st.tabs(["Random Generator", "By Rarity Counts"])

with tab1:
    st.header("Random Magic Items")
    rarities = st.multiselect(
        "Select rarities",
        ['Common','Uncommon','Rare','Very Rare','Legendary','Artifact'],
        default=['Common','Uncommon','Rare','Very Rare','Legendary','Artifact']
    )
    types_ = st.multiselect("Select types", magic_items['type'].unique(), default=magic_items['type'].unique(), key = 'random_item')
    count = st.number_input("Number of items", min_value=1, value=1)
    if st.button("Generate Random Items"):
        loot = random_item(rarities=rarities, types=types_, count=count)
        st.dataframe(loot)

with tab2:
    st.header("Generate Specific Amounts by Rarity")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        common = st.number_input("Common", min_value=0, value=0)
    with col2:
        uncommon = st.number_input("Uncommon", min_value=0, value=0)
    with col3:
        rare = st.number_input("Rare", min_value=0, value=0)
    
    # Nieuwe rij van kolommen
    col4, col5, col6 = st.columns(3)
    with col4:
        very_rare = st.number_input("Very Rare", min_value=0, value=0)
    with col5:
        legendary = st.number_input("Legendary", min_value=0, value=0)
    with col6:
        artifact = st.number_input("Artifact", min_value=0, value=0)

    types_rare = st.multiselect("Select types", magic_items['type'].unique(), default=magic_items['type'].unique(), key = 'rarity_types')
    if st.button("Generate by Rarity"):
        items = item_by_rarity(
            common=common,
            uncommon=uncommon,
            rare=rare,
            very_rare=very_rare,
            legendary=legendary,
            artifact=artifact,
            types=types_rare
        )
        items_df = pd.concat(items, ignore_index = True)
        st.dataframe(items_df)
        
