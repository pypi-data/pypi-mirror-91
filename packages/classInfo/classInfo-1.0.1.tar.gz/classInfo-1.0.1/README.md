# classInfo

## Simple information writing module
****
## Usage
```py
import classInfo

about = classInfo.information(name='Dave',
                              age='23',
                              job='Developer',
                              salary='$12300',
                              co_worker='Mark')
print(about)###Return a dict of information
```
### There's only one function(not anymore)

## ReadInfo and dict in information(New in `1.0.1`)
![code](https://i.ibb.co/ydjGSCH/image.png)
![output](https://i.ibb.co/XJ3Hp5y/image.png)
```py
import classInfo

about = classInfo.information(name={'name1':'ali','name2':'ali'},
                              age='23',
                              job='poor',
                              wife='None')

print(classInfo.read_info(about))
```
****
