from commands import *

#function
def z_start_named():
  getstatus('cd /opt/named/sbin')
  (status, output) = getstatusoutput('named')
  print 'named is run'
#  (status, output) = getstatusoutput('ps -ef | grep named')
#  print output

def z_stop_named():
  (status, output) = getstatusoutput('ps -ef | grep named')
  output = output + '\n'  #deal last line
#  print output
  count = output.count('\n')
#  print count
  for item in range(count):
    br = output.index('\n')
#    print br
    line = output[:br].split()
#    print line[1]
    getstatusoutput('kill -9 %s'%line[1])
    output = output[br+1:]
  print 'named is stop'
#  (status, output) = getstatusoutput('ps -ef | grep named')
#  print output

#main
z_start_named()
z_stop_named()
