text = 'DDdfFf.ff'
a = text.split('.')
tech = '%s%s' % (a[0][0].lower(), a[0][1:])
print(tech)

result = ''.join(list(map(lambda i: ' %s' % i.lower() if i.isupper() else i, tech)))

print(result)

