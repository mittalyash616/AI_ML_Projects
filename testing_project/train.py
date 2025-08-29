# import pandas as pd

# def hike(series):
#     length_data=len(series)
#     result=[0]
#     for i in range(1, length_data):
#         prev=series[i-1]
#         current=series[i]
#         if prev == 0:
#             result.append(0)
#         else:
#             result.append((current-prev)/prev*100)
#     return result

# def check(df1):
#     length_data=len(df1)
#     new_df=df1.copy()
#     x=df1["EstimatedSalary"].tolist()
#     for i in range(length_data):
#         if(x[i]<50000):
#             new_df=new_df.drop(df1.index[i])
    
#     return new_df




# df=pd.read_csv(r"/Users/yashmittal/Downloads/Social_Network_Ads.csv")
# df=df.dropna()
# print(df)
# #sorted_df = df.sort_values(by="EstimatedSalary", key=lambda x: x.abs())
# changed_df=df.copy()
# changed_df["EstimatedSalary"]=hike(df["EstimatedSalary"].tolist())
# print(changed_df)
# changed_df_2=check(df)
# changed_df_2=changed_df_2.reset_index(drop=True)
# print(changed_df_2)
import streamlit as st
import pandas as pd

st.title("CSV Modifier App 📊")

# Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read CSV into DataFrame
    df = pd.read_csv(uploaded_file)
    st.write("### Original Data")
    st.dataframe(df)

    # Select column and threshold
    col_name = st.selectbox("Select a column for filtering", df.columns)
    threshold = st.number_input("Enter minimum value value to take", value=0)

    # Filter + Reset index
    def check(df1, col_name, threshold):
        new_df = df1[df1[col_name] >= threshold]
        new_df = new_df.reset_index(drop=True)
        new_df.index = new_df.index + 1
        return new_df

    changed_df = check(df, col_name, threshold)

    st.write("### Filtered Data")
    st.dataframe(changed_df)

    # Download button for modified CSV
    csv = changed_df.to_csv(index=True).encode("utf-8")
    st.download_button(
        label="Download Modified CSV",
        data=csv,
        file_name="modified.csv",
        mime="csv",
    )
