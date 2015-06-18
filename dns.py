import dns.resolver

answers = dns.resolver.query('3485913b698.cdn.boltcdn.com')
for rdata in answers:
    print(rdata)
	      
