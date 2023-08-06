
# pyPasswordValidator  
My simple python password validation script to take over the world.

A simple program to detect if a password meets the [NIST](https://nam04.safelinks.protection.outlook.com/?url=https%3A%2F%2Fwww.nist.gov%2F&data=04%7C01%7CJonDuarte%40iheartmedia.com%7Cdefb1f313bae4df7ec2008d8b9a1d959%7C122a527e5b714eba878d9810b495b9e3%7C0%7C0%7C637463452070111718%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C1000&sdata=08ikdwZel28rsztRT%2Bm3SzIHDbhchJeVUjFOh5S8tgg%3D&reserved=0) requirements.

1.  Have an 8 character minimum
2.  AT LEAST 64 character maximum
3.  Allow all ASCII characters and spaces (unicode optional)
4.  Not be a common password
  
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
pip3 install pyPasswordValidator --user  
```  
## Usage  
### Setup
The script accepts input from STDIN in newline delimited format and will take a file of newline delimited common passwords and efficiently check if a password is in that file
If you would like, you can use this common password list to compare you list of passwords
```bash
wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt
```
Create a list of passwords you want to test:
```bash
cat > small_input.txt  
2small  
l;ksjaofieuaorihno234j23u8r9u3459328f9aaf89234289h98234us9ga8ert923r8a9gje8w9r3tr2j;o32ijq42oqijg8ewoa4ur8439q324gj9849gjao4i  
भारतभारतभारत  
password1
```
### You can either:  
- Import the module and use the methods  
```python  
Python 3.6.9 (default, Oct  8 2020, 12:12:24)
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pyPasswordValidator as pv
>>> pv.
pv.argparse           pv.is_ascii(          pv.main(              pv.password_len(      pv.re                 pv.remove_non_ascii(  pv.sys
>>> pv.is_ascii('test')
True
```  
- Can run the script as is
```bash
cat small_input.txt | python3 pyPasswordValidator.py 10-million-password-list-top-1000000.txt  
2small -> Error: Too Short  
l;ksjaofieuaorihno234j23u8r9u3459328f9aaf89234289h98234us9ga8ert923r8a9gje8w9r3tr2j;o32ijq42oqijg8ewoa4ur8439q324gj9849gjao4i -> Error: Too Long  
************ -> Error: Invalid Charaters  
password1 -> Error: Too Common 
```  
  
## Testing  
  
```python  
cd pyPasswordValidator/pyPasswordValidator/
python3 test_pyPasswordValidator.py 
```  
  
## Contributing  
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.  
  
Please make sure to update tests as appropriate.
