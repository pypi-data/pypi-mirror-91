# pyPasswordValidator  
My simple python password validation script to take over the world  
  
  
## Installation  
  
### To install this cool app, you can:  
  
- Clone repo from my github  
```bash  
git clone https://github.com/jonjpbm/pyPasswordValidator  
```  
  
- Download the zip file  
```bash  
wget https://github.com/jonjpbm/pyPasswordValidator/archive/main.zip  
```  
 - Pip install  
```bash  
pip install pyPasswordValidator --user  
```  
## Usage  
### You can either:  
- Import the module and use the methods  
```python  
import password_validator  
  
password_validator.is_ascii('agoodstring') # returns boolean 
password_validator.remove_non_ascii('asdf¡Hola!' # returns string with asterisk replacing non ascii
password_validator.password_len(input_len) # returns int length of string  
```  
- Can run the script as is  
```python  
cat small_input.txt | python3 pyPasswordValidator.py weak_password_list.txt  
```  
  
## Testing  
  
```python  
python3 test_password_validator.py  
```  
  
## Contributing  
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.  
  
Please make sure to update tests as appropriate.
