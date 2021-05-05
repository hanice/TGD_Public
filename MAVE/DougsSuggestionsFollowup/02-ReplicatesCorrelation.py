from pyst import *
import pandas as pd
import scipy.stats

def ReplicatesCorrelation(inF, MinCounts=20):
    ouF = inF.split('.txt')[0] + '_MinCounts%s_Correlation.txt'%MinCounts
    ouFile = open(ouF, 'w')
    ouFile.write('Contrast\tPearsonR\tSpearmanR\n')

    df = pd.read_table(inF, header=0)

    wh = (df['InDesignOrNot'] == 'InDesign') & (df['ConstructReference'] != 'Construct')
    df = df.loc[wh, :]

    #TP = ['High', 'Middle', 'Low', 'Unsorted', 'Uninduced']
    TP = ['High', 'Middle', 'Low', 'Unsorted']
    CL = {}
    CL['Uninduced'] = 'C0'
    CL['Unsorted'] = 'C1'
    CL['Low'] = 'C2'
    CL['Middle'] = 'C3'
    CL['High'] = 'C4'

    for tp in TP:
        wh = [True if x.find(tp) != -1 and x.split('_')[0] in ['Assay22', 'Assay23', 'Assay24'] else False for x in df.columns]
        df_sub = df.loc[:, wh]
        #s = df_sub.sum(axis=1)
        #df_sub = df_sub.loc[s > MinCounts, :]
        s = (df_sub > MinCounts).all(axis=1)
        df_sub = df_sub.loc[s, :]
        print(df_sub.shape)
        for i in range(df_sub.shape[1] - 1):
            for j in range(i + 1, df_sub.shape[1]):
                fig = plt.figure()
                ax = fig.add_subplot()
                X = df_sub.iloc[:, i]
                Y = df_sub.iloc[:, j]
                X_log10 = np.log10(X)
                Y_log10 = np.log10(Y)
                m = max(list(X_log10) + list(Y_log10))
                cor1 = scipy.stats.pearsonr(X_log10, Y_log10)[0]
                cor2 = scipy.stats.spearmanr(X_log10, Y_log10)[0]
                ax.scatter(X_log10, Y_log10, color=CL[tp])
                ax.set_title('number of codons (counts > %s): %s (%.2f%%)\npearson r: %.2f, spearman r: %.2f'%(MinCounts, df_sub.shape[0], df_sub.shape[0]/df.shape[0]*100, cor1, cor2))
                ax.set_xlim(0, m + 2)
                ax.set_ylim(0, m + 2)
                ax.set_xlabel(df_sub.columns[i] + ' (log10)')
                ax.set_ylabel(df_sub.columns[j] + ' (log10)')
                ct = '%s_%s_%s'%(tp, df_sub.columns[i].split('_')[0], df_sub.columns[j].split('_')[0])
                print('%s\t%s\t%s'%(ct, cor1, cor2))
                ouFile.write('%s\t%s\t%s\n'%(ct, cor1, cor2))
                plt.tight_layout()
                plt.savefig(inF.split('.txt')[0] + '_MinCounts%s_%s.pdf'%(MinCounts, ct))
                plt.savefig(inF.split('.txt')[0] + '_MinCounts%s_%s.svg'%(MinCounts, ct))

    ouFile.close()

    DF = pd.read_table(ouF, header=0)
    DF['Color'] = [CL[x.split('_')[0]] for x in DF['Contrast']]

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_title('counts > %s'%(MinCounts))
    sns.barplot(x='Contrast', y='PearsonR', data=DF, ax=ax, palette=DF['Color'])
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, fontsize=6)
    ax.set_xlabel('')
    ax.set_ylabel('pearson r')
    plt.tight_layout()
    plt.savefig(ouF.split('.txt')[0] + '_BarPlot.pdf')
    plt.savefig(ouF.split('.txt')[0] + '_BarPlot.svg')

ReplicatesCorrelation('MAVE_CodonCounts.txt', 0)
ReplicatesCorrelation('MAVE_CodonCounts.txt', 20)
ReplicatesCorrelation('MAVE_CodonCounts.txt', 100)

