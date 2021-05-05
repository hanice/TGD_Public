from pyst import *
from matplotlib_venn import venn3
def VennPlot(inF, Assays=['Assay22', 'Assay23', 'Assay24'], Bins=['Low', 'Middle', 'High']):
    D = {}
    inFile = open(inF)
    for line in inFile:
        line = line.strip()
        fields = line.split('\t')

        k = '\t'.join(fields[0:2])
        D.setdefault(fields[1], {})
        D[fields[1]].setdefault(fields[0], [])
        D[fields[1]][fields[0]] += fields[3].split(' ')
    
    for N in [0, 20, 100]:
        L = [set(D[str(N)][Assays[0]]), set(D[str(N)][Assays[1]]), set(D[str(N)][Assays[2]])]
        venn3(L, Assays)
        plt.title('%s (counts > %s)'%('Assays', N))
        plt.tight_layout()
        plt.savefig('%s_Min%s_Venn.pdf'%('Assays', N))
        plt.savefig('%s_Min%s_Venn.svg'%('Assays', N))
        plt.close()

    for N in [0, 20, 100]:
        L = [set(D[str(N)][Bins[0]]), set(D[str(N)][Bins[1]]), set(D[str(N)][Bins[2]])]
        venn3(L, Bins)
        plt.title('%s (counts > %s)'%('Bins', N))
        plt.tight_layout()
        plt.savefig('%s_Min%s_Venn.pdf'%('Bins', N))
        plt.savefig('%s_Min%s_Venn.svg'%('Bins', N))
        plt.close()



VennPlot('MAVE_CodonCounts_SingleBinVariantsRandomness.txt')
