from pyst import *

def BarPlot(inF, Assays=['Assay22', 'Assay23', 'Assay24'], Bins=['Low', 'Middle', 'High']):
    df = pd.read_table(inF, header=0)
    df_sub = df.loc[df.iloc[:, 1].isin(Bins), :]
    g = sns.FacetGrid(data=df_sub, col='Bin', col_wrap=1, aspect=3)
    g.map_dataframe(sns.barplot, x='MinCounts', y='NumVariants', hue='NumAssays', palette=['C0', 'C1', 'C2'])
    g.set_axis_labels("MinCounts", "NumVariants")
    plt.legend()
    plt.tight_layout()
    plt.savefig(inF.split('.txt')[0] + '_Bins.pdf')
    plt.savefig(inF.split('.txt')[0] + '_Bins.svg')

BarPlot('MAVE_CodonCounts_SingleBinVariantsRandomness_NumBinsAssays.txt')
