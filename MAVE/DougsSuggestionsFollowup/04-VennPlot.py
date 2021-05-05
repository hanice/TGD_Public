from pyst import *
from matplotlib_venn import venn3
def VennPlot(inF, Assays=['Assay22', 'Assay23', 'Assay24'], Bins=['Low', 'Middle', 'High']):
    D = {}
    inFile = open(inF)
    for line in inFile:
        line = line.strip()
        fields = line.split('\t')

        k = '\t'.join(fields[0:2])
        D.setdefault(k, {})
        D[k][fields[2]] = set(fields[3].split(' '))
    
    for assay in Assays:
        for N in [0, 20, 100]:
            L = []
            for Bin in Bins:
                L.append(D['\t'.join([assay, str(N)])][Bin])
            venn3(L, Bins)
            plt.title('%s (counts > %s)'%(assay, N))
            plt.tight_layout()
            plt.savefig('%s_Min%s_Venn.pdf'%(assay, N))
            plt.savefig('%s_Min%s_Venn.svg'%(assay, N))
            plt.close()

    for Bin in Bins:
        for N in [0, 20, 100]:
            L = []
            for assay in Assays:
                L.append(D['\t'.join([Bin, str(N)])][assay])
            venn3(L, Assays)
            plt.title('%s (counts > %s)'%(Bin, N))
            plt.tight_layout()
            plt.savefig('%s_Min%s_Venn.pdf'%(Bin, N))
            plt.savefig('%s_Min%s_Venn.svg'%(Bin, N))
            plt.close()

    inFile.close()

VennPlot('MAVE_CodonCounts_SingleBinVariantsRandomness.txt')
