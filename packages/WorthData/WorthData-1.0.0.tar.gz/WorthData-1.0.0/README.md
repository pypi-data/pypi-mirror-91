# WorthData(WD)
## Simple Database For Python
****
## Usage
```py
import WorthData as WD

database = WD.get('MyDatabase')
```
```py
database.create()
data = database.access()
```
```py
data['dict'] = {'str':'Support every data type','int':10,'list':['support','list'],'float':10.6}
```
```py
database.keep(data)
```
****
- Can Handle Big Amount Of Data
- Live Updating
    - when you change value of the key it will automatically update at your code