# jonjpbm-password-validation
My simple python password validation script to take over the world


## Installation

To install this cool app, you need to

clone repo from my github
```bash
git clone git@github.com:jonjpbm/jonjpbm-password-validation.git
```

Or just download the zip file

## Usage
You can either import the module and use the methods

```python
import password_validator

password_validator.is_ascii('agoodstring') # returns 'words'
password_validator.remove_non_ascii('asdf¡Hola!' # returns 'geese'
password_validator.password_len(input_len) # returns 'phenomenon'
```
or you can run the script as is
```python
cat small_input.txt | python3 password_validator.py weak_password_list.txt
```

##Testing

```python
python3 test_password_validator.py

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
