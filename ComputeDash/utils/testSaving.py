
import ComputeDash.utils.general_utils as gu

exampleLog = '../../logs/zagreus.stats'
exampleDb = '../../logs/zagreus.npy'

print('reading log')
log = gu.readLogFile(exampleLog)
print(f'log: {log}')

print('Writting as binary')
gu.writeLogHistory(exampleDb,log)
print('reading binary')
logHistory = gu.readLogHistory(exampleDb)
print(f'read in: {logHistory}')
