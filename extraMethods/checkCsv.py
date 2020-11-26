import pandas as pd
if __name__ == "__main__":
    df = pd.read_csv(
        r"C:\\Users\\Claudiu\Desktop\\Programming\\NLPProgramming\\Counts\SpacyNPFreqDict.csv", encoding="utf-8")
    print(df.head())
    df_agg = df.groupby(['word']).sum()
    df_agg.reset_index().sort_values(by='count', ascending=False).to_csv(
        'Counts/SpacyWordFreqDict.csv', index=False)
