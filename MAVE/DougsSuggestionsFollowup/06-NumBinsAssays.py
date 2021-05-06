def NumBinsAssays(inF):
    ouFile = open(inF.split('.txt')[0] + '_NumBinsAssays.txt', 'w')
    ouFile.write('MinCounts\tBin\tNumAssays\tNumVariants\n')
    D = {}
    D2 = {}
    inFile = open(inF)
    for line in inFile:
        line = line.strip()
        fields = line.split('\t')
        k = '\t'.join(fields[1:3])
        D.setdefault(k, [])
        D[k] += fields[3].split(' ')
    inFile.close()

    for k in D:
        D2.setdefault(k, {})
        for item in set(D[k]):
            n = D[k].count(item)
            D2[k].setdefault(n, 0)
            D2[k][n] += 1
    
    for k in D2:
        for n in [1, 2, 3]:
            ouFile.write(k + '\t' + '%sAssays'%n + '\t' + str(D2[k][n]) + '\n')
    ouFile.close()


NumBinsAssays('MAVE_CodonCounts_SingleBinVariantsRandomness.txt')
