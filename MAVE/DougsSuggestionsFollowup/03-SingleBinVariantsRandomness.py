import pandas as pd

def VariantDistribution(inF, Assays=['Assay22', 'Assay23', 'Assay24'], Bins=['Low', 'Middle', 'High']):
    ouFile = open(inF.split('.txt')[0] + '_SingleBinVariantsRandomness.txt', 'w')
    df = pd.read_table(inF, header=0, sep='\t')
    wh = (df['InDesignOrNot'] == 'InDesign') & (df['ConstructReference'] != 'Construct')
    df_sub = df.loc[wh, :]
    df_sub.index = df_sub.iloc[:, 0].astype('str') + '_' + df_sub.iloc[:, 1] + '_' + df_sub.iloc[:, 2]

    for Assay in Assays:
        wh = [x.split('_')[0] in [Assay] and x.split('_')[1] in Bins for x in df_sub.columns]
        df_sub2 = df_sub.loc[:, wh]
        for N in [0, 20, 100]:
            for j in range(df_sub2.shape[1]):
                wh = df_sub2.iloc[:, j] > N
                df_sub3 = df_sub2.loc[wh, ]
                wh = (df_sub3 > N).sum(axis=1) == 1
                df_sub4 = df_sub3.loc[wh, :]
                ouFile.write('\t'.join([Assay, str(N), df_sub2.columns[j].split('_')[1], ' '.join(df_sub4.index)]) + '\n')
        

    for Bin in Bins:
        wh = [x.split('_')[0] in Assays and x.split('_')[1] in [Bin] for x in df_sub.columns]
        df_sub2 = df_sub.loc[:, wh]
        for N in [0, 20, 100]:
            for j in range(df_sub2.shape[1]):
                wh = df_sub2.iloc[:, j] > N
                df_sub3 = df_sub2.loc[wh, ]
                wh = (df_sub3 > N).sum(axis=1) == 1
                df_sub4 = df_sub3.loc[wh, :]
                ouFile.write('\t'.join([Bin, str(N), df_sub2.columns[j].split('_')[0], ' '.join(df_sub4.index)]) + '\n')
 

VariantDistribution('MAVE_CodonCounts.txt')
