import os
import sys
import streamlit as st
from plotly.express import histogram
from pandas.errors import PerformanceWarning
from warnings import simplefilter

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.data import import_data, MetadataStats
from src.features import (
    MetaDataManagement,
    DataManagement
)
from src.utils import (
    train_valid_splitting,
    Modeling_Data,
    df_skewed_feature
)


simplefilter(action="ignore", category=PerformanceWarning)

raw_data = import_data()

_raw_data = raw_data.copy()

st.markdown("# Feature Engineering")
st.markdown(
    "Since ML model perform well with no leak of information \
    between train and test datasets, it comes to distinguish two \
    levels of data engineering"
)

st.markdown("## Metadata Level")

st.markdown(
    "Below is the metadata tables, one for numerical data type and \
    the other for character data type. They describe the raw properties \
    of each feature. for better understanding and better decision"
)

st.dataframe(
    data=MetadataStats(_raw_data).metadata_report('char'),
    use_container_width=True)
st.dataframe(
    data=MetadataStats(_raw_data).metadata_report('num'),
    use_container_width=True)

st.markdown("### Numerical features processing")
st.markdown(
    """
    A starting point of this section is the identification of
    useless features and their removing. Afterwards, due to some business
    assumptions some features cannot have a certain values like negative
    one or must be transformed in order to handle skewness or kurtosis.
    """
)


st.markdown(
    """
    * The following features can be handled as useless in view of the use case
    `issue_level2`, `resolution`, `city`, `city_lat`, `city_long`,
    `data_usage_amt`,
    `mou_onnet_6m_normal`, `mou_roam_6m_normal`, `region_lat`, `region_long`,
    `state_lat`, `state_long`, `tweedie_adjusted`, `upsell_xsell`; \n
    * Some variables especially those having `MB_Data_Usg_M0` are very skewed as
    the plot describes. A $\\log$ transformation here is suitable to handle
    log_MB_Data_Usg_M0_i = $\\log$ (1 + MB_Data_Usg_M0_i)
    """
)

feature = st.selectbox(
    "Choose a variable to see its distribution",
    (f"MB_Data_Usg_M0{str(i)}" for i in range(4, 10)))

plot_feature = st.radio(
    "Choose the values to be plotted: raw or log-transformed",
    (f"log_{feature}", feature))

fig = histogram(
    df_skewed_feature(_raw_data, feature),
    x=plot_feature, nbins=30, histnorm='probability density'
)
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """
    * It is not reasonable for some variables such as to have
    negative values. To handle this incoherence the $ReLU$ is applied to
    censor the value
    """
)

st.markdown("### Categorical & Text features processing")

st.markdown(
    """
    In order to outcome to same data structure for the both
    train and valid data sets, the TextMining decisions here are: \
    * For categorical features the method employed is OneHotEncoding. \
    * The text variable which is `verbatims` will be handled after splitting \
    the data set into train and validation partition in order to avoid
    information leaking. Indeed the idea here is to build a text mining model
    on the train data and afterwards fit that model on the validation
    data set
    """
)

MetaDataManagement(_raw_data).metadata_management_pipeline()

st.markdown("## Data Level")

X_train, X_test, y_train, y_test = train_valid_splitting(
    _raw_data, st.session_state["train_frac"]
)

st.markdown(
    f"THis part starts by splitting the data according to the selected\
    fraction in the previous page then {st.session_state['train_frac']} \
    % is reserved for training models and the remaining for model validation.\
    * Binning Interval features: \n\
    * Text mining on `verbatims` variable: "
)


X_train_sp_mat, _ = DataManagement(X_train).data_management_pipeline()
X_test_sp_mat, _ = DataManagement(X_test).data_management_pipeline()


modeling_data = Modeling_Data(
    X_train_sp_mat, X_test_sp_mat,
    y_train, y_test, "churn"
)

st.session_state["modeling_data"] = modeling_data
