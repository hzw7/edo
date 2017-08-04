#!/usr/python/env python
#
#################################################################################################################
#  EDO v 0.05 - encryption domain optimizer by hubert.wisniewski@gmail.com
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#
#  The script parses a file with ACL to see if there are ovelapping entries within one 'object-group network'.
#  It doesn't support all features mentioned in Cisco documentation. In this version (0.04) it can analyze following
#  elements:
#
#  object-group network OBJECT-GROUP-NAME
#  |-network-object host IP
#  |-network-object IP Mask
#  |-network-object object OBJECT-NAME
#  |-group-object GROUP-OBJECT-NAME <-- not supported yet
#
#
#  object network OBJECT-NAME
#  |-subnet IP MASK
#  |-host IP
#  |-range IP IP  <-- not supported yet
#  |-fqdn         <-- not supported yet
#
#
##################################################################################################################
import sys, getopt

filename = sys.argv[1]
filename = str(filename)
debugmode = sys.argv[2:3]

if debugmode == ['-d']:
 debugmode = "on"

f = open(filename, 'r')
id = 0

#table-object-network
ton = []

#table-object-group-network
togn = []

#table-encr-domain
ted = []

#table-encr-domain-binary-hosts
tedbH = []

#table for hosts and subnets
tedbHS = []

#table-encr-domain-binary-hosts-new
tedbHn = []

#table-encr-domain-binary-subnets
tedbS = []

#final version of host duplicates
hostdupl = []

#final version of subnets/network duplicates
subnetdupl = []

#rest of items duplicates
restdupl = []

for line in f:
 id = id + 1
 eol = len(line)-1


 if line[0:14] == 'object network':
# object network name
  onn = line[15:eol]
  if debugmode == "on":
   print line[0:14] + ' -> OBJECT NAME: ' + onn


 if line[0:20] == 'object-group network':
# object group network name
  ognn = line[21:eol]
  if debugmode == "on":
   print line[0:20] + ' -> OBJECT-GROUP NAME: '+ ognn


 if line[1:7] == 'subnet':
# IP + Mask
  ipm = line[8:eol]
  ton.append([id,onn,"subnet",ipm,ipm])
  if debugmode == "on":
   print '|-'+line[1:7] +' -> SUBNET: '+ line[8:eol]


 if line[1:5] == 'host':
# IP
  ip = line[6:eol]
  ton.append([id,onn,"host",ip,'255.255.255.255'])
  if debugmode == "on":
   print '|-'+line[1:5] +' -> HOST: '+ line[5:eol]


 if line[1:20] == 'network-object host':
  ip = line[21:eol]
  togn.append([id,ognn,"host",ip,'255.255.255.255'])
  if debugmode == "on":
   print '|-'+line[1:20] +' -> HOST: '+ line[21:eol]


 if line[1:20] <> 'network-object host' and line[1:22] <> 'network-object object'  and line[1:15] == 'network-object':
  ip = line[16:eol]
  ipmask1 = ip.split(' ')
  ipaddr = ipmask1[0]
  mask = ipmask1[1]
  togn.append([id,ognn,"network",ipaddr,mask])
  if debugmode == "on":
   print '|-'+line[1:15] +' -> NETWORK-OBJECT: '+ line[16:eol]


 if line[1:22] == 'network-object object':
# network object object name
  noon = line[23:eol]
  togn.append([id,ognn,"object",noon,noon])
  if debugmode == "on":
   print '|-'+line[1:22] +' -> NETWORK-OBJECT OBJECT NAME: '+ noon

if debugmode == "on":
 print '\n\nObject network table:'
 for i in ton:
  print i

if debugmode == "on":
 print '\n\nObject group network table:'
 for i in togn:
  print i

if debugmode == "on":
 print '\n\nObject group network table:'
 
for i in togn:
 if [i[2]] == ['object']:
  i0 = i[0]
  
  if debugmode == "on":
   print i0
   
  i1 = i[1]
  
  if debugmode == "on":
   print i1
   
  i2 = i[2]
  
  if debugmode == "on":
   print i2
   
  i3 = i[3]
  
  if debugmode == "on":
   print i3
   
  i4 = i[4]
  
  if debugmode == "on":
   print i4
   
  for j in ton:
   if debugmode == "on":
    print j[1] + '-j - ton'
    print i4  + '-i4 - togn'
    print j[1] == i4
    
   if j[1] == i4:
    i34a = j[3]
    i34b = i34a.split(' ')
    i3 = i34b[0]
    if j[2] <> 'host':
     i4 = i34b[1]
     i2 = 'subnet'
    else:
     i4 = '255.255.255.255'
     i2 = 'host'
    togn.append([i0,i1,i2,i3,i4])


for i in togn:
 if i[2] <> 'object':
  ted.append(i)

if debugmode == "on":
 print '\n\nObject group network table:'
 for i in ted:
  print i

print '\n\n'

for i in ted:
 tedb0 = i[0]
 if debugmode == "on":
  print tedb0
 tedb1 = i[1]
 if debugmode == "on":
  print tedb1
 tedb2 = i[2]
 if debugmode == "on":
  print tedb2

# IP:
 tedb3 = i[3]
 if debugmode == "on":
  print tedb3

# Mask:
 tedb4 = i[4]
 if debugmode == "on":
  print tedb4

# IP binary:

 tedb5 = tedb3
 tedb5 = tedb5.split('.')

 tedb5a = tedb5[0]
 tedb5a = bin(int(tedb5a))
 tedb5a = tedb5a.split('0b')
 tedb5a = '00000000'+tedb5a[1]
 tedb5a = tedb5a[-8:]
 if debugmode == "on":
  print tedb5a

 tedb5b = tedb5[1]
 tedb5b = bin(int(tedb5b))
 tedb5b = tedb5b.split('0b')
 tedb5b = '00000000'+tedb5b[1]
 tedb5b = tedb5b[-8:]
 if debugmode == "on":
  print tedb5b

 tedb5c = tedb5[2]
 tedb5c = bin(int(tedb5c))
 tedb5c = tedb5c.split('0b')
 tedb5c = '00000000'+tedb5c[1]
 tedb5c = tedb5c[-8:]
 if debugmode == "on":
  print tedb5c

 tedb5d = tedb5[3]
 tedb5d = bin(int(tedb5d))
 tedb5d = tedb5d.split('0b')
 tedb5d = '00000000'+tedb5d[1]
 tedb5d = tedb5d[-8:]
 if debugmode == "on":
  print tedb5d

 tedb5ad = tedb5a+tedb5b+tedb5c+tedb5d
 
 if debugmode == "on":
  print tedb5ad

# Mask binary:

 tedb6 = tedb4
 tedb6 = tedb6.split('.')

 tedb6a = tedb6[0]
 tedb6a = bin(int(tedb6a))
 tedb6a = tedb6a.split('0b')
 tedb6a = '00000000'+tedb6a[1]
 tedb6a = tedb6a[-8:]
 if debugmode == "on":
  print tedb6a

 tedb6b = tedb6[1]
 tedb6b = bin(int(tedb6b))
 tedb6b = tedb6b.split('0b')
 tedb6b = '00000000'+tedb6b[1]
 tedb6b = tedb6b[-8:]
 if debugmode == "on":
  print tedb6b

 tedb6c = tedb6[2]
 tedb6c = bin(int(tedb6c))
 tedb6c = tedb6c.split('0b')
 tedb6c = '00000000'+tedb6c[1]
 tedb6c = tedb6c[-8:]

 tedb6d = tedb6[3]
 tedb6d = bin(int(tedb6d))
 tedb6d = tedb6d.split('0b')
 tedb6d = '00000000'+tedb6d[1]
 tedb6d = tedb6d[-8:]
 if debugmode == "on":
  print tedb6d

 tedb6ad = tedb6a+tedb6b+tedb6c+tedb6d

 tedb6adtmp = tedb6ad.split('0')
 tedb6adtmp = tedb6adtmp[0]
 tedb6adlen = len(tedb6adtmp)
 if debugmode == "on":
  print tedb6adtmp
  print tedb6adlen
  print tedb6ad

 if tedb2 == 'host':
  tedbH.append([tedb5ad,tedb1,tedb6ad,tedb6adlen,tedb0,tedb2,tedb3,tedb4])
 else:
  tedbS.append([tedb5ad,tedb1,tedb6ad,tedb6adlen,tedb0,tedb2,tedb3,tedb4])

if debugmode == "on":
 for i in tedbH:
  print i
 print ('\n\n')

if debugmode == "on":
 for i in tedbS:
  print i
 print ('\n\n')

# tedbHn - unique table with host entries

used = []
tedbHn = [[sub, used.append(sub[0:2])][0] for sub in tedbH if sub[0:2] not in used]

for i in tedbHn:
 for j in tedbH:
  if i == j:
   tedbH.remove(j)
   if debugmode == "on":
    print('removed\n')

if debugmode == "on":    
 print ('duplicate hosts in tedbH\n')
for i in tedbH:
 i1 = i[1]
 if debugmode == "on":
  print i1
 i6 = i[6]
 if debugmode == "on":
  print i6
 i7 = i[7]
 if debugmode == "on":
  print i7
 hostdupl.append([i1,i6,i7])
 if debugmode == "on":
  print i[1:8]

print ('final version of host duplicates:')

for i in hostdupl:
 print i

#tedbSn - unique list with subnets

used = []
tedbSn = [[sub, used.append(sub[0:3])][0] for sub in tedbS if sub[0:3] not in used]

for i in tedbSn:
 for j in tedbS:
  if i == j:
   tedbS.remove(j)

for i in tedbS:
 i1 = i[1]
 if debugmode == "on":
  print i1
 i6 = i[6]
 if debugmode == "on":
  print i6
 i7 = i[7]
 if debugmode == "on":
  print i7
 subnetdupl.append([i1,i6,i7])
 if debugmode == "on":
  print i[1:8]

print ('\n\nfinal version of network duplicates:')

for i in subnetdupl:
 print i

if debugmode == "on":
 print('\n\nMerged host and subnet table (unique)')

tedbHS = tedbHn + tedbSn

tedbHSbis = tedbHS

if debugmode == "on":
 for i in tedbHS:
  print(i)
 print('\n\n')

#compare items by binary IP with the shortest mask a/23 and b/20 then compare only /20 bits

for i in tedbHSbis:
 if debugmode == "on":
  print i[0]
#i0 - ip address
 i0 = i[0]
#i1 - object name
 i1 = i[1]
#i3 - mask lenght
 i3 = i[3]
#i0 - ip address cut to mask lenght:
 i0 = i0[:i3]
# print i0
#i4 - index
 i4 = i[4]
 for j in tedbHS:
  if debugmode == "on":
   print j[0]
  j0 = j[0]
  j1 = j[1]
  j3 = j[3]
  j0 = j0[:j3]
  if debugmode == "on":
   print j0
  j4 = j[4]

  if i3 > j3:
   maska = j3
  else:
   maska = i3

#  print('\n\n')

  if i0[:maska] == j0[:maska] and i4 <> j4 and i1 == j1 :
   if debugmode == "on":
    print('-------------------------')
    print('i'+ str(i))

   restdupl.append([i[1],i[6],i[7]])

   if debugmode == "on":
    print('j'+ str(j))

   restdupl.append([j[1],j[6],j[7]])
   justnothing = "-----"
   restdupl.append(justnothing)

#print('\n\n')

print ('\n\nfinal version of overlapping networks/subnets:')
for i in restdupl:
print i
