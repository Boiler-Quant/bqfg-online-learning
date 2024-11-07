from vowpalwabbit.dftovw import DFtoVW

def df_to_vw(df, label, features=None, tag_col=None):
    """Convert a DataFrame to Vowpal Wabbit format.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to convert.
    label : str
        The column name to use as the label.
    features : list of str, optional
        The columns to use as features. If not provided, all columns
        except the label column are used.
    tag_col : str, optional
        The column name to use as the tag.
    
    Returns
    -------
    str
        The DataFrame in Vowpal Wabbit format.
    """
    if features is None:
        features = df.columns.drop(label).tolist()
    
    print(type(features))
    print(df.dtypes)
        
    converter = DFtoVW.from_column_names(df=df, x=features, y=label)
    return converter.convert_df()