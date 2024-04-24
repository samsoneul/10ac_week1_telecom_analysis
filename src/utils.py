import pandas as pd 

import os



def preproccess_numerical_data(df):
    # Fill missing values with mean for numerical columns
    numerical_cols = df.select_dtypes(include=['number']).columns
    for col in numerical_cols:
        df[col] = df[col].fillna(df[col].mean())
    return df





def preproccess_categorical_data(df):
    categorical_cols = df.select_dtypes(exclude=['number']).columns
    mode_values = df[categorical_cols].mode().iloc[0]
    df.loc[:, categorical_cols] = df[categorical_cols].fillna(mode_values)
    return df


